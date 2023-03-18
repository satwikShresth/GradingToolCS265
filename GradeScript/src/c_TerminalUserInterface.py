import curses,os
from .c_Grader import permission

class c_termianlUserInterface():
    #initilizing readable characters and screen
    def __init__(self) -> None:
        curses.initscr();curses.endwin(); # for some reason this helps in avoiding screen freeze
        self.screen = curses.initscr()
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.mouseinterval(60)
        curses.curs_set(0)
        self.screen.idlok(False)
        self.screen.idcok(False)
        self.stringEditMode = False
        self.readable_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '\\', '|', ';', ':', '\'', '\"', ',', '.', '<', '>', '/', '?'," ","\n"]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # This function creates a list of only dir 
    def _refreshContent_(self)->None:
        self.dir_content = [dir for dir in self.dir_content if os.path.isdir(dir) or dir.endswith("json")]

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def m_end(self):
        curses.endwin()
        
    def m_restart(self):
        self.screen = curses.initscr()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def m_selectStudents(self,listOfStudents,gradedStudent)->bool:
        self.m_preReq()
        sep1 = "-"*39
        sep2= "-"*8
        self.instructions=[f"Name{'':35} {'':3}Grade",f"{sep1} {sep2}"]
        self.content = []
        for name,student in listOfStudents.items():
            if name in gradedStudent:
                self.content += [f'{student.s_fullname:<39} {student.f_grade:<8}']
            else:
                self.content += [f'{student.s_fullname:<39} {"Pending":<8}']
        while True:
            self.dir_content = ["Search"] + self.content
            curses.curs_set(0)
            self.m_mrefresh()

            if(self.checkMove()):
                if self.dir_content[self.selected_item] == self.dir_content[0]:
                    self.dir_content[self.selected_item] = ""
                    curx=3
                    curses.curs_set(1)
                    while (1): 
                        self.screen.move(self.idx+self.selected_item,curx)
                        self.m_mrefresh()
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
                        del self.dir_content[1::]
                        for name,student in listOfStudents.items():
                            if self.dir_content[self.selected_item] in student.s_fullname:
                                if name in gradedStudent:
                                    self.content += [f'{student.s_fullname:<39} {student.f_grade:<8}']
                                else:
                                    self.content += [f'{student.s_fullname:<39} {"Pending":<8}']
                    curses.curs_set(0)
                else:
                    break

        self.screen.erase()
        self.screen.refresh()
        curses.endwin()
        
        return list(listOfStudents.keys())[self.selected_item-1]


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def m_selectGraders(self,ListOfGraders):
        self.m_preReq()
        sep1 = "-"*39
        sep2= "-"*8
        self.instructions=[f"Name{'':35} {'':3}Grade",f"{sep1} {sep2}"]
        self.content = []
        for name,obj in ListOfGraders.items():
            display = f'{obj.name} ({obj.username})'
            if obj.status != permission.REQUESTED:
                status = "Active" if obj.status == permission.GRANTED else "Denied"
                self.instructions += [f'{ (obj.username):<39} {status:<8}']
            else:
                self.content += [f'{display:<39} {"Requested":<8}']
        while True:
            self.dir_content = ["Search"] + self.content
            curses.curs_set(0)
            self.m_mrefresh()

            if(self.checkMove()):
                if self.dir_content[self.selected_item] == self.dir_content[0]:
                    self.dir_content[self.selected_item] = ""
                    curx=3
                    curses.curs_set(1)
                    while (1): 
                        self.screen.move(self.idx+self.selected_item,curx)
                        self.m_mrefresh()
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
                        del self.dir_content[1::]
                        for name,obj in ListOfGraders.items():
                            display = f'{obj.name} ({obj.username})'
                            if self.dir_content[self.selected_item] in display:
                                if obj.status != permission.REQUESTED:
                                    status = "Active" if obj.status == permission.GRANTED else "Denied"
                                    self.instructions += [f'{ (obj.username):<39} {status:<8}']
                                else:
                                    self.content += [f'{display:<39} {"Requested":<8}']
                    curses.curs_set(0)
                else:
                    break

        self.screen.erase()
        self.screen.refresh()
        curses.endwin()
        
        return list(ListOfGraders.values())[self.selected_item-1]


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #checks the keystroke if its pointing up or down
    #return true if enter is pressed
    def checkMove(self)->bool:
        if self.key == curses.KEY_MOUSE:
            _,_,_, _, mouse_event = curses.getmouse()
            if mouse_event == 2097152 and self.idy < self.limit:
                self.idy+=1
            elif mouse_event == 65536 and self.idy >= 1:
                self.idy-=1
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
        self.instructions = ["<-,-> arrow keys to move in and out of the dir","enter to select"]
        self.static = ["Select the Json File:"]
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

        self.screen.erase()
        self.screen.refresh()
        return os.path.join(path, self.dir_content[self.selected_item])
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Puts instruction on the screen to display and options to choose from
    def m_terminalUserInterface(self, options:list[str], instructions:list[str])->str:
        self.m_preReq()
        self.instructions = instructions[:-1]
        self.dir_content = options
        self.static = [instructions[-1]]
        try:
            for i, inputString in enumerate(self.instructions):
                self.instructions[i] = "".join([char if char in self.readable_characters else "?" for char in inputString])
        except:
            pass
        while True:
            self.m_refresh()

            if(self.checkMove()):
                break

        self.screen.erase()
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
        self.win.erase()
        self.height, self.width = self.screen.getmaxyx()
        self.win.resize(self.height, self.width)
        self.win.noutrefresh()
        curses.doupdate()
        self.idx = 0
        local_idx = 0
        

        self.limit = len(self.instructions) -  self.height//2 +1
        for idx,instruction in enumerate(self.instructions):
            if self.idx < self.height//2-1 and idx >= self.idy:
                self.win.addstr(self.idx, 0, instruction,self.width)
                self.idx += 1
            elif self.idx >= self.height//2-1:
                break

        if self.idx > self.height//2:
            self.idx = self.height//2

        self.win.addstr(self.idx, 0, "-"*self.width,self.width)
        self.idx+=1
        try:
            for idx, item in enumerate(self.static):
                self.win.addstr(self.idx+idx, 0,item)
                self.idx+=1
        except:
            self.win.addstr(self.idx+idx, 0,"error")
            self.idx+=1

        self.win.addstr(self.idx, 0, "-"*self.width,self.width)
        self.idx+=1


        for idx2, item in enumerate(self.dir_content):
            if idx2 == self.selected_item:
                self.win.addstr(idx2 + self.idx, 0,item +str(" "*(self.width-len(item))),curses.A_REVERSE)
            else:
                if os.path.isfile(item):
                    self.win.addstr(idx2 + self.idx, 0,item +str(" "*(self.width-len(item))),curses.A_BOLD)
                else:
                    self.win.addstr(idx2 + self.idx, 0,item +str(" "*(self.width-len(item))))

        # Refresh the screen
        self.win.noutrefresh()
        curses.doupdate()
        self.key = self.screen.getch()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #refreshes the screen with new information evertime its called
    def m_feedbackRefresh(self)-> None:
        # self.win.erase()
        self.height, self.width = self.screen.getmaxyx()
        self.win.resize(self.height, self.width)
        self.displayWin.resize(self.height//2,self.width)
        self.menuWin.resize(self.height//2,self.width)
        self.win.noutrefresh()
        curses.doupdate()
        self.displayWin.refresh()
        self.menuWin.refresh()
        self.idx = 0
        local_idx=0
        static = 0
        
        self.limit = len(self.instructions) -  self.height//2 +2
        for idx,instruction in enumerate(self.instructions):
            if self.idx < self.height//2 -2 and idx >= self.idy:
                self.displayWin.addstr(self.idx, 0, instruction+str(" "*(self.width-len(instruction))),self.width)
                self.idx += 1
            elif self.idx >= self.height//2-2:
                break

        self.displayWin.addstr(self.height//2 -2, 0, "-"*self.width,self.width)

        for idx, item in enumerate(self.static):
            self.menuWin.addstr(idx, 0,item+str(" "*(self.width-len(item))))
            local_idx+=1

        self.menuWin.addstr(local_idx, 0, "-"*self.width,self.width)
        local_idx+=1

        for idx2, item in enumerate(self.dir_content):
            if idx2 == self.selected_item:
                if len(self.dir_content)>3 and idx2<len(self.dir_content)-3:
                    if self.stringEditMode:
                        self.menuWin.addstr(idx2 +local_idx, 0,item +str(" "*(self.width-len(item))))
                    else:
                        self.menuWin.addstr(idx2 +local_idx, 0,"* " + item +str(" "*(self.width-len(item))),curses.A_REVERSE)
                else:
                    self.menuWin.addstr(idx2+ local_idx, 0,item+str(" "*(self.width-len(item))),curses.A_REVERSE)
            elif len(self.dir_content)>3 and idx2<len(self.dir_content)-3 and len(item)!=0:
                self.menuWin.addstr(idx2+local_idx, 0,"* "+ item +str(" "*(self.width-len(item))))
            else:
                self.menuWin.addstr(idx2+local_idx, 0,item +str(" "*(self.width-len(item))))


        # Refresh the screen
        self.win.noutrefresh()
        curses.doupdate()
        self.displayWin.refresh()
        self.menuWin.refresh()
        self.key = self.screen.getch()


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #refreshes the screen with new information evertime its called
    def m_mrefresh(self)-> None:
        # self.win.erase()
        self.height, self.width = self.screen.getmaxyx()
        self.win.resize(self.height, self.width)
        self.win.noutrefresh()
        curses.doupdate()
        self.idx = 0

        self.limit = len(self.instructions) + len(self.dir_content)
        for instruction in self.instructions:
            self.win.addstr(self.idx, 0, instruction,self.width)
            self.idx += 1

        for idx2, item in enumerate(self.dir_content):
            if idx2 + self.idx < self.height:
                if idx2 == self.selected_item: 
                    self.win.addstr(idx2 + self.idx, 0,item+str(" "*(self.width-len(item))),curses.A_REVERSE)
                else:
                    self.win.addstr(idx2 + self.idx, 0,item,)

        # Refresh the screen
        self.win.noutrefresh()
        curses.doupdate()
        self.key = self.screen.getch()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #initlizes values
    def m_preReq(self)->None:
        self.idy=0
        self.limit = 0
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
        self.displayWin = self.win.subwin(self.height//2,self.width,0,0)
        self.menuWin = self.win.subwin(self.height//2,self.width,self.height//2-1,0)
        try:
            for i, inputString in enumerate(self.instructions):
                self.instructions[i] = "".join([char if char in self.readable_characters else "?" for char in inputString])
        except:
            pass
        for i, inputString in enumerate(self.instructions):
                if "Feedback:" in inputString:
                    self.static = self.instructions[i::]
                    self.instructions = self.instructions[0:i]
        while True:
            curses.curs_set(0)
            self.m_feedbackRefresh()
            if(self.checkMove()):
                if len(self.dir_content) > 3 and not (self.selected_item+1 > (len(self.dir_content)-3)):
                    curx=0
                    curses.curs_set(1)
                    while (1):
                        self.stringEditMode = True 
                        self.screen.move(self.idx+2+len(self.static)+self.selected_item,curx)
                        self.m_feedbackRefresh()
                        string = self.dir_content[self.selected_item]
                        if self.key == curses.KEY_LEFT:
                            if curx >0:
                                curx -=1
                        elif self.key == curses.KEY_RIGHT: 
                            if curx < len(string):
                                curx +=1
                        elif self.key == curses.KEY_BACKSPACE or self.key == 127: 
                            if curx >0 and len(string) >= curx:
                                curx -=1
                                self.dir_content[self.selected_item] = string[:curx] + string[curx+1:]
                        elif self.key == ord("\n"):
                            break
                        else:
                            str = chr(self.key)
                            if str in self.readable_characters and len(string) < (self.width-2):
                                if curx == 0:
                                    self.dir_content[self.selected_item] = str+string
                                else :
                                    self.dir_content[self.selected_item] = string[:curx] + str + string[curx:]
                                curx +=1
                    curses.curs_set(0)
                    self.stringEditMode = False
                elif self.dir_content[self.selected_item] == self.dir_content[-3]:
                    self.dir_content.insert(len(self.dir_content)-3, "")
                elif self.dir_content[self.selected_item] == self.dir_content[-2] and len(self.dir_content) >3:
                    self.dir_content.pop(len(self.dir_content)-4)
                    self.selected_item -= 1
                elif self.dir_content[self.selected_item] == self.dir_content[-1]:
                    break

        self.screen.erase()
        self.screen.refresh()

        return self.dir_content[:-3] if len(self.dir_content) >3 else None 

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

