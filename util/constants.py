SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
LINE_WIDTH = 2
PLAYER_TURN_SPEED = 300
PLAYER_ACCELERATION = 200
PLAYER_DRAG = 0.001
PLAYER_MAX_SPEED = 300
PLAYER_THRUST_PARTICLES = 2
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3
PLAYER_LIVES = 3
PLAYER_RESPAWN_INVULN_SECONDS = 2.0

# Scoring System
SCORE_SMALL_ASTEROID = 50       # Points for smallest asteroid
SCORE_MEDIUM_ASTEROID = 150     # Points for medium asteroid
SCORE_LARGE_ASTEROID = 400      # Points for largest asteroid
SCORE_MAX = 999999              # Maximum displayable score

# Combo System
COMBO_WINDOW_SECONDS = 2.0      # Time window to maintain combo
COMBO_INITIAL_MULTIPLIER = 1    # Starting multiplier

# Score Display
SCORE_FONT_SIZE = 36            # Font size for score display
SCORE_COLOR = (255, 255, 255)   # White color for text
SCORE_POSITION = (10, 10)       # Top-left corner
COMBO_COLOR = (255, 215, 0)     # Gold color for combo text
COMBO_POSITION = (10, 50)       # Below score
HIGH_SCORE_COLOR = (100, 200, 255)  # Light blue color for high score
HIGH_SCORE_POSITION = (10, 90)  # Below combo
LIVES_COLOR = (255, 255, 255)   # White color for lives text
LIVES_POSITION = (10, 130)      # Below high score

# High Score Persistence
import pathlib  # noqa: E402 -- kept adjacent to its sole use below
HIGH_SCORE_FILE = str(pathlib.Path(__file__).parent.parent / "highscore.json")  # Anchored to project root

# Shield Power-up
SHIELD_POWERUP_RADIUS = 12              # Size of the collectible pickup
SHIELD_POWERUP_SPAWN_SECONDS = 20.0     # Time between pickup spawns
SHIELD_POWERUP_LIFETIME_SECONDS = 8.0   # Uncollected pickup disappears after this
SHIELD_DURATION_SECONDS = 10.0          # Active shield expires after this
SHIELD_WARNING_SECONDS = 2.0            # Shield and pickup blink when this close to running out
SHIELD_BREAK_INVULN_SECONDS = 2.0       # Grace period after the shield absorbs a hit
SHIELD_RADIUS_SCALE = 1.5               # Shield bubble radius relative to the ship
SHIELD_COLOR = (0, 200, 255)            # Cyan color for the shield and its pickup
