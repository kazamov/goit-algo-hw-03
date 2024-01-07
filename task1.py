from argparse import ArgumentParser
import pathlib
import os
import shutil


class ApplicationError(Exception):
    """Base class for all application errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def read_arguments():
    parser = ArgumentParser(
        description="Copy files from source directory to destination directory and sort them by extension in subdirectories",
        add_help=True,
    )

    parser.add_argument(
        "-s", "--source", help="Absolute path to source directory", required=True
    )
    parser.add_argument(
        "-d",
        "--destination",
        help="Absolute path to destination directory",
        default="C:\\dist",
    )

    try:
        args = parser.parse_args()

        print("source: ", args.source)
        print("destination: ", args.destination)

    except SystemExit as err:
        raise ApplicationError("Invalid arguments") from err

    else:
        return args.source, args.destination


def convert_to_paths(source: str, destination: str):
    source_path = pathlib.Path(source)
    destination_path = pathlib.Path(destination)

    if not source_path.is_absolute() or not destination_path.is_absolute():
        raise ApplicationError("Source or destination path is not absolute")

    if not source_path.exists():
        raise ApplicationError("Source path does not exist")

    if not source_path.is_dir():
        raise ApplicationError("Source path should be a directory")

    if not destination_path.is_dir():
        raise ApplicationError("Destination path should be a directory")

    if destination_path.exists():
        shutil.rmtree(destination_path)
    os.makedirs(destination_path)

    return source_path, destination_path


def find_free_name(files: set[str], initial_name: str) -> str:
    if initial_name not in files:
        return initial_name

    i = 1
    while True:
        new_name = f"{initial_name} ({i})"
        if new_name not in files:
            return new_name
        i += 1


def process_file(
    source_path: pathlib.Path,
    destination_path: pathlib.Path,
    files_map: dict[str, set[str]],
):
    name = source_path.stem
    extension = (source_path.suffix or ".unknown")[1:]
    file_destination_path = destination_path / extension

    if extension not in files_map:
        os.makedirs(file_destination_path, exist_ok=True)
        files_map[extension] = set()

    try:
        if name in files_map[extension]:
            free_name = find_free_name(files_map[extension], name)
            files_map[extension].add(name)
            shutil.copy(source_path, file_destination_path / f"{free_name}.{extension}")
        else:
            files_map[extension].add(name)
            shutil.copy(source_path, file_destination_path)
    except PermissionError:
        print(f"Permission denied for file '{source_path}'")
    except:
        print(f"Cannot copy file '{source_path}'")


def process_directory(
    source_path: pathlib.Path,
    destination_path: pathlib.Path,
    files_map: dict[str, set[str]],
):
    for item in source_path.iterdir():
        if item.is_file():
            process_file(item, destination_path, files_map)
        elif item.is_dir():
            process_directory(item, destination_path, files_map)


def copy_files(source_path: pathlib.Path, destination_path: pathlib.Path):
    process_directory(source_path, destination_path, {})


def main():
    """Напишіть програму на Python, яка рекурсивно копіює файли у вихідній директорії,
    переміщає їх до нової директорії та сортує в піддиректорії, назви яких базуються
    на розширенні файлів.
    """

    try:
        source, destination = read_arguments()

        source_path, destination_path = convert_to_paths(source, destination)

        copy_files(source_path, destination_path)

    except ApplicationError as err:
        print(err.message)
        return
    except:
        print("Something went wrong. Please, try again.")
        return


if __name__ == "__main__":
    main()
