import os
import curses
import sys


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

    def _selectDirectory_(self):
        screen = curses.initscr()
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
            

    def refresh(self,win,instructions,selected_item,dir_content):
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
        return idx

    def m_feedbackForm(self,instructions):
        screen = curses.initscr()
        readable_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '\\', '|', ';', ':', '\'', '\"', ',', '.', '<', '>', '/', '?'," "]
        dir_content = ["Add Line","Pop Line","Done"]
        # Disable line buffering
        curses.cbreak()

        # Enable keypad input
        screen.keypad(1)

        # Get the dimensions of the terminal
        height, width = screen.getmaxyx()

        # Create a window to display the directory content
        win = curses.newwin(height, width, 0, 0)
        # Initialize the selected item
        selected_item = 0
        # Display the directory contents

        while True:
            curses.curs_set(0)
            idx = self.refresh(win,instructions,selected_item,dir_content)
            key = screen.getch()

            # Check if the user pressed an arrow key
            if key == curses.KEY_RIGHT or key == curses.KEY_LEFT:
                pass
            elif key == curses.KEY_UP:
                if selected_item > 0:
                    selected_item -= 1
            elif key == curses.KEY_DOWN:
                if selected_item < len(dir_content) - 1:
                    selected_item += 1
            elif key == ord("\n"):
                if len(dir_content) > 3 and not (selected_item+1 > (len(dir_content)-3)):
                    curx=3
                    curses.curs_set(1)
                    while (1): 
                        screen.move(idx+selected_item,curx)
                        c = screen.getch()
                        string = dir_content[selected_item]
                        if c == curses.KEY_LEFT:
                            if curx >3:
                                curx -=1
                        elif c == curses.KEY_RIGHT: 
                            if curx < len(string)+3:
                                curx +=1
                        elif c == curses.KEY_BACKSPACE or c == 127: 
                            if curx >3 and len(string) >= curx-3:
                                curx -=1
                                dir_content[selected_item] = string[:curx-3] + string[curx-3+1:]
                        elif c == ord("\n"):
                            break
                        else:
                            str = chr(c)
                            if str in readable_characters:
                                if curx-3 ==0:
                                    dir_content[selected_item] = str+string
                                else:
                                    dir_content[selected_item] = string[:curx-3] + str + string[curx-3:]
                                curx +=1
                        idx = self.refresh(win,instructions,selected_item,dir_content)
                elif dir_content[selected_item] == dir_content[-3]:
                    dir_content.insert(len(dir_content)-3, "")
                elif dir_content[selected_item] == dir_content[-2] and len(dir_content) >3:
                    dir_content.pop(len(dir_content)-4)
                    selected_item -= 1
                elif dir_content[selected_item] == dir_content[-1]:
                    break

        curses.endwin()

        return dir_content[:-3] if len(dir_content) >3 else None 

    def m_terminalUserInterface(self, options, instructions):
        screen = curses.initscr()
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
