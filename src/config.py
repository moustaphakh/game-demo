# --- Window ---
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS = 60
BG_COLOR = (30, 30, 40)   # background color

# --- World ---
TILE_SIZE = 32            # 1 tile = 32x32 px

# --- Player physics (fundamental constants, might change) ---
PLAYER_SPEED    = 200     # px/s left-right
JUMP_VELOCITY   = -350    # px/s (negative is up)
GRAVITY         = 1200    # px/s^2
MAX_FALL_SPEED  = 800     # px/s capping the fall speed

# --- Colors ---
BG_COLOR     = (30, 30, 40)
WALL_COLOR   = (80, 80, 100)
COIN_COLOR   = (240, 210, 80)
FLAG_COLOR   = (120, 200, 120)
PLAYER_COLOR = (200, 140, 200)

# --- Tile symbols ---
EMPTY_CHAR  = '.'
WALL_CHAR   = '#'
COIN_CHAR   = 'C'
FLAG_CHAR   = 'F'
PLAYER_CHAR = 'P'