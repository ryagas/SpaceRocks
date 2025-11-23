# Feature Specification: Scoring System with Combo Multipliers

**Feature Branch**: `scoring-system`  
**Created**: 2025-11-23  
**Status**: Draft  
**Input**: User description: "Create a scoring system that includes points awarded for destroying asteroids and a combo multiplier system that rewards skilled consecutive hits"

## Feature Overview

An arcade-style scoring system that rewards players for destroying asteroids, with an emphasis on skilled play through a time-based combo multiplier system. This feature enhances player engagement by providing immediate feedback for successful hits and rewarding rapid, consecutive asteroid destruction.

### Key Objectives

1. **Reward Skill**: Incentivize aggressive, accurate play through combo multipliers
2. **Provide Clear Feedback**: Display current score and combo status in real-time
3. **Maintain Game Feel**: Keep controls responsive and frame rate at 60 FPS

### Alignment with Constitutional Principles

- **Game Feel First**: Score updates are immediate and satisfying; combo system rewards skilled play
- **Clean Architecture**: New `ScoreManager` class follows OO design, integrates cleanly with existing event system
- **Constants-Driven Configuration**: All scoring values, combo timings, and display settings in [`constants.py`](constants.py)
- **Performance & Frame Rate**: Minimal computational overhead; score calculations are O(1) operations
- **Extensibility**: Modular design allows future additions (achievements, leaderboards, score events)

---

## User Scenarios & Testing

### User Story 1 - Basic Score Tracking (Priority: P1)

A player destroys asteroids and sees their score increase based on asteroid size, providing immediate feedback on their performance.

**Why this priority**: Core functionality required for all other scoring features. Delivers immediate value by quantifying player performance.

**Independent Test**: Can be fully tested by shooting asteroids and verifying score increases match expected values (50/150/400 points). Delivers basic progression tracking.

**Acceptance Scenarios**:

1. **Given** the game has just started, **When** player destroys a small asteroid (radius 20), **Then** score increases by 50 points
2. **Given** the game has just started, **When** player destroys a medium asteroid (radius 40), **Then** score increases by 150 points
3. **Given** the game has just started, **When** player destroys a large asteroid (radius 60), **Then** score increases by 400 points
4. **Given** the player has a score of 500, **When** player destroys another small asteroid, **Then** score increases to 550
5. **Given** the game is running, **When** player views the screen, **Then** current score is clearly visible in HUD

---

### User Story 2 - Combo Multiplier System (Priority: P2)

A skilled player hits multiple asteroids in quick succession (within 2 seconds) and sees their score multiplied, rewarding aggressive gameplay.

**Why this priority**: Adds depth to gameplay and rewards skilled players. Enhances game feel significantly. Can be added after basic scoring.

**Independent Test**: Can be tested by rapidly destroying asteroids within 2-second windows and verifying multiplier increases and score calculations. Delivers skill-based progression.

**Acceptance Scenarios**:

1. **Given** player destroys an asteroid, **When** player destroys another asteroid within 2 seconds, **Then** combo multiplier increases to 2x
2. **Given** player has a 2x combo, **When** player destroys another asteroid within 2 seconds, **Then** combo multiplier increases to 3x
3. **Given** player has a 3x combo and destroys a small asteroid, **When** score is calculated, **Then** player receives 50 × 3 = 150 points
4. **Given** player has a combo active, **When** 2 seconds pass without hitting an asteroid, **Then** combo multiplier resets to 1x
5. **Given** player has an active combo, **When** player views the screen, **Then** current combo multiplier is clearly visible (e.g., "2x COMBO!")

---

### Edge Cases

