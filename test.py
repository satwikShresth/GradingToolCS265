import curses

# Initialize curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

# Get screen dimensions
max_y, max_x = stdscr.getmaxyx()

# Create two windows side by side
window1 = curses.newwin(max_y//2, max_x, 0, 0)
window2 = curses.newwin(max_y//2, max_x, max_y//2, 0)

# Add some text to each window
while(1):
    window1.addstr(0, 0, "This is window 1")
    window2.addstr(0, 0, "This is window 2")
    window1.refresh()
    window2.refresh()



# Refresh the windows to show the changes
window1.refresh()
window2.refresh()

# Wait for a key press
stdscr.getch()

# Clean up curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()