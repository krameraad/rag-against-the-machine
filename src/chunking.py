from pathlib import Path
import re

from .data_models import MinimalSource


CHUNKING_PATTERNS = {
    '.py': re.compile(
        r"^[ \t]*(?:(?:async[ \t]+)?def|class)[ \t]+.+$",
        re.MULTILINE
        ),
    '.md': re.compile(r"^#{1,6}[ \t]+.+$", re.MULTILINE),
    '.txt': re.compile('matchnothing^', re.MULTILINE)
}


def chunk(path: Path, suffix: str, max_chunk_size: int) -> list[MinimalSource]:
    # Don't chunk files that don't have a chunking strategy defined.
    if suffix not in CHUNKING_PATTERNS:
        return []

    content = path.read_text()
    length = len(content)

    if length <= max_chunk_size:
        return [MinimalSource(
            file_path=str(path),
            first_character_index=0,
            last_character_index=length - 1
        )]

    matches = list(CHUNKING_PATTERNS[suffix].finditer(content))
    result = []

    # Content before the first header.
    if matches and content[:matches[0].start()].strip():
        result.append(MinimalSource(
            file_path=str(path),
            first_character_index=0,
            last_character_index=matches[0].start() - 1
        ))

    # Add all sections to the result.
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else length

        result.append(MinimalSource(
            file_path=str(path),
            first_character_index=start,
            last_character_index=end - 1
        ))

    # File with no headers.
    if not matches and content.strip():
        result.append(MinimalSource(
            file_path=str(path),
            first_character_index=0,
            last_character_index=length - 1
        ))
    return result
