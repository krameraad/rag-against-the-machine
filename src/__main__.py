from pathlib import Path

from .chunking import CHUNKING_STRATEGIES


def index(path: Path) -> list[str]:
    result = []

    for file in path.iterdir():
        if file.is_dir():
            result.extend(index(file))
        else:
            if file.suffix in {'.md'}:
                result.extend(CHUNKING_STRATEGIES[file.suffix](file))
    return result


if __name__ == "__main__":
    print('-' * 62)
    print(f'NAME{' ' * 36} | CHARS{' ' * 3} | LINES')
    print('-' * 62)
    print(index(Path('data/raw/vllm-0.10.1')))
