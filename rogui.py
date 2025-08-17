#!/usr/bin/env python3

import curses
from dataclasses import dataclass


@dataclass
class Rect:
    y: int
    x: int
    h: int
    w: int

    def printable_width(self):
        return self.w - 1


def clamp(val, min_val, max_val):
    """Clamp a value between min_val and max_val"""
    return max(min_val, min(val, max_val))


def compute_layout(stdscr):
    """Compute the layout of all the windows in the main screen"""
    heigh, width = stdscr.getmaxyx()
    top_height = 1
    log_height = clamp(heigh - 5, 3, 7)
    body_height = max(3, heigh - top_height - log_height)

    top_r = Rect(0, 0, top_height, width)
    main_r = Rect(top_height, 0, body_height, width)
    log_r = Rect(top_height + body_height, 0, log_height, width)
    return top_r, main_r, log_r


def draw_box(win, title=None):
    """Draw a box around a window"""
    win.box()
    if title:
        h, w = win.getmaxyx()
        label = f" {title} "
        x = max(1, (w - len(label)) // 2)
        try:
            win.addstr(0, x, label, curses.A_BOLD)
        except curses.error:
            raise


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    # let the terminal background color be what we see
    curses.use_default_colors()

    while True:
        top_rect, main_rect, log_rect = compute_layout(stdscr)
        # top bar on stdscr
        stdscr.erase()
        stdscr.addnstr(0, 0, "q:quit", top_rect.printable_width(), curses.A_REVERSE)

        # Creating windows
        main_win = curses.newwin(main_rect.h, main_rect.w, main_rect.y, main_rect.x)
        log_win = curses.newwin(log_rect.h, log_rect.w, log_rect.y, log_rect.x)

        draw_box(main_win, "Main")
        draw_box(log_win, "Log")

        # flushing
        stdscr.noutrefresh()
        main_win.noutrefresh()
        log_win.noutrefresh()
        curses.doupdate()

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
