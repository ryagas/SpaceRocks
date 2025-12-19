SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
LINE_WIDTH = 2
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3

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

# High Score Persistence
HIGH_SCORE_FILE = "highscore.json"  # File to store high score