- **Rapid asteroid splitting**: When large asteroid splits into multiple smaller ones, each child asteroid hit within combo window extends the combo
- **Combo at game boundaries**: Combo resets on player death or game restart
- **Score overflow**: Score is capped at 999,999 to prevent display issues
- **Frame rate drops**: Combo timer uses delta time to ensure consistent 2-second window regardless of frame rate variations
- **Simultaneous hits**: If shot somehow hits multiple asteroids in same frame (edge case), each asteroid scores independently with same multiplier

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST award 50 points for destroying small asteroids (radius = ASTEROID_MIN_RADIUS)
- **FR-002**: System MUST award 150 points for destroying medium asteroids (radius = ASTEROID_MIN_RADIUS * 2)
- **FR-003**: System MUST award 400 points for destroying large asteroids (radius = ASTEROID_MAX_RADIUS)
- **FR-004**: System MUST apply combo multiplier to base points when calculating final score
- **FR-005**: System MUST increase combo multiplier by 1 when player destroys asteroid within 2 seconds of previous hit
- **FR-006**: System MUST reset combo multiplier to 1x when 2 seconds pass without an asteroid hit
- **FR-007**: System MUST reset combo multiplier to 1x when player dies or game restarts
- **FR-008**: System MUST display current score in HUD at all times during gameplay
- **FR-009**: System MUST display combo multiplier in HUD when combo is active (≥2x)
- **FR-010**: System MUST log all scoring events using existing [`logger.py`](logger.py) event system
- **FR-011**: System MUST cap maximum score at 999,999 to prevent display overflow
- **FR-012**: System MUST maintain 60 FPS performance during all scoring operations

### Key Entities

- **ScoreManager**: Manages score state and combo logic
  - Attributes: current_score, combo_multiplier, combo_timer
  - Responsibilities: Score calculation, combo timing, event logging
  
- **ScoreDisplay**: Renders score information to screen
  - Attributes: font, color, position
  - Responsibilities: HUD rendering, text formatting, visual feedback for combos

---

## Technical Design

### Architecture Overview

```
┌─────────────────────────────────────────────────┐
│              main.py (Game Loop)                │
│                                                 │
│  ┌──────────────┐      ┌──────────────┐       │
│  │  Collision   │─────→│ ScoreManager │       │
│  │  Detection   │      │              │       │
│  └──────────────┘      └──────┬───────┘       │
│                                │               │
│                                ↓               │
│                        ┌───────────────┐       │
│                        │ ScoreDisplay  │       │
│                        │   (HUD)       │       │
│                        └───────────────┘       │
└─────────────────────────────────────────────────┘

Data Flow:
1. Asteroid hit detected in main loop
2. ScoreManager.add_score(asteroid_size) called
3. ScoreManager calculates points with multiplier
4. ScoreManager updates combo state and timer
5. ScoreManager logs scoring event
6. ScoreDisplay renders updated values
```

### New Files Required

1. **`score_manager.py`** - Core scoring logic
   - Class: `ScoreManager`
   - Methods:
     - `__init__()`: Initialize score state
     - `add_score(asteroid_radius)`: Calculate and add points based on size
     - `update(dt)`: Update combo timer each frame
     - `reset()`: Reset score and combo for new game
     - `_update_combo()`: Increase combo multiplier
     - `_reset_combo()`: Reset combo to 1x
     - `_calculate_base_points(radius)`: Map radius to base point value
     - `get_current_score()`: Return current score
     - `get_combo_multiplier()`: Return current combo

2. **`score_display.py`** - Visual rendering
   - Class: `ScoreDisplay`
   - Methods:
     - `__init__(screen)`: Initialize fonts and positions
     - `draw(score_manager)`: Render score HUD
     - `_draw_text(text, position, color)`: Helper for text rendering

### Integration Points

1. **[`main.py`](main.py)** modifications:
   - Import `ScoreManager` and `ScoreDisplay`
   - Instantiate `score_manager` and `score_display` at game start
   - In collision detection loop (line 47): Call `score_manager.add_score(rock.radius)`
   - In update loop: Call `score_manager.update(dt)`
   - In render loop: Call `score_display.draw(score_manager)`
   - On player death: Call `score_manager.reset()`

