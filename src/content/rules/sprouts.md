---
cover: "/img/rules/sprouts.png"
title: "Sprouts rules: how to play the game of sprouts"
game_name: "Sprouts"
aliases: ["game of sprouts", "Brussels sprouts"]
category: "pen-and-paper"
summary: "Sprouts is a two-player pencil game: join spots with lines that never cross, add a new spot on every line, never let a spot have more than three lines, and make the last possible move."
players_min: 2
players_max: 2
time_min: 10
time_max: 10
equipment: ["paper and pencil"]
public_domain: true
sources:
  - { label: "Sprouts (game), Wikipedia", url: "https://en.wikipedia.org/wiki/Sprouts_(game)" }
  - { label: "Computer Analysis of Sprouts, Applegate, Jacobson and Sleator (Carnegie Mellon University)", url: "https://www.cs.cmu.edu/~sleator/papers/Sprouts.htm" }
  - { label: "Sprouts notation, Dan Hoey (David Eppstein's Combinatorial Game Theory pages)", url: "https://ics.uci.edu/~eppstein/cgt/sprouts.html" }
status: "published"
date_added: "2026-10-18"
seo_title: "Sprouts rules: how to play the pencil game"
seo_description: "How to play sprouts: start with a few spots, draw a line and add a spot each turn, never cross a line or exceed three lines per spot, and make the last move. Plus misère and Brussels sprouts."
---
<!-- hand-edited -->
## What you need

A pencil and a sheet of paper. Sprouts was invented in 1967 by the mathematicians John Conway and Michael Paterson, and made famous by Martin Gardner's *Mathematical Games* column in *Scientific American*. It looks like doodling but hides real topology.

## Setup

Draw a few spots on the paper, well spaced. Two or three spots make a short game for learning; five or six give a proper contest. Decide who goes first.

## How to play

On your turn you do two things:

1. **Draw a line** joining two spots, or a loop from one spot back to itself. The line may be straight or curved.
2. **Add a new spot** somewhere along the line you just drew, not on its ends.

The line must obey three rules:

- It may not **cross or touch** itself or any other line, and may not pass through a spot.
- No spot may ever have more than **three lines** attached to it. A loop from a spot to itself counts as two lines at that spot.
- The new spot already has **two lines** (one each side), so it can take only one more.

A spot with three lines is **dead**. A spot with fewer than three is **alive** and can still be used.

## Scoring and winning

Players alternate until someone cannot make a legal move. In the normal game, **the player who makes the last move wins**: the player unable to move loses. There are no draws.

The game always ends. Each spot starts with three "lives"; every move uses up two lives at the ends of the line and creates a new spot with one life left, so the total falls by one each turn. A game with *n* starting spots lasts at least 2*n* moves and at most 3*n* − 1.

Who wins with perfect play depends on the number of spots. Computer analysis supports the **Sprouts conjecture**: the first player wins when the number of starting spots, divided by 6, leaves a remainder of 3, 4 or 5, and loses otherwise. Two spots is a second-player win; three spots a first-player win.

## Common variants

- **Misère sprouts**: the player who makes the last move **loses**. It is harder to analyse and played competitively online.
- **Brussels sprouts**: start with crosses (spots with four free arms) instead of spots. Each move joins two free arms with a line and draws a short stroke across it, creating two new arms. The number of moves is always 5*n* − 2 for *n* crosses, so the winner is decided before the game begins: a fun trick to play on someone once.
- **Bigger starts**: 7 or 8 spots make long, tricky games on a big sheet.

## Tips for first games

- Count moves, not spots. Since the game has a fixed range of possible lengths, your goal is to make the total number of moves odd if you started, even if you did not.
- Enclosing a region with a loop shortens the game: spots trapped inside can only connect to each other.
- Keeping all spots in one open group lengthens the game.
- Draw neatly and leave room; most arguments come from lines that seem to touch.
- With two spots, play both sides to see why the first player always loses.

## Frequently asked questions

**Can a line go from a spot to itself?** Yes, as a loop. It counts as two of that spot's three lines.

**Do the new spots count towards the three-line limit?** Yes. A new spot starts with two lines, so it can take one more.

**Can lines be curved?** Yes, any shape, as long as they never cross or touch another line.

**Who wins with three spots?** The first player, with perfect play.

**Can the game go on forever?** No. With *n* starting spots it ends after at most 3*n* − 1 moves.
