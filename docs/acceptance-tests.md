# Acceptance Test Checklist

Run these checks on the target desktop with audio support available.

- [ ] Launch with `python3 pac-man.py config.json`.
- [ ] Missing/invalid config reports a clear warning and uses safe defaults.
- [ ] Menu buttons work by mouse and keyboard; highscore and instruction screens open.\n- [ ] Instruction screen contains no extra overlaid instruction text and its artwork back button returns to the menu by mouse.\n- [ ] Highscore screen shows the original menu artwork behind a readable panel; its back button returns by mouse.\n- [ ] Custom mazes (including 29×17) fit the gameplay viewport and actors remain aligned with cells.\n- [ ] Pellet, power-pellet, ghost-eaten, and player-hit sound effects play when the corresponding events occur.\n- [ ] Chomp, ghost, and power-pellet animations remain smooth at different frame rates.
- [ ] Player moves with arrows and WASD; attempted turns into walls do not stop current movement.
- [ ] Player cannot pass through maze walls.
- [ ] Small pellets increase score; power pellets increase score and frighten ghosts.
- [ ] Eating frightened ghosts increases score and ghosts return after a delay.
- [ ] Contact with a normal ghost costs one life and respawns the player.
- [ ] Invincibility prevents life loss; freeze and speed cheats work; level skip and extra-life cheats work.
- [ ] Pause freezes gameplay; resume returns to the same run; menu return works.
- [ ] Clearing all pellets advances through every configured level; the HUD shows the configured campaign length. Level timeout ends the run.
- [ ] Game over and victory show final score and accept a valid name.
- [ ] Saved highscores survive restarting the program and only the top ten remain.
- [ ] Missing audio does not prevent startup.
- [ ] Run `make clean`, `make test`, and `python3 -m compileall -q .`.

Automated syntax checks cannot replace live playtesting; record any environment-specific issues during peer review.
