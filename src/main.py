import argparse
from pathlib import Path
from page_generator import copy_static_assets, generate_pages_recursive


PROJECT_ROOT = Path(__file__).parent.parent

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_path", type=str, nargs="?", default="/", help="Base path for the generated site")
    return parser.parse_args()

def main():
    args = parse_args()
    base_path = args.base_path
    dest_path = PROJECT_ROOT / "docs"

    copy_static_assets(
        static_path=PROJECT_ROOT / "static",
        public_path=dest_path,
    )
    generate_pages_recursive(
        dir_path_content=PROJECT_ROOT / "content",
        template_path=PROJECT_ROOT / "template.html",
        dest_dir_path=dest_path,
        base_path=base_path,
    )


if __name__ == "__main__":
    main()
