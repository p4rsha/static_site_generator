from pathlib import Path
import shutil
import sys

from page_gen import generate_pages_recursive



def copy_contents(source_path: Path, dest_path:Path) -> None:
    if dest_path.exists():
        shutil.rmtree(dest_path)

    dest_path.mkdir()

    for content in source_path.iterdir():


        if content.is_file():
            shutil.copy(content , dest_path / content.name)
            print(f"Copied {content.name} from {content} to { dest_path / content.name }")

        if content.is_dir():
            copy_contents( content , dest_path / content.name )








def main():

    source: Path = Path("static")
    dest: Path = Path("docs")
    copy_contents(source, dest)

    from_path_root = Path('content')
    template_path = Path('template.html')
    dest_path_root = Path('docs')

    base_path = sys.argv[1] if len(sys.argv) > 1 else '/'

    generate_pages_recursive(from_path_root, template_path, dest_path_root, base_path )



if __name__ == '__main__':
    main()