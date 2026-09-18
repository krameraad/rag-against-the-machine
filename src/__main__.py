import json
from pathlib import Path
from pprint import pprint

from .chunking import CHUNKING_STRATEGIES
from .data_models import MinimalSource


def index(max_chunk_size: int) -> list[MinimalSource]:
    def walk(max_chunk_size: int, path: Path) -> list[MinimalSource]:
        result = []
        for file in path.iterdir():
            if file.is_dir():
                result.extend(walk(max_chunk_size, file))
            else:
                if file.suffix in {'.md'}:
                    result.extend(CHUNKING_STRATEGIES[file.suffix](
                        max_chunk_size, file))
        return result

    result = walk(max_chunk_size, Path('data/raw'))

    Path('data/processed/').mkdir(parents=True, exist_ok=True)
    with Path('data/processed/index.json').open('w') as f:
        json.dump(result, f, indent='\t', default=lambda x: x.__dict__)
    print("Ingestion complete! Indices saved under data/processed/")
    return result


def search(query: str, k: int) -> list[MinimalSource]:
    print("Searching")
    return []


def search_dataset(dataset_path: str, k: int, save_directory: str) -> None:
    print("Searching dataset")


def answer(query: str, k: int) -> None:
    print("Answering")


def answer_dataset(
        student_search_results_path: str,
        save_directory: str) -> None:
    print("Answering dataset")


def evaluate(
        student_search_results_path: str,
        dataset_path: str) -> None:
    print("Evaluating")


if __name__ == "__main__":
    # print('-' * 62)
    # print(f'NAME{' ' * 36} | CHARS{' ' * 3} | LINES')
    # print('-' * 62)
    for source in index(2000)[:10]:
        print()
        print(source.info())
