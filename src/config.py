# --- Window ---
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS = 60
BG_COLOR = (30, 30, 40)   # background color

# --- World ---
TILE_SIZE = 32            # 1 tile = 32x32 px


# --- Player physics (fundamental constants, might change) ---
PLAYER_SPEED    = 200     # px/s left-right
JUMP_VELOCITY   = -420    # px/s (negative is up)
GRAVITY         = 1200    # px/s^2
MAX_FALL_SPEED  = 800     # px/s capping the fall speed
PLAYER_COLOR = (200, 140, 200)  # Player color
MAX_JUMPS = 2               # Number of jumps (1 = no double jump, 2 = double jump, etc.)
# Jump feel
LOW_JUMP_GRAVITY   = 600    # gentler gravity while holding jump (going up)
FALL_GRAVITY       = 1600   # stronger gravity when falling
MAX_JUMP_HOLD_MS   = 160    # how long “hold to go higher” lasts (in milliseconds)
JUMP_CUT_MULTIPLIER = 0.5   # when you release early, reduce upward speed


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