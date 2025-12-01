# USER MANUAL — Flip 7 Card Game

## Overview
Flip 7 is a two‑player card game played over **three rounds**. Each player draws cards trying to build a hand of **unique number cards**, avoiding busts, and using ability and modifier cards to influence the game. The game includes an in‑game **Rules Screen**, **Options Menu**, and **Scores Display**.

---

## Game Objective
Win by either:
1. Reaching **7 unique number cards** first in a round, or
2. Finishing the 3‑round game with the **highest total score**.

---

## Startup Flow
When the game launches:
- The **Rules Screen** appears.
- Press **SPACE** to begin the game.
- The game then initializes players, deals initial cards, and starts Round 1.

---

## Controls
| Key | Action |
|-----|--------|
| **D** | Draw a card on your turn |
| **S** | Stand for the round (lock in your hand) |
| **ESC** | Open in‑game Options Menu |
| **UP/DOWN** | Navigate options menu |
| **ENTER** | Select menu item |

---

## Options Menu
Press **ESC** during gameplay to open the Options Menu.

### Menu Choices
- **Resume Game** — Return to gameplay.
- **View Rules** — Opens an on‑demand rule summary.
- **View Scores** — Shows current hand, scores, and status for both players.
- **Quit Game** — Exit immediately.

---

## Card Types
### Number Cards
- Values: `Zero` through `Twelve`.
- Drawing a **duplicate number card** causes a bust unless protected by Second Chance.
- Number cards count toward the **7‑card instant win condition**.

### Modifier Cards
Added to hand but **do not cause busts**:
- **+2, +4, +6, +8, +10** → add to final score.
- **x2** → multiplies the total value of number cards.

### Ability Cards
All activate **immediately**, except Second Chance.

#### Freeze
Forces opponent to **stand** for the round.

#### Flip Three
Opponent must draw **three cards**. They may:
- Draw safely,
- Use Second Chance automatically, or
- Bust.

#### Second Chance
Held until needed. Automatically prevents **one** bust, then expires.

---

## Turn Flow
Each round alternates player turns.
On your turn:
1. Press **D** to draw, or
2. Press **S** to stand.

A player becomes **inactive** after standing or busting.

---

## Busting Rules
A bust occurs if:
- The player draws a **duplicate number card** and
- **Second Chance is not active**.

Effects of busting:
- Player becomes inactive.
- Player earns **0 points** for the round.

---

## Round End Conditions
A round ends if:
1. A player reaches **7 number cards**, or
2. **Both players are inactive** (standing or busted).

---

## Scoring
If not busted, score is calculated as:

```
(number card total × multipliers) + additions
```

- Number card sum = total of all number card values.
- Multipliers = each **x2** card doubles current total.
- Additions = sum of all +X modifier cards.

Score is added to the player's **total score**.

---

## Displays
### During Gameplay
- Player hands shown at top/bottom.
- Status indicators: **BUSTED**, **STANDING**, or **Second Chance Active**.
- Current turn displayed in the center.
- Recent action message shown beneath turn message.
- Corner score totals updated continuously.

### Rules Display
Accessible at startup or through Options Menu.

### Scores Display
Shows:
- Total scores
- Status indicators
- Full hands per player

---

## Game End
After 3 rounds:
- Final scores are displayed.
- Highest total score wins.
- A complete game log is saved as **GameLog.txt**.

---

## System Requirements
- Python 3.x
- Pygame installed

Run the game using:
```
python main.py
```

---

End of USER_MANUAL.

