from pathlib import Path

_DEFAULT_SEPARATORS = ["\n\n", "\n", " ", ""]


def _split(text: str, chunk_size: int, separators: list[str]) -> list[str]:
    """Recursive core: split text into chunks using the coarsest separator that works."""
    if len(text) <= chunk_size:
        return [text]

    sep, *rest = separators

    if not sep:  # empty string = hard split at chunk_size
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    pieces = text.split(sep)
    chunks = []
    buffer = ""

    for piece in pieces:
        candidate = buffer + sep + piece if buffer else piece
        if len(candidate) <= chunk_size:
            buffer = candidate
        else:
            if buffer:
                chunks.append(buffer)
            # piece itself may be too large — recurse with next finer separator
            if len(piece) > chunk_size:
                chunks.extend(_split(piece, chunk_size, rest or [""]))
                buffer = ""
            else:
                buffer = piece

    if buffer:
        chunks.append(buffer)

    return chunks


def _add_overlap(chunks: list[str], chunk_overlap: int) -> list[str]:
    """Prepend the tail of each chunk onto the next to preserve boundary context."""
    if chunk_overlap == 0 or len(chunks) <= 1:
        return chunks
    result = [chunks[0]]
    for i in range(1, len(chunks)):
        tail = chunks[i - 1][-chunk_overlap:]
        result.append(tail + chunks[i])
    return result


def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    separators: list[str] | None = None,
) -> list[str]:
    """Split text into overlapping chunks using recursive character splitting.

    Tries separators from coarsest to finest (\n\n → \n → space → hard split)
    so chunks respect natural document boundaries where possible.
    """
    if separators is None:
        separators = _DEFAULT_SEPARATORS[:]
    chunks = _split(text.strip(), chunk_size, separators)
    chunks = [c.strip() for c in chunks if c.strip()]
    return _add_overlap(chunks, chunk_overlap)


def chunk_document(
    file_path: str | Path,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[dict]:
    """Read a .txt/.md file and return a list of chunk dicts.

    Each dict: {"text": str, "source": str, "chunk_index": int}
    """
    text = Path(file_path).read_text(encoding="utf-8").strip()
    chunks = split_text(text, chunk_size, chunk_overlap)
    return [
        {"text": chunk, "source": Path(file_path).stem, "chunk_index": i}
        for i, chunk in enumerate(chunks)
    ]


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "ingestion/test.txt"
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    overlap = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    results = chunk_document(path, size, overlap)
    for c in results:
        print(f"[{c['chunk_index']}] ({len(c['text'])} chars) {c['text']!r}")
