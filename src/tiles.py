#this file contains the tile setup for the game
# Each level is a text file with characters representing different tiles.
# For example:
# P = player spawn point
# . = empty space
# # = collision tile (ground, wall, etc.)
def load_level(path: str) -> list[str]:
    """Read a text file and return a list of rows (strings), all the same width."""
    with open(path, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f]
    assert rows, "Level file is empty"

    width = max(len(r) for r in rows)
    # Pad shorter rows with '.' so every row has equal length
    rows = [r.ljust(width, ".") for r in rows]
    return rows

# Find the first occurrence of a character in the level and return its (col, row) position
def find_char(rows: list[str], ch: str) -> tuple[int, int] | None:
    """Return (col, row) of the first occurrence of ch, or None if not found."""
    for row_idx, row in enumerate(rows):
        col_idx = row.find(ch)
        if col_idx != -1:
            return (col_idx, row_idx)
    return None
