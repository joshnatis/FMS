#==========================================================================#
# This program is courtesy of minigrammer:                                 #
# https://github.com/mingrammer/python-curses-scroll-example               #
# LICENSE: MIT                                                             #
#                                                                          #
# I use this in the Food Management System CLI to display data that may be #
# larger than the size of the window -- specifically, to display a list of #
# users in display_main(), and to display data in display_data()           #
#==========================================================================#

import curses
import curses.textpad


class Screen(object):
    UP = -1
    DOWN = 1

    def __init__(self, items, win, dims, selectable=False):
        """ Initialize the screen window
        Attributes
            window: A full curses screen window
            width: The width of `window`
            height: The height of `window`
            max_lines: Maximum visible line count for `result_window`
            top: Available top line position for current page (used on scrolling)
            bottom: Available bottom line position for whole pages (as length of items)
            current: Current highlighted line number (as window cursor)
            page: Total page count which being changed corresponding to result of a query (starts from 0)
            ┌--------------------------------------┐
            |1. Item                               |
            |--------------------------------------| <- top = 1
            |2. Item                               |
            |3. Item                               |
            |4./Item///////////////////////////////| <- current = 3
            |5. Item                               |
            |6. Item                               |
            |7. Item                               |
            |8. Item                               | <- max_lines = 7
            |--------------------------------------|
            |9. Item                               |
            |10. Item                              | <- bottom = 10
            |                                      |
            |                                      | <- page = 1 (0 and 1)
            └--------------------------------------┘
        Returns
            None
        """
        self.nlines, self.ncols, self.begin_y, self.begin_x = dims
        self.selectable = selectable
        self.window = win

        self.width = 0
        self.height = 0

        self.init_curses()

        self.items = items

        self.max_lines = self.nlines
        self.top = 0
        self.bottom = len(self.items)
        self.current = 0
        self.page = self.bottom // self.max_lines

    def init_curses(self):
        """Setup the curses"""
        self.window.keypad(True)
        curses.curs_set(0)
        self.current = curses.color_pair(1)
        self.height, self.width = self.nlines, self.ncols
        self.window.box()
        self.window.refresh()

    def run(self):
        """Continue running the TUI until get interrupted"""
        choice = self.input_stream()
        return choice

    def input_stream(self):
        """Waiting an input and run a proper method according to type of input"""
        chosen = 0
        while True:
            self.display()

            ch = self.window.getch()
            if ch == curses.KEY_UP:
                if chosen != 0: chosen -= 1
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                if chosen != len(self.items) - 1: chosen += 1
                self.scroll(self.DOWN)

            elif not self.selectable and ch == curses.KEY_LEFT:
                self.paging(self.UP)
            elif not self.selectable and ch == curses.KEY_RIGHT:
                self.paging(self.DOWN)

            elif ch == curses.ascii.ESC or ch == 10:
                return self.items[chosen]
                break

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return
        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return

    def paging(self, direction):
        """Paging the window when pressing left/right arrow keys"""
        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction
        # The last page may have fewer items than max lines,
        # so we should adjust the current cursor position as maximum item count on last page
        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)

        # Page up
        # if current page is not a first page, page up is possible
        # top position can not be negative, so if top position is going to be negative, we should set it as 0
        if (direction == self.UP) and (current_page > 0):
            self.top = max(0, self.top - self.max_lines)
            return
        # Page down
        # if current page is not a last page, page down is possible
        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return

    def display(self):
        """Display the items on window"""
        self.window.erase()
        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines]):
            # Highlight the current cursor line
            if idx == self.current:
                self.window.addstr(idx, 0, item, curses.color_pair(1))
            else:
                self.window.addstr(idx, 0, item, curses.color_pair(3))
        self.window.refresh()

