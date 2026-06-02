# Navia Dratp Digital

> A fan-made Python recreation of the discontinued Navia Dratp strategy board game.

![Status](https://img.shields.io/badge/status-beta-orange)
![Language](https://img.shields.io/badge/python-3.11+-blue)
![Framework](https://img.shields.io/badge/pygame-2.x-green)
![License](https://img.shields.io/badge/license-fan--project-lightgrey)

---

## Overview

Navia Dratp Digital is an open-source fan project that aims to preserve and modernize the classic **Navia Dratp** board game through a modular Python implementation.

The goal is not only to recreate the original gameplay, but to build a maintainable platform capable of supporting:

* Human vs Human gameplay
* Single Player AI opponents
* Future online multiplayer
* Save and Load functionality
* Pixel-art graphics and animations
* Community-driven rules verification
* Long-term preservation of Navia Dratp

Project Website:

https://progretech.com/navia_dratp_digital_archive_site/

---

## Current Status

Current Release: **Beta v1.5**

### Implemented

* Launcher and Main Menu
* Rules Reference Screen
* Draft / Setup Phase
* Battlefield Rendering
* Summoning System
* Gyullas Economy
* Black Gulled and Red Gulled rules
* Maseitai Movement Framework
* Data-Driven Piece Definitions
* Dratp Activation Framework
* Piece Effect Panel
* Documentation Framework
* PyInstaller Packaging Support

### In Progress

* Full Dratp Effect Implementation
* Single Player AI
* Save / Load System
* Pixel-Art Graphics
* Sound Effects

### Planned

* Online Multiplayer
* Replay System
* AI Difficulty Levels
* Additional Board Themes
* Tournament Support

---

## Architecture

The project is intentionally modular.

```text
main.py
 │
 ├── src/
 │   │
 │   ├── app/
 │   │   ├── launcher.py
 │   │   └── game_app.py
 │   │
 │   ├── engine/
 │   │   ├── game_state.py
 │   │   ├── move_generator.py
 │   │   ├── dratp_rules.py
 │   │   ├── gyullas.py
 │   │   ├── board_zones.py
 │   │   └── setup_state.py
 │   │
 │   ├── ui/
 │   │   ├── board_view.py
 │   │   ├── setup_view.py
 │   │   ├── menu_view.py
 │   │   └── hud.py
 │   │
 │   └── utils/
 │
 └── data/
     └── maseitai_roster.json
```

### Design Philosophy

The architecture follows a strict separation of concerns:

* UI files display information.
* Engine files validate and execute rules.
* Data files define game pieces.
* Future AI modules will consume engine APIs.
* Future networking will reuse the same engine logic.

This keeps the codebase easy to maintain and extend.

---

## Features

### Draft Phase

Players alternate selecting Maseitai cards before the match begins.

Each player has an independent roster, meaning:

* Both players may draft the same Maseitai type.
* Players cannot draft duplicate copies within their own Keep.

### Summoning

Players may spend Gyullas to summon Maseitai from their Keep onto valid Summoning Squares.

### Gyullas Economy

* Black Gulled generate Gyullas through advancement.
* Red Gulled generate additional Gyullas through their movement rules.
* The Gyullas Reduction Zone modifies Dratp costs.

### Dratp System

Current implementation includes:

* Right-click activation
* Eligibility validation
* Turn-age validation
* Cost calculation
* Effect descriptions
* Dratp status tracking

Additional effects will be implemented incrementally.

---

## Building the Project

### Development

```bash
pip install -r requirements.txt
python main.py
```

### PyInstaller

```bash
pyinstaller --noconfirm --clean --onefile --windowed --name "NaviaDratp" --add-data "assets;assets" --add-data "data;data" --add-data "COPYRIGHT_AND_FAN_PROJECT_NOTICE.md;." --add-data "DEVELOPER_NOTES.md;." main.py
```

---

## Roadmap

### Beta v1.6

* Single Player AI (Basic)
* Save / Load Framework
* Human vs AI Mode
* AI Turn Indicators
* Additional Dratp Effects

### Beta v1.7

* Improved AI Evaluation
* More Complete Dratp Library
* Additional UI Polish

### Beta v2.0

* Pixel-Art Graphics
* Audio Framework
* Multiplayer Foundation

---

## Contributing

Contributions, bug reports, documentation improvements, and rules verification assistance are welcome.

Please review:

* DEVELOPER_NOTES.md
* COPYRIGHT_AND_FAN_PROJECT_NOTICE.md

before submitting contributions.

---

## Fan Project Disclaimer

This project is an unofficial fan-made recreation inspired by the discontinued **Navia Dratp** board game.

The author and contributors do **not** claim ownership of:

* Navia Dratp
* Bandai trademarks
* Bandai Namco intellectual property
* Original artwork
* Original card designs
* Original game assets

This repository exists for preservation, education, experimentation, and non-commercial fan development.

---

## Author

**Edwin A. Rodriguez**

GitHub:
https://github.com/eabdiel

Project Website:
https://progretech.com/navia_dratp_digital_archive_site/

---

*"Keep errors boring."*

# Navia Dratp Digital - Beta v1.5

## New in v0.7

- Battlefield visually centered between the left and right UI panels.
- Setup Phase now allows both players to draft the same Maseitai type.
  - Example: Player 1 can draft Troll and Player 2 can also draft Troll.
  - Each player still cannot draft duplicate copies within their own Keep.
- Full 44-piece Maseitai roster added to `data/maseitai_roster.json`.
- Maseitai movement is now data-driven through `movement_offsets`.
- Summoned Maseitai use their own movement profile instead of all using placeholder king movement.
- Movement patterns are stored in JSON so we can refine the compass diagrams without changing engine code.
- Corrected board-zone rules retained:
  - Black Gulled always start on the forward row.
  - Red Gulled always start on the Navia row beside the Navia.
  - Black Gulled move forward and earn 1 Gyullas.
  - Red Gulled move forward in one of three directions and earn 3 Gyullas.
  - At game start only 4 summon spaces are open because Gulled occupy the other 4.
  - Gyullas Reduction Zone is row 3, columns 1 through 5.

## Controls

### Setup Phase
- Click an available roster card to draft it for the active player.
- Players alternate picks until both have 7.
- The game starts automatically.

### Game Phase
- Left click a battlefield piece to select it.
- Left click a highlighted square to move.
- Left click one of your Keep cards to prepare a summon.
- Left click a highlighted summon square to summon.
- Press R to reset to Setup Phase.
- Press ESC to return to menu.

## Important Note About Movement

v0.7 introduces the correct architecture for Maseitai movement: each card carries movement offsets in JSON.

This version includes a first-pass interpretation of the visible movement compass diagrams from the reference images. Since the diagrams are small and some are partially compressed, the movement data is intentionally easy to correct in `data/maseitai_roster.json`.

Next refinement step: tune each individual Maseitai's compass offsets and Dratp movement/effect from the original scans.


## New in v0.8

- Battlefield moved lower so the top player's Maseitai row no longer overlaps the board.
- Right-click Maseitai context menu added.
- Choose `Dratp` from the context menu to activate the piece.
- Dratp is only allowed after the Maseitai has been on the field for more than 1 turn.
- Dratp cost uses the Maseitai value and respects the Gyullas Reduction Zone.
- First-pass Dratp effect handler added.
  - Simple Gyullas effects are functional.
  - Return-self-to-Keep is functional.
  - Send-self-to-Graveyard style effects are partially functional.
  - Complex effects are safely logged as placeholders for the next implementation round.


## Beta v1.4 Hotfix

- Rebuilt from stable v0.8.
- Fixed `BoardView._draw_wrapped()` class binding.
- Rewrote `GameApp._handle_board_click()` safely.
- Fixes crash where empty-board clicks could reference `piece.name`.
- Keeps lower board placement, selected Piece Effect panel, and Dratp flags.


## Beta v1.4 Documentation Pass

- Added source headers to all Python files.
- Added fan-project disclaimer and copyright notice.
- Added author and project links:
  - GitHub: https://github.com/eabdiel
  - Project Website: https://progretech.com/navia_dratp_digital_archive_site/
- Added hidden attribution footprint comments.
- Added comments around important logic sections.
- Added `COPYRIGHT_AND_FAN_PROJECT_NOTICE.md`.
- Added `DEVELOPER_NOTES.md`.


## Beta v1.5 UI Polish

- Raised the bottom player's Maseitai card row so the status/status detail bar no longer covers card costs.
- Kept the status bar anchored at the bottom of the window.
- Added more visual breathing room between bottom cards and the status bar.
- Updated footer version to `v1.5-beta`.
- Preserved the v1.4 documentation/copyright headers and fan-project notices.
