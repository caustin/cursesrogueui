#!/usr/bin/env python3

import curses

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    # let the terminal background color be what we see
    curses.use_default_colors()

    while True:
        h, w = stdscr.getmaxyx()

        stdscr.erase()

        msg = "hello curse.  Press q to quit. Resize the terminal."
        size = f"terminal size (W*H): {w} x {h}"
        stdscr.addnstr(0, 0, msg, w-1, curses.A_BOLD)
        stdscr.addnstr(1, 0, size, w-1)
        stdscr.refresh()

        ch = stdscr.getch()
        if ch == curses.KEY_RESIZE:
            # some terminals send KEY_RESIZE when the terminal is resized,
            # and this is needed to nudge the terminal into updating the internal buffers
            h, w = stdscr.getmaxyx()
            if curses.is_term_resized(h, w):
                curses.resizeterm(h, w)
            continue

        if ch in (ord('q'), ord('Q')):
            break

if __name__ == '__main__':
    curses.wrapper(main)
