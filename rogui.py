#!/usr/bin/env python3

import curses
import textwrap
from collections import deque
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


class LogBuffer:
    def __init__(self, capacity=500):
        self.lines = deque(maxlen=capacity)

    def add(self, msg):
        self.lines.append(msg)

    def render(self, win):
        win.erase()
        h, w = win.getmaxyx()
        # draw a box around the window
        win.box()
        try:
            win.addstr(0, 2, "Log", curses.A_BOLD)
        except curses.error:
            pass

        inner_h = h - 2
        start = max(0, len(self.lines) - inner_h)
        y = 1
        for line in list(self.lines)[start:]:
            for wrapped in textwrap.wrap(line, width=w - 2):
                if y >= h - 1:
                    return
                try:
                    win.addnstr(y, 1, wrapped, w - 2)
                except curses.error:
                    pass
                y += 1


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
    curses.use_default_colors()  # let the terminal background color be what we see
    log = LogBuffer(1000)
    message = "Welcome to the curses GUI: press q to quit, g:add to log"
    log.add(message)

    while True:
        top_rect, main_rect, log_rect = compute_layout(stdscr)
        # top bar on stdscr
        stdscr.erase()
        stdscr.addnstr(0, 0, "q:quit g:add log", top_rect.printable_width(), curses.A_REVERSE)

        # Creating windows
        main_win = curses.newwin(main_rect.h, main_rect.w, main_rect.y, main_rect.x)
        main_win.box()
        try:
            main_win.addstr(0, 2, "Main", curses.A_BOLD)
        except curses.error:
            pass

        log_win = curses.newwin(log_rect.h, log_rect.w, log_rect.y, log_rect.x)
        log.render(log_win)

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
        if ch in (ord('g'), ord('G')):
            h, w = stdscr.getmaxyx()
            log.add(f"TICK: terminal is: {h}*{w}")
            continue

if __name__ == '__main__':
    curses.wrapper(main)
