import tempfile
import unittest
from pathlib import Path

from page_generator import copy_static_assets, generate_page, generate_pages_recursive

TEMPLATE = "<title>{{ Title }}</title><article>{{ Content }}</article>"


class FileSystemTestCase(unittest.TestCase):
    """Gives each test a fresh temporary directory, deleted afterwards."""

    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        self.root = Path(temp_dir.name)

    def write(self, relative_path: str, text: str) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


class TestCopyStaticAssets(FileSystemTestCase):
    def test_copies_nested_files(self):
        self.write("static/index.css", "body {}")
        self.write("static/images/tom.png", "not really a png")
        copy_static_assets(self.root / "static", self.root / "public")
        self.assertEqual((self.root / "public/index.css").read_text(), "body {}")
        self.assertTrue((self.root / "public/images/tom.png").is_file())

    def test_removes_stale_files_from_previous_build(self):
        self.write("static/index.css", "body {}")
        self.write("public/old_page.html", "stale")
        copy_static_assets(self.root / "static", self.root / "public")
        self.assertFalse((self.root / "public/old_page.html").exists())


class TestGeneratePage(FileSystemTestCase):
    def test_fills_title_and_content_into_template(self):
        source = self.write("content/index.md", "# Hello\n\nSome text")
        template = self.write("template.html", TEMPLATE)
        dest = self.root / "public/index.html"
        generate_page(source, template, dest)
        self.assertEqual(
            dest.read_text(),
            "<title>Hello</title><article><div><h1>Hello</h1><p>Some text</p></div></article>",
        )

    def test_creates_missing_parent_directories(self):
        source = self.write("content/index.md", "# Hello")
        template = self.write("template.html", TEMPLATE)
        dest = self.root / "public/blog/tom/index.html"
        generate_page(source, template, dest)
        self.assertTrue(dest.is_file())


class TestGeneratePagesRecursive(FileSystemTestCase):
    def setUp(self):
        super().setUp()
        self.template = self.write("template.html", TEMPLATE)

    def generate(self):
        generate_pages_recursive(self.root / "content", self.template, self.root / "public")

    def test_mirrors_nested_directory_structure(self):
        self.write("content/index.md", "# Home")
        self.write("content/contact/index.md", "# Contact")
        self.write("content/blog/tom/index.md", "# Tom")
        self.generate()
        for page in ["index.html", "contact/index.html", "blog/tom/index.html"]:
            with self.subTest(page=page):
                self.assertTrue((self.root / "public" / page).is_file())

    def test_nested_pages_do_not_overwrite_each_other(self):
        # Regression test: using md_file.name as the destination sent every
        # index.md to public/index.html, each one overwriting the last.
        self.write("content/index.md", "# Home")
        self.write("content/blog/tom/index.md", "# Tom")
        self.generate()
        self.assertIn("<title>Home</title>", (self.root / "public/index.html").read_text())
        self.assertIn("<title>Tom</title>", (self.root / "public/blog/tom/index.html").read_text())

    def test_ignores_non_markdown_files(self):
        self.write("content/index.md", "# Home")
        self.write("content/notes.txt", "not markdown")
        self.generate()
        generated = sorted(p.relative_to(self.root / "public").as_posix() for p in (self.root / "public").rglob("*"))
        self.assertEqual(generated, ["index.html"])


if __name__ == "__main__":
    unittest.main()
