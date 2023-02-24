import curses

# Initialize curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.mousemask(curses.ALL_MOUSE_EVENTS)

# Set mouse interval to a low value
curses.mouseinterval(1)

# Wait for a key press or mouse event
while True:
    ch = stdscr.getch()
    if ch == ord('q'):
        break
    elif ch == curses.KEY_MOUSE:
        _, x, y, _, mouse_event = curses.getmouse()
        stdscr.addstr(0, 0, str(mouse_event))
        stdscr.refresh()

# Clean up curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()


2097152
65536