from pathlib import Path
from page_generator import copy_static_assets, generate_pages_recursive

PROJECT_ROOT = Path(__file__).parent.parent


def main():
    copy_static_assets(
        static_path=PROJECT_ROOT / "static",
        public_path=PROJECT_ROOT / "public",
    )
    generate_pages_recursive(
        dir_path_content=PROJECT_ROOT / "content",
        template_path=PROJECT_ROOT / "template.html",
        dest_dir_path=PROJECT_ROOT / "public",
    )


if __name__ == "__main__":
    main()
