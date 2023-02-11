import os
import curses


class c_termianlUserInterface():
    def __init__(self) -> None:
        curses.initscr();curses.endwin();
        self.screen = curses.initscr()
        self.readable_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '\\', '|', ';', ':', '\'', '\"', ',', '.', '<', '>', '/', '?'," "]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def _refreshContent_(self):
        self.dir_content = [dir for dir in self.dir_content if os.path.isdir(dir)]

    def checkMove(self):
        if self.key == curses.KEY_UP:
            if self.selected_item > 0:
                self.selected_item -= 1
            elif self.selected_item == 0:
                self.selected_item = len(self.dir_content)-1
        elif self.key == curses.KEY_DOWN:
            if self.selected_item < len(self.dir_content) - 1:
                self.selected_item += 1
            elif self.selected_item == len(self.dir_content) - 1:
                self.selected_item = 0
        elif self.key == ord("\n"):
            return True
        return False

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def _selectDirectory_(self):
        self.m_preReq()
        path = os.getcwd()
        self.dir_content = os.listdir(path)
        self._refreshContent_()
        self.instructions = ["Select the directory of the assignment:"]
        self.dirHistory={}
        while True:
            self.m_refresh()
            pList = path.split("/")

            if(self.checkMove()):
                break
            elif self.key == curses.KEY_RIGHT:
                # Check if the selected item is a directory
                if os.path.isdir(os.path.join(path, self.dir_content[self.selected_item])):
                    self.dirHistory[path]=self.selected_item
                    path = os.path.join(path, self.dir_content[self.selected_item])
                    os.chdir(path)
                    self.dir_content = os.listdir(path)
                    self._refreshContent_()
                    self.selected_item = self.selected_item = self.dirHistory[path] if path in self.dirHistory else 0
            elif self.key == curses.KEY_LEFT:
                if len(pList) > 3:
                    newPath = '/'.join(pList[:-1])
                    if os.path.isdir(newPath):
                        self.dirHistory[path]=self.selected_item
                        path = newPath
                        os.chdir(path)
                        self.dir_content = os.listdir(path)
                        self._refreshContent_()
                        self.selected_item = self.dirHistory[path] if path in self.dirHistory else self.dir_content.index(pList[-1])
            elif self.key == ord("q"):
                return "q"

        return os.path.join(path, self.dir_content[self.selected_item])

    def m_terminalUserInterface(self, options, instructions):

        self.m_preReq()
        self.instructions = instructions
        self.dir_content = options
        while True:
            self.m_refresh()

            if(self.checkMove()):
                break

        return self.dir_content[self.selected_item]
            
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_refresh(self):
        self.win.clear()
        self.idx = 0
        for instruction in self.instructions:
            self.win.addstr(self.idx, 0, instruction)
            self.idx += 1
        
        for idx2, item in enumerate(self.dir_content):
            if idx2 == self.selected_item:
                self.win.addstr(idx2 + self.idx, 0, "-> " + item)
            else:
                self.win.addstr(idx2 + self.idx, 0, "   " + item)

        # Refresh the screen
        self.win.refresh()
        self.key = self.screen.getch()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_preReq(self):
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(1)
        self.height, self.width = self.screen.getmaxyx()
        self.win = curses.newwin(self.height, self.width, 0, 0)
        self.selected_item = 0

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_feedbackForm(self,instructions):
        self.m_preReq()
        self.dir_content = ["Add Line","Pop Line","Done"]
        self.instructions = instructions
        while True:
            curses.curs_set(0)
            self.m_refresh()

            if(self.checkMove()):
                if len(self.dir_content) > 3 and not (self.selected_item+1 > (len(self.dir_content)-3)):
                    curx=3
                    curses.curs_set(1)
                    while (1): 
                        self.screen.move(self.idx+self.selected_item,curx)
                        self.m_refresh()
                        string = self.dir_content[self.selected_item]
                        if self.key == curses.KEY_LEFT:
                            if curx >3:
                                curx -=1
                        elif self.key == curses.KEY_RIGHT: 
                            if curx < len(string)+3:
                                curx +=1
                        elif self.key == curses.KEY_BACKSPACE or self.key == 127: 
                            if curx >3 and len(string) >= curx-3:
                                curx -=1
                                self.dir_content[self.selected_item] = string[:curx-3] + string[curx-3+1:]
                        elif self.key == ord("\n"):
                            break
                        else:
                            str = chr(self.key)
                            if str in self.readable_characters:
                                if curx-3 == 0:
                                    self.dir_content[self.selected_item] = str+string
                                elif len(string) < (self.width-3):
                                    self.dir_content[self.selected_item] = string[:curx-3] + str + string[curx-3:]
                                curx +=1
                elif self.dir_content[self.selected_item] == self.dir_content[-3]:
                    self.dir_content.insert(len(self.dir_content)-3, "")
                elif self.dir_content[self.selected_item] == self.dir_content[-2] and len(self.dir_content) >3:
                    self.dir_content.pop(len(self.dir_content)-4)
                    self.selected_item -= 1
                elif self.dir_content[self.selected_item] == self.dir_content[-1]:
                    break

        return self.dir_content[:-3] if len(self.dir_content) >3 else None 


