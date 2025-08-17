# Introduction

A tutorial for learning curses for building a roguelike game in python.
This is just for learning cureses.

## Step 1: understanding how to draw a basic window in cures.
- Pass a screen object (`stdscr`) to the main function.
- Call `stdscr.curs_set(0)` to hide the cursor.
- Call `stdscr.keypad(True)` to enable the keyboard.
- Start a loop.
- Get the height and width of the screen by calling `stdscr.getmaxyx()`.
- Call `stdscr.erase()` to clear the screen.
- Create some things we want to display on the main scree.
### Adding text to the screen.
- Call `stdscr.addnstr()` to display the things.
```python
stdscr.addnstr(0, 0, msg, w-1, curses.A_BOLD)
```
This snippet above does the following.
- Writes msg at row 0, column 0.
- addnstr limits the number of characters written to at most w-1. This avoids writing into the last column which could cause wrapping or a curses error if the text would overflow the window width.
- curses.A_BOLD applies bold attribute.

### Adding more text.
- call `stdscr.addnstr(1, 0, size, w-1)` to display a message about the size of the window on the next line.

Note that the Y position is 0-based and starts from the top left corner of the scree.
This call above writes the message at the next line below our previous message.

- Call `stdscr.refresh()` to update the screen with the changes we made.
- Wait for input by calling `stdscr.getch()`.
- Process the input.
- If the user presses `q` or `Q`, exit the loop.

Special Notes:
- `curses.A_BOLD` is a constant that can be used to apply bold attribute to a string.
- calling `getmaxyx()` each iteration means the display updates correctly if the terminal is resized.
- `getch()` returns an int; ord('q') converts the character 'q' to its integer code for comparison.
#### curses.wrapper()
`curses.wrapper()` is a function that takes a function as an argument and calls it with a screen object as an argument.
This is a safe/clean setup and teardown for curses apps.  This helps with
- automatic initialization and cleanup.
  - calls initscr()
  - sets up the terminal modes
  - creates a screen object (`stdscr`)
  - On exit, restores the terminal state by calling `endwin()`.
    - rests echo and break modes
    - makes sure your shell isn't broken.
- Exception handling
  - restores the terminal as stated above.
  - provides a traceback.
- reduces boilerplate code.
Without the wrapper you'd be looking at somehting like the following.
```python
# Python
import curses

def main(stdscr):
    # your curses code here
    ...

def run():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    try:
        return main(stdscr)
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()

if __name__ == "__main__":
    run()
```




