import os
import curses


class c_termianlUserInterface():
    def __init__(self) -> None:
        pass

    def _preReq_(self, screen):
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

        return win

    def _refreshContent_(self, dir_content):
        return [dir for dir in dir_content if os.path.isdir(dir)]

    def _selectDirectory_(self, screen):

        win = self._preReq_(screen)
        # Get the current working directory
        path = os.getcwd()

        # List the contents of the directory
        dir_content = self._refreshContent_(os.listdir(path))
        # Initialize the selected item
        selected_item = 0

        # Display the directory contents
        while True:
            win.clear()
            win.addstr(0, 1, "Select the directory of the assignment:")
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
                    dir_content = self._refreshContent_(os.listdir(path))
                    selected_item = 0
            elif key == curses.KEY_LEFT:
                newPath = '/'.join(path.split("/")[:-1])
                if os.path.isdir(newPath):
                    path = newPath
                    os.chdir(path)
                    dir_content = self._refreshContent_(os.listdir(path))
                    selected_item = 0
            elif key == ord("\n"):
                break
            elif key == ord("q"):
                curses.endwin()
                return "q"

        # Deinitialize the screen
        curses.endwin()

        return os.path.join(path, dir_content[selected_item])

    def m_terminalUserInterface(self, screen, options, instructions):
        win = self._preReq_(screen)
        dir_content = options
        # Initialize the selected item
        selected_item = 0
        # Display the directory contents
        while True:
            win.clear()

            idx = 0
            for instruction in instructions:
                win.addstr(idx, 0, instruction)
                idx += 1

            for idx2, item in enumerate(dir_content):
                if idx2 == selected_item:
                    win.addstr(idx2 + idx, 0, "-> " + item)
                else:
                    win.addstr(idx2 + idx, 0, "   " + item)

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
            elif key == ord("\n"):
                break

        # Deinitialize the screen
        curses.endwin()

        return dir_content[selected_item]
