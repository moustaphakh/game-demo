#this file contains the tile setup for the game
import pygame
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

def iter_tiles(rows):
    """Yield (tx, ty, ch) for every tile coordinate."""
    for ty, row in enumerate(rows):
        for tx, ch in enumerate(row):
            yield tx, ty, ch

def build_solids(rows, wall_char, tile_size):
    """Return a list of Rects for solid tiles (e.g., '#')."""
    rects = []
    for tx, ty, ch in iter_tiles(rows):
        if ch == wall_char:
            rects.append(pygame.Rect(tx * tile_size, ty * tile_size, tile_size, tile_size))
    return rects