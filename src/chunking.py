from pathlib import Path

from .data_models import MinimalSource


def chunk_py(path: Path) -> list[MinimalSource]:
    return []


def chunk_md(path: Path) -> list[MinimalSource]:
    return []


def chunk_txt(path: Path) -> list[MinimalSource]:
    with path.open() as f:
        content = f.read()
        lines = content.splitlines()
    name = path.name[:37] + '...' if len(path.name) > 40 else path.name
    print(f'{name:<40} | {len(content):>8} | {len(lines):>8}')
    return []


CHUNKING_STRATEGIES = {'.py': chunk_txt, '.md': chunk_txt, '.txt': chunk_txt}
