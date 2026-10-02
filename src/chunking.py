from pathlib import Path
import re

from .data_models import MinimalSource


PYTHON_RE = re.compile(
    r"^[ \t]*(?:(?:async[ \t]+)?def|class)[ \t]+.+$",
    re.MULTILINE,
)


def chunk_py(max_chunk_size: int, path: Path) -> list[MinimalSource]:
    return ['py']


# HEADER_RE = re.compile(
#     r"^(?P<header>#{1,6})[ \t]+(?P<title>.+?)[ \t]*$",
#     re.MULTILINE,
# )


HEADER_RE = re.compile(r"^#{1,6}[ \t]+.+$", re.MULTILINE)


def chunk_md(max_chunk_size: int, path: Path) -> list[MinimalSource]:
    content = path.read_text()
    length = len(content)

    if length <= max_chunk_size:
        return [MinimalSource(
            file_path=str(path),
            first_character_index=0,
            last_character_index=length - 1
        )]

    matches = list(HEADER_RE.finditer(content))
    result = []

    # Content before the first header
    if matches and content[:matches[0].start()].strip():
        result.append(MinimalSource(
            file_path=str(path),
            first_character_index=0,
            last_character_index=matches[0].start() - 1
        ))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else length

        result.append(MinimalSource(
            file_path=str(path),
            first_character_index=start,
            last_character_index=end - 1
        ))

    # File with no headers
    if not matches and content.strip():
        result.append(MinimalSource(
            file_path=str(path),
            first_character_index=0,
            last_character_index=length - 1
        ))
    return result


def chunk_txt(max_chunk_size: int, path: Path) -> list[MinimalSource]:
    return [MinimalSource(
        file_path=str(path),
        first_character_index=0,
        last_character_index=len(path.read_text()) - 1
    )]


CHUNKING_STRATEGIES = {'.py': chunk_py, '.md': chunk_md, '.txt': chunk_txt}
