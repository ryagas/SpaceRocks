<!--
SYNC IMPACT REPORT
Version: 1.0.0 (Initial Constitution)
Date: 2025-11-23
Principles Defined: 5 core principles established
Changes: Initial constitution created from template
Follow-up TODOs:
  - Review and refine principles as team develops game
  - Add specific performance benchmarks as needed
  - Consider adding principle for sound/audio when implemented
-->

# SpaceRocks Constitution

A Python/Pygame arcade game inspired by the classic Asteroids. This constitution defines the core principles and standards that guide all development decisions for this project.

## Core Principles

### I. Game Feel First
**Rules:**
- Prioritize responsive controls and smooth gameplay above all else
- Player actions must feel immediate and satisfying (shooting, movement, explosions)
- Maintain consistent 60 FPS performance
- Tune game constants iteratively for optimal feel (speeds, cooldowns, sizes)
- Add visual and auditory feedback for all player actions

**Rationale:** Arcade games live or die by their "game feel" - the tactile responsiveness and satisfaction of controls. Technical correctness without satisfying gameplay is failure. Players must feel in complete control, and actions must have weight and impact.

### II. Clean Architecture
**Rules:**
- Maintain object-oriented design with clear inheritance hierarchies
- Use `CircleShape` as base for all game entities
- Keep entity logic encapsulated in respective classes (`Player`, `Asteroid`, `Shot`)
- Separate concerns: game loop, rendering, collision, spawning handled independently
- All entity groups managed through pygame's sprite system
- No god objects or classes that do everything

**Rationale:** The codebase is well-structured with clear separation between entities. This pattern scales well as we add power-ups, enemies, and new mechanics. Clean architecture makes the codebase maintainable and debuggable.

### III. Constants-Driven Configuration
**Rules:**
- All tunable values live in `constants.py` (speeds, sizes, rates, cooldowns)
- No magic numbers in game logic code
- Constants use ALL_CAPS naming
- Group related constants together with clear names
- Constants should enable rapid iteration without code changes

**Rationale:** Game balance requires constant tweaking. Centralizing configuration in `constants.py` allows rapid iteration on game feel without touching logic code. This follows the established pattern in the codebase.

### IV. Performance & Frame Rate
**Rules:**
- Target 60 FPS on modern hardware as baseline
- Use delta time (`dt`) for all time-based calculations
- Optimize collision detection for large numbers of entities
- Profile before optimizing - measure, don't guess
- Efficient sprite group operations (avoid O(n²) where possible)

**Rationale:** Arcade games demand consistent frame rates for responsive controls. The game loop already uses delta time properly. As we add more asteroids, power-ups, and effects, maintaining performance becomes critical.

### V. Extensibility for Features
**Rules:**
- Design new features as modular additions, not modifications
- Use composition over inheritance where appropriate
- Power-ups should be self-contained entities
- New weapon types should extend, not replace, existing shooting logic
- Event logging system (`logger.py`) must capture all game events

**Rationale:** The WISHLIST shows many planned features (power-ups, weapon types, scoring). The architecture must support adding these without rewriting core systems. The existing event logging demonstrates forward-thinking design.

## Code Quality Standards

**Style & Conventions:**
- Follow PEP 8 for Python code style
- Use tabs for indentation (matching existing codebase)
- Descriptive variable names over comments
- Type hints encouraged for public methods
- Keep methods focused and small

**Testing:**
- Test core game mechanics (collision, splitting, movement)
- Validate constants produce desired gameplay
- Manual playtesting is primary validation method
- Automated tests for collision math and entity logic

**Dependencies:**
- Minimize external dependencies beyond Pygame
- Python 3.13+ required (per `pyproject.toml`)
- Lock dependency versions in `pyproject.toml`

## Feature Development Process

**Adding New Features:**
1. Update WISHLIST.md with detailed requirements
2. Define any new constants needed
3. Implement as modular, testable component
4. Playtest extensively for game feel
5. Adjust constants based on feedback
6. Document any new event types in logger

**Integration Requirements:**
- New entities must inherit from `CircleShape` or have clear rationale
- Collision detection must work with existing system
- Frame rate impact must be acceptable
- Constants must be tunable without code changes

## Governance

**Constitution Authority:**
- This constitution guides all development decisions
- Principles are mandatory; guidelines are recommended
- When in doubt, prioritize game feel over technical purity

**Amendment Process:**
- Amendments require clear rationale and team consensus
- Version number increments with each amendment
- Document migration impact for breaking changes
- Preserve spirit of original principles

**Compliance:**
- All pull requests reviewed against these principles
- Feature additions must align with extensibility principle
- Performance regressions are blockers
- Game feel changes require playtester validation

**Version**: 1.0.0 | **Ratified**: 2025-11-23 | **Last Amended**: 2025-11-23