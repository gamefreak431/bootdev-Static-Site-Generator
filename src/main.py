from pathlib import Path
from page_generator import copy_static_assets, generate_page


def main():
    copy_static_assets()
    generate_page(
        source_path=Path("content/index.md"),
        template_path=Path("template.html"),
        dest_path=Path("public/index.html")
    )


if __name__ == "__main__":
    main()
