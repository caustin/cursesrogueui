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

## Step 2: Updating the app loop and handling screen resizing.

- Adding `curses.use_default_colors()` before entering the loop to use the default colors.
- Check if the screen is resized by checking if `stdscr.getch()` returns a `curses.KEY_RESIZE` code.
  - If the screen is resized, called get the updated height and width of the screen.
  - Some terminals emit this when the terminal is resized.
  - Re-check the size (h, w = stdscr.getmaxyx()).
  - If curses.is_term_resized(h, w) says the internal state needs updating, call curses.resizeterm(h, w) so curses recalculates layout/buffers.
  - Use `curses.resizeterm(height, width)` help curses resize to match the terminal.

## Step 3: Calculation the layout.

In this step, we figure out how to calculate the layout of the 'static' windows on the screen.
- We create a simple dataclase to hold the layout information.
- Then we add a clamp function to constrain the values to the range of the screen.
- The compute_layout function takes the screen size and the layout dataclass and returns the layout.
  - The max height and width calcualtion is moved into the compute_layout function.
  - For now, the starting y-position of the windows is hard coded.
  - The height and width of the windows are hard coded.
  - Notice that the heigh of the main window is used to both the size of the main window and the size of the log window.
- The draw_box function draws a box around the window and adds a title.
- The main function is updated to get the layout and draw the windows using the new function.
  - Its import to notice that `noutrefresh()` is called after the layout is computed.
    - This is because the layout is computed before the screen is resized.
    - If we didn't call `noutrefresh()` after the layout is computed, the layout would be incorrect.`
  - Finally, we call `curses.doupdate()` to update the screen.`
    - `doupdate()` is a blocking call that waits for the screen to be updated.
    - This is important because the screen is updated asynchronously.
    - If we don't call `doupdate()` after the layout is computed, the screen would be updated before the layout is computed.
    - This would cause the layout to be incorrect.`

## Step 4: Adding logging to the bottom log window.
In this step we add a log buff class that contains a list of log messages and wrapps text and renders it.
- The core part of `LogBuffer` is in the `render()` method which takes a window and determines it's max size.
- The textwrap module is used to wrap the text inside the window. 
  - Note the heigh calculation is done in the `render()` method to determine where to 
  start displaying the text.  For now new text event are displayed at the bottom.

- The main function is updated to add a log buffer to the layout.
  - The log buffer is updated to add a new log message.
  - We are no longer using the `draw_box` function to draw boxes around the windows. 
    This is handled by the `box()` method of the curses window.

## Step 5: Adding a togglable side window.
In this step we add a side window that can be toggled on and off.
This isn't super remarkable but it lets us experiment with the layout. For now, the main window's
width isn't recalculated when the side window is toggled on or off; but we should do that in the future.
Notable changes in this step:
- A simple placeholder class for the UI state was added to track the state of the side window.
- For now, we've hard coded the width of the side window and created a side panel window.
- A `draw_side` and `draw_main` function were added to add some embelished text to those windows.
- The main function inits the UI state and adds the side window to the layout when `p` is pressed.`

## Step 6: Adding overlays.
In this step `curses.panels` is used to add overlays to the screen.
- A simple placeholder for the overlay state is added to the UI state.
- The new `center_rect` function creates a centered rectangle for the overlay.
- The `draw_overlay` function handles the heavy lifting of creating the overlay.
  - Uses the main window (`stdscr`) to build cords and then create the panel window.
    - Note that the panel window is created with the `new_panel` function. and it is passed a curses window.
  - Adds possible panels to the `cureses.panel`.
  - Uses the familiar draw_box function to draw the box around the overlay.
  - Adds the text to the overlay.
  - Adds the center rect to the overlay.
  - adds the new window to the overlay panel.
- The main function is updated to handle handling the overlay state.
  - Note here that `update_panels()` is called after the layout is computed.
    - This is because the layout is computed before the screen is resized.
    - If we didn't call `update_panels()` after the layout is computed, the layout would be incorrect.`
