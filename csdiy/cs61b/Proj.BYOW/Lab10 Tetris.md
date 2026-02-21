> [!Warning]
> This lab has a lot of **helper methods**
> the coordinates (0, 0) represent the bottom left of the board.

All of your implementation will be in `Tetris.java`. We have also provided three other files:
- `Tetromino.java`: contains the board pieces that you’ll be using
- `Movement.java`: contains logic for rotating and moving the pieces
- `BagRandomizer.java`: helps randomize the pieces that are spawned

We’ll also be working with a library, `StdDraw`, to help implement some features, such as user input. You will find this library very useful for Project 3.


While we want to have a working game of `Tetris.java`, we should break it down into smaller steps instead of tackling it all at once. The game can be loosely broken down into the following steps:

1. Create the game window.
2. Randomly spawn a piece for the player to control and keep a display of the current score.
3. Update the movements of the piece based on the player’s input.
4. Once the piece can no longer move, check if any lines need to be cleared, update the score and respawn a new piece.
5. Repeat steps 2-4 until the game is over (when the uncleared lines reach the top).

## [[StdDraw_API]]
