# Navia Dratp Digital - Beta v1.1

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


## New in v0.9

- Board moved lower again to prevent top coordinate labels from hitting the top player's Maseitai cost area.
- Added a lower-right `Selected Piece` panel under Turn Overview.
- Clicking a battlefield piece now displays:
  - Name
  - Owner
  - Type
  - Value/Cost
  - Dratp readiness
  - Dratp/effect text
- Right-clicking a Maseitai also populates the Selected Piece panel.
- Pieces that have successfully Dratp'ed now display a small `D` flag badge on the piece.


## Beta v1.0 Notes

This is the first beta build of the Python prototype.

Final fixes included before beta:

- Board moved lower again to leave visible breathing room between the top player's Maseitai row and the board.
- Lower-right panel now clearly displays selected-piece effect details under Turn Overview.
- The panel title is now `Piece Effect`.
- Dratp flags remain visible on battlefield pieces after a successful Dratp.
- Footer version updated to `v1.0-beta`.

This beta is ready for broader rule testing and iterative effect implementation.

## Beta v1.1 Hotfix

- Restored `BoardView._draw_wrapped()` after the Beta v1 panel refactor.
- Fixes crash after completing Maseitai setup and entering the board.
