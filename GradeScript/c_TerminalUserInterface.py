import os
import curses


class c_termianlUserInterface():
    #initilizing readable characters and screen
    def __init__(self) -> None:
        curses.initscr();curses.endwin(); # for some reason this helps in avoiding screen freeze
        self.screen = curses.initscr()
        self.idy=0
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.mouseinterval(60)
        self.readable_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '\\', '|', ';', ':', '\'', '\"', ',', '.', '<', '>', '/', '?'," ","\n"]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # This function creates a list of only dir 
    def _refreshContent_(self)->None:
        self.dir_content = [dir for dir in self.dir_content if os.path.isdir(dir)]

    def m_end(self):
        curses.endwin()
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #checks the keystroke if its pointing up or down
    #return true if enter is pressed
    def checkMove(self)->bool:
        if self.key == curses.KEY_MOUSE:
            _,_,_, _, mouse_event = curses.getmouse()
            if mouse_event == 2097152 and self.idy < self.limit +5:
                self.idy+=1
            elif mouse_event == 65536 and self.idy >= 1:
                self.idy-=1
            self.win.addstr(self.idx, 0,str(self.idy))
        elif self.key == curses.KEY_UP:
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
    #creates a list of directory and all user to select one
    def _selectDirectory_(self)->str:
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

        self.screen.clear()
        self.screen.refresh()
        return os.path.join(path, self.dir_content[self.selected_item])
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Puts instruction on the screen to display and options to choose from
    def m_terminalUserInterface(self, options:list[str], instructions:list[str])->str:
        self.m_preReq()
        self.instructions = instructions
        self.dir_content = options
        while True:
            self.m_refresh()

            if(self.checkMove()):
                break

        self.screen.clear()
        self.screen.refresh()
        return self.dir_content[self.selected_item]
    
    def m_checkUnreadable(self,fileContent):
        for i in fileContent:
            if i not in self.readable_characters:
                return False
        return True


    

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #refreshes the screen with new information evertime its called
    def m_refresh(self)-> None:
        self.win.clear()
        self.height, self.width = self.screen.getmaxyx()
        self.win.resize(self.height, self.width)
        self.win.refresh()
        self.idx = 0
        
        try:
            for i, inputString in enumerate(self.instructions):
                self.instructions[i] = "".join([char if char in self.readable_characters else "?" for char in inputString])
        except:
            pass

        self.limit = len(self.instructions)
        for idx,instruction in enumerate(self.instructions):
            if self.idx < self.height//2 and idx >= self.idy:
                self.win.addstr(self.idx, 0, instruction,self.width)
                self.idx += 1

        for idx2, item in enumerate(self.dir_content):
            if idx2 + self.idx <= self.height//2:
                if idx2 == self.selected_item: 
                    self.win.addstr(idx2 + self.idx, 0, "-> " + item)
                else:
                    self.win.addstr(idx2 + self.idx, 0, "   " + item)
            else:
                if idx2 == self.selected_item: 
                    self.win.addstr(idx2+ (self.height//2 -2), 0, "-> " + item)
                else:
                    self.win.addstr(idx2+ (self.height//2-2), 0, "   " + item)

        # Refresh the screen
        self.win.refresh()
        self.key = self.screen.getch()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #initlizes values
    def m_preReq(self)->None:
        self.idy=0
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(1)
        self.height, self.width = self.screen.getmaxyx()
        self.win = curses.newwin(self.height, self.width, 0, 0)
        self.selected_item = 0

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #creates a interface for user to add comments
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
                            if str in self.readable_characters and len(string) < (self.width-5):
                                if curx-3 == 0:
                                    self.dir_content[self.selected_item] = str+string
                                else :
                                    self.dir_content[self.selected_item] = string[:curx-3] + str + string[curx-3:]
                                curx +=1
                elif self.dir_content[self.selected_item] == self.dir_content[-3]:
                    self.dir_content.insert(len(self.dir_content)-3, "")
                elif self.dir_content[self.selected_item] == self.dir_content[-2] and len(self.dir_content) >3:
                    self.dir_content.pop(len(self.dir_content)-4)
                    self.selected_item -= 1
                elif self.dir_content[self.selected_item] == self.dir_content[-1]:
                    break

        self.screen.clear()
        self.screen.refresh()

        return self.dir_content[:-3] if len(self.dir_content) >3 else None 

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

