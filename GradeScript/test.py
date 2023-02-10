#!/usr/bin/env python3
import curses
from pygments import highlight

def delete_char(string):
    if curx:
      curx -= 1
      del string[curx]
    elif curx == 0 and cury:
      oldline = string[curx:]
      del string
      cury -= 1
      curx = len(string)
      string += oldline
      total_lines -= 1
    modified += 1

    
  
def move_cursor(key,curx,string):
    row = string
    if key == curses.KEY_LEFT:
      if curx != 4: curx -= 1
    elif key == curses.KEY_RIGHT:
      if row is not None and curx < len(row):
        curx += 1
      elif row is not None and curx == len(row):
        curx = 4
    row = string
    rowlen = len(row) if row is not None else 4
    if curx > rowlen: curx = rowlen
    return curx


def refresh(win,instructions,selected_item,dir_content):
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


def m_feedbackForm(screen,instructions):

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
        idx = refresh(win,instructions,selected_item,dir_content)
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
                    idx = refresh(win,instructions,selected_item,dir_content)
            elif dir_content[selected_item] == dir_content[-3]:
                dir_content.insert(len(dir_content)-3, "")
            elif dir_content[selected_item] == dir_content[-2] and len(dir_content) >3:
                dir_content.pop(len(dir_content)-4)
                selected_item -= 1
            elif dir_content[selected_item] == dir_content[-1]:
                break

    curses.endwin()

    return dir_content[selected_item]

def main():
    curses.initscr()
    curses.endwin()
    screen = curses.initscr()
    with open("testSplit.c","r") as file:
        n = file.readlines()
    selectedData = m_feedbackForm(screen,n)
    print(selectedData)


if __name__ == "__main__":
    main()