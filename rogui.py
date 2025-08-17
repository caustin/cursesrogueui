import curses

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    while True:
        h, w = stdscr.getmaxyx()

        stdscr.erase()

        msg = "hello curse.  Press q to quit."
        size = f"terminal size (W*H): {w}x{h}"
        stdscr.addnstr(0, 0, msg, w-1, curses.A_BOLD)
        stdscr.addnstr(1, 0, size, w-1)
        stdscr.refresh()

        ch = stdscr.getch()
        if ch in (ord('q'), ord('Q')):
            break

if __name__ == '__main__':
    curses.wrapper(main)