2. **[`logger.py`](logger.py)** integration:
   - Add scoring events: `log_event('score_added', points=X, multiplier=Y, total=Z)`
   - Add combo events: `log_event('combo_increased', multiplier=X)`
   - Add combo events: `log_event('combo_reset')`

### Data Structures

```python
# ScoreManager state
{
    'current_score': int,        # 0 to 999,999
    'combo_multiplier': int,     # 1, 2, 3, 4, ...
    'combo_timer': float         # 0.0 to COMBO_WINDOW_SECONDS
}
```

### Constants to Add to [`constants.py`](constants.py)

```python
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
```

### Event Logging

New events to log via [`logger.py`](logger.py):

```python
# Score events
log_event('score_added', 
          asteroid_size='small'|'medium'|'large',
          base_points=50|150|400,
          multiplier=1|2|3|...,
          points_awarded=calculated_value,
          new_total=current_score)

log_event('combo_increased', 
          old_multiplier=X, 
          new_multiplier=Y)

log_event('combo_reset',
          final_multiplier=X,
          reason='timeout'|'death'|'manual')
```

---

## UI/Visual Design

### HUD Layout

```
┌─────────────────────────────────────────┐
│ SCORE: 12,450                           │
│ 3x COMBO!                               │  <- Gold text, only shown if combo ≥ 2x
│                                         │
│                                         │
│          [GAMEPLAY AREA]                │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

### Visual Elements

1. **Score Display**:
   - Position: Top-left corner (10, 10)
   - Font: Pygame default font, size 36
   - Color: White (255, 255, 255)
   - Format: "SCORE: X,XXX" with comma separators

2. **Combo Indicator**:
   - Position: Below score (10, 50)
   - Font: Same as score
   - Color: Gold (255, 215, 0) to stand out
   - Format: "Xx COMBO!" (e.g., "3x COMBO!")
   - Visibility: Only shown when multiplier ≥ 2x

### Color Scheme

- Primary text: White `(255, 255, 255)` - matches existing game aesthetic
- Combo text: Gold `(255, 215, 0)` - creates visual hierarchy and excitement
- Background: None (transparent) - maintains clean arcade look

### Animation Considerations

For initial implementation (minimal feedback):
- No animations required
- Static text display
- Instant updates on score changes

Future enhancement possibilities:
- Brief flash effect when combo increases
- Score pop-up numbers at asteroid destruction point
- Combo text pulse effect

---

## Implementation Considerations

### Performance Impact

**Expected Impact**: Minimal (< 0.1ms per frame)

- **Score calculations**: O(1) arithmetic operations
- **Combo timer**: Simple float decrement each frame
- **Text rendering**: Pygame's built-in text rendering (2 strings per frame)

**Performance Validation**:
- Monitor frame rate with scoring active
- Ensure consistent 60 FPS maintained
- Profile with 20+ asteroids and active combos

### Testing Approach

1. **Unit Tests** (optional but recommended):
   - Test `ScoreManager._calculate_base_points()` with all asteroid sizes
   - Test combo timer logic with various dt values
   - Test score cap at 999,999

2. **Integration Tests**:
   - Test score updates during actual gameplay
   - Verify combo timing with real-time play

3. **Playtest Scenarios**:
   - Rapid fire: Destroy 10+ asteroids quickly, verify combo increases
   - Slow play: Wait >2 seconds between hits, verify combo resets
   - Score progression: Play full game, verify final score calculations

### Edge Cases to Handle

1. **Gameplay**:
   - Player death mid-combo
   - Asteroid splits creating multiple targets quickly
   - Extremely long combos (>10x multiplier)
   - Score reaches maximum (999,999)

2. **Technical**:
   - Frame rate drops affecting combo timer accuracy
   - Delta time spikes
   - Multiple asteroids destroyed in single frame

### Future Extensibility

**Designed to Support**:

1. **Leaderboard System**:
   - Extend high score file to JSON format with player names
   - Add `ScoreManager.get_top_scores(n)` method
   - Create `LeaderboardDisplay` class

2. **Achievement System**:
   - Add achievement tracking to `ScoreManager`
   - Log achievement events
   - Hook into existing event system

3. **Power-up Score Bonuses**:
   - Add `score_multiplier_modifier` attribute
   - Implement temporary multiplier boosts
   - Stack with combo multipliers

4. **Score Events/Feedback**:
   - Extend `ScoreDisplay` for floating numbers
   - Add particle effects on high combos
   - Sound effect hooks for score milestones

**Modular Design Principles**:
- `ScoreManager` is independent of rendering
- Clear separation between logic and display
- Event-driven architecture for easy extension
- Constants-driven for easy tuning

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Score updates are immediate (< 16ms) when asteroid is destroyed, maintaining 60 FPS
- **SC-002**: Combo multiplier increases correctly when asteroids destroyed within 2.0 ± 0.1 second window
- **SC-003**: Players can achieve 5x+ combos through skilled play, validating skill-reward system
- **SC-004**: Score calculations are mathematically correct for all asteroid sizes and multiplier combinations
- **SC-005**: HUD displays score information clearly without obscuring gameplay (validated through playtest)

### Validation Methods

1. **Performance**: Profile with pygame clock, ensure avg frame time stays under 16ms (60 FPS)
2. **Accuracy**: Automated tests verify score calculations match expected values
3. **Game Feel**: Playtest feedback confirms scoring system enhances engagement
4. **Integration**: Manual testing confirms no conflicts with existing game systems

---

## Implementation Checklist

### Phase 1: Core Scoring (P1)
- [ ] Create `score_manager.py` with `ScoreManager` class
- [ ] Add scoring constants to [`constants.py`](constants.py)
- [ ] Implement base point calculation based on asteroid radius
- [ ] Integrate with collision detection in [`main.py`](main.py)
- [ ] Add score logging events to [`logger.py`](logger.py)
- [ ] Create `score_display.py` with basic HUD
- [ ] Test score accuracy for all asteroid sizes

### Phase 2: Combo System (P2)
- [ ] Implement combo timer in `ScoreManager.update(dt)`
- [ ] Add combo increase logic on asteroid hits
- [ ] Add combo reset logic on timeout
- [ ] Add combo multiplier to score calculations
- [ ] Add combo display to HUD
- [ ] Add combo logging events
- [ ] Playtest combo timing and feel

### Phase 3: Polish & Testing
- [ ] Performance profiling and optimization
- [ ] Edge case testing
- [ ] Playtest for game feel validation
- [ ] Documentation updates
- [ ] Code review against constitutional principles

---

## Technical Debt & Future Work

### Known Limitations

1. **Session-only scores**: Score resets between game sessions
2. **Minimal visual feedback**: No animations or particle effects
3. **No sound effects**: Score milestones and combos are silent

### Potential Improvements

1. **High Score Persistence**: Save and display best score across sessions
   - Simple file-based storage (e.g., `highscore.txt`)
   - Display high score in HUD alongside current score
   - Update and save when player beats previous high
2. **Enhanced Visual Feedback**: Floating damage numbers, combo animations, screen shake
3. **Audio Feedback**: Sound effects for score milestones, combo increases
4. **Score Breakdown**: Show detailed scoring breakdown on game over screen
5. **Statistics Tracking**: Average combo, highest combo, total asteroids destroyed
6. **Difficulty Scaling**: Award more points for higher difficulty levels
7. **Leaderboard System**: Multiple scores with player names, online leaderboards

---

## Conclusion

This scoring system specification provides a complete, implementable design that:
- Aligns with SpaceRocks constitutional principles
- Rewards skilled play through combo multipliers
- Maintains performance at 60 FPS
- Integrates cleanly with existing architecture
- Provides foundation for future enhancements (including persistence, leaderboards, and achievements)

The two-phase implementation approach focuses on core functionality first (scoring and combos), allowing for iterative development and testing. The modular design makes it easy to add high score persistence and other enhancements later without changing the core architecture.