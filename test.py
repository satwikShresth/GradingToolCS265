import os
import curses

def selectDirectory(screen):
    # Disable line buffering
    curses.cbreak()

    # Hide the cursor
    curses.curs_set(0)

    # Enable keypad input
    screen.keypad(1)

    # Get the dimensions of the terminal
    height, width = screen.getmaxyx()

    # Create a window to display the directory content
    win = curses.newwin(height, width, 0, 0)

    # Get the current working directory
    path = os.getcwd()

    # List the contents of the directory
    dir_content = os.listdir(path)

    # Initialize the selected item
    selected_item = 0

    # Display the directory contents
    while True:
        win.clear()
        win.addstr(0, 0, "Select a directory:")
        for idx, item in enumerate(dir_content):
            if idx == selected_item:
                win.addstr(idx + 1, 0, "-> " + item)
            else:
                win.addstr(idx + 1, 0, "   " + item)

        # Refresh the screen
        win.refresh()

        # Get the user input
        key = screen.getch()

        # Check if the user pressed an arrow key
        if key == curses.KEY_UP:
            if selected_item > 0:
                selected_item -= 1
        elif key == curses.KEY_DOWN:
            if selected_item < len(dir_content) - 1:
                selected_item += 1
        elif key == curses.KEY_RIGHT:
            # Check if the selected item is a directory
            if os.path.isdir(os.path.join(path, dir_content[selected_item])):
                path = os.path.join(path, dir_content[selected_item])
                os.chdir(path)
                dir_content = os.listdir(path)
                selected_item = 0
        elif key == ord("\n"):
            break
    
    # Deinitialize the screen
    curses.endwin()

    return os.path.join(path, dir_content[selected_item])


screen = curses.initscr()
selected_directory = selectDirectory(screen)
curses.endwin()
print(selected_directory)