from pathlib import Path


def iterpath(path: Path):
    if path.is_file():
        yield path

    else:
        for sub in path.iterdir():
            yield from iterpath(sub)


def main():
    print(
        "WARNING: `/calc_symbols.py` is cosmetic file, it only needed to count symbols and strings in all files, only for author to be proud of his work."
    )

    strings = 0
    symbols = 0

    cwd = Path.cwd()

    for path in iterpath(cwd):
        if path.parent.name == "__pycache__":
            continue
        print(path.parent.suffix)
        if path.parent.suffix.endswith("py") == False:
            continue

        print(f"Scanning {path.relative_to (cwd)}")

        text = path.read_text()

        symbols += len(text)
        strings += len(text.split("\n"))

    print()

    print("Calculated:")
    print(f"{symbols = }")
    print(f"{strings = }")
    print(f"Moreless count of strings (including delted) = ~{strings * 1.5}")


if __name__ == "__main__":
    print("You're running `/calc_simbols.py` file as main, are you sure?")
    main()
