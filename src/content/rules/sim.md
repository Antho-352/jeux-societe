---
title: "Sim rules: how to play the pencil game Sim"
game_name: "Sim"
aliases: ["Sim pencil game", "game of Sim"]
category: "pen-and-paper"
summary: "Sim is a two-player pencil game on six dots: take turns colouring the lines between them, and the first player to complete a triangle in their own colour loses."
players_min: 2
players_max: 2
equipment: ["paper", "two pencils or pens of different colours"]
public_domain: true
sources:
  - { label: "Sim (game), Wikipedia", url: "https://en.wikipedia.org/wiki/Sim_(game)" }
  - { label: "Graph Ramsey games, Wolfgang Slany (arXiv)", url: "https://arxiv.org/abs/cs/9911004" }
status: "published"
date_added: "2026-10-18"
seo_title: "Sim rules: how to play the pencil game Sim"
seo_description: "How to play Sim: draw six dots and fifteen lines, colour one line per turn, avoid making a triangle of your own colour. Why a draw is impossible, and tips to survive longer."
---
<!-- hand-edited -->
## What you need

A sheet of paper and two pens or pencils in different colours, say red and blue. That is all. Sim was introduced in 1969 by the mathematician Gustavus Simmons and is a favourite in maths classes because it is quick to learn and shows a real theorem at work.

## Setup

Draw six dots spaced out around a circle, like the corners of a hexagon. Then join **every dot to every other dot** with a thin pencil line. That gives fifteen lines, many of them crossing in the middle. Each player picks a colour and you decide who starts.

If you prefer not to draw the lines in advance, just draw the six dots: each move then draws a new coloured line between two dots instead of colouring an existing one.

## How to play

1. On your turn, colour **one** uncoloured line in your colour.
2. Players alternate until someone is forced to lose.
3. The danger is a **triangle**: three lines of the same colour joining three of the six dots. Only triangles whose three corners are dots count. Places where lines cross in the middle are not corners.

You must colour a line on every turn; passing is not allowed.

## Scoring and winning

The player who completes a triangle in **their own colour loses** immediately. Triangles of mixed colours mean nothing.

Sim can never end in a draw. A result from Ramsey theory, often stated as "among any six people, there are three who all know each other or three who are all strangers", guarantees that once all fifteen lines are coloured, a single-colour triangle must exist. So someone always loses before the lines run out.

Computer searches in 1974 showed that the second player can always win with perfect play. The strategy is too complicated to memorise, so in practice the game stays open.

## Common variants

- **Three colours, three players**: with 17 dots and every pair joined, three colours always produce a single-colour triangle. Players each have a colour and avoid triangles; the drawing gets crowded, so it suits large paper.
- **Two players, three colours**: on the same 17-dot figure, each player may colour any line in any of the three colours, and whoever first completes a one-colour triangle loses.
- **Bigger Sim**: on 18 dots, players must avoid a set of four dots fully joined in their colour (six lines).
- **Several lines per turn**: colour two lines each turn for a faster, more dangerous game.

## Tips for first games

- Early on, spread your lines between different dots. Two of your lines meeting at one dot create a "trap": the line closing that triangle becomes unplayable for you.
- Count the safe lines left for each player. Towards the end, the player with more safe moves usually wins.
- Make your opponent's lines meet: every pair of their lines sharing a dot removes one safe line from them.
- Use a pencil for the uncoloured lines and bold colours for played lines, so the board stays readable.
- Swap who starts after each game; the second player has the edge.

## Frequently asked questions

**Does a triangle made where lines cross count?** No. All three corners must be among the six dots.

**Can the game end in a draw?** No. Mathematics guarantees a one-colour triangle before all fifteen lines are coloured.

**Who has the advantage?** The second player can always win with perfect play, though finding the right moves is hard.

**Can I make a triangle in my opponent's colour?** You cannot; you only ever colour lines in your own colour.

**How long does a game take?** A few minutes. There are at most fifteen moves.
