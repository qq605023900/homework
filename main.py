import random
from tkinter import *
from copy import deepcopy
import tkinter.messagebox as messagebox

#==========================school class=============================== 
class Major(object):
    def __init__(self, MajorCode, MajorName, MajorNum, MajorLess):
        self.MajorCode = MajorCode
        self.MajorName = MajorName       
        self.MajorNum = MajorNum
        self.MajorLess = MajorLess
        self.mates = []

    def add(self, student):
        self.mates.append(student)
        self.MajorLess -= 1
    
    def pop(self):
        self.mates.sort()
        self.MajorLess += 1
        return self.mates.pop(0)
    
    def isNotFull(self):
        if self.MajorLess == 0:
            return False
        else:
            return True

class SchIfo(object):
    def __init__(self, schCode, schName):
        self.schCode = schCode
        self.schName = schName
        self.major = []
    
    def addMajor(self, MajorCode, MajorName, MajorNum, MajorLess):
        self.major.append(Major(MajorCode, MajorName, MajorNum, MajorLess))
    
    def setFullMajor(self, fullmajor):
        self.major = fullmajor
#====================================student class====================
class StuIfo(object):
    def __init__(self, name, age, snum, sex, isAdjust):
        self.name = name
        self.age = age
        self.snum = snum
        self.sex = sex
        self.scores = {}
        self.will = []
        self.schoolwill = 1049
        self.isAdmit = False
        self.isAdjust = isAdjust

    #操作符重载... :)
    def __lt__(self, other):#operator <     
        return self.scores['total'] < other.scores['total'] 

    def __ge__(self,other):#oprator >= 
        return self.scores['total'] >= other.scores['total'] 
    
    def __le__(self,other):#oprator <= 
        return self.scores['total'] <= other.scores['total']   

    def addWill(self, will):
        self.will.append(will)
    
    def setFullscore(self, fullscore):
        self.scores = fullscore
    
    def getWill(self, i):
        return self.will[i]
    
    def strIfo(self):
        tmpinf = []
        tmpinf.append(str(self.snum))
        tmpinf.append(self.name)
        tmpinf.append(str('%s' %self.age))
        tmpinf.append(self.sex)
        tmpinf.append(self.isAdjust)
        for key in self.scores:
            tmpinf.append('%s' %(self.scores[key]))
        tmpinf.append('  '.join('%s' %id for id in self.will))
        return tmpinf           
#==========================myheap class=============================
class MaxHeap(object): 
    def __init__(self): 
        self._data = [] 
        self._count = len(self._data) 

    def size(self): 
        return self._count 

    def add(self, item): # 插入元素入堆 
        self._data.append(item) 
        self._count += 1 
        self._shiftup(self._count-1) 
        
    def pop(self): # 出堆 
        if self._count > 0: 
            ret = self._data[0] 
            self._data[0] = self._data[self._count-1] 
            self._data.pop()
            self._count -= 1 
            self._shiftDown(0) 
            return ret 
    
    def _shiftup(self, index): # 上移self._data[index]，以使它不大于父节点 
        parent = (index-1)>>1
        while index > 0 and self._data[parent] < self._data[index]: 
            # swap 
            self._data[parent], self._data[index] = self._data[index], self._data[parent] 
            index = parent 
            parent = (index-1)>>1 
    
    def _shiftDown(self, index): # xia移self._data[index]，以使它不小于子节点 
        j = (index << 1) + 1 
        while j < self._count : 
            # 有子节点 
            if j+1 < self._count and self._data[j+1] > self._data[j]: 
                # 有右子节点，并且右子节点较大 
                j += 1 
            if self._data[index] >= self._data[j]: # 堆的索引位置已经大于两个子节点，不需要交换了 
                break 
            self._data[index], self._data[j] = self._data[j], self._data[index] 
            index = j 
            j = (index << 1) + 1 
#=========================strategy mode=============================
class AdmitStrategy(object):
    #录取策略
    def admit(self):
        pass

class bjutAdmit(AdmitStrategy):
    #分数优先，遵循志愿
    def admit(self):
        for major in bjut.major:
            major.mates = []
            major.MajorLess = major.MajorNum
        while tmpHeap.size() > 0:
            tmpHeap.pop()
        for student in myClass:
            tmpHeap.add(deepcopy(student))
        while retireHeap.size() > 0:
            retireHeap.pop()
        while retryHeap.size() > 0:
            retryHeap.pop()

        admitNum = 0
        for major in bjut.major:
            #计数
            admitNum += major.MajorNum 
        while admitNum > 0 and tmpHeap.size() > 0:
            tmpStu = tmpHeap.pop()
            tmpWill = []
            for will in tmpStu.will:
                tmpWill.append(will)
            while tmpStu.isAdmit is False: 
                if len(tmpWill) == 0:
                    #所报志愿均满员
                    if tmpStu.isAdjust == 'yes':#服从调剂进入调剂堆
                        retryHeap.add(tmpStu)
                        break
                    else:#不服从则退档
                        retireHeap.add(tmpStu)
                        break
                else:           
                    op = tmpWill.pop(0)
                    
                    for major in bjut.major:
                        if op == major.MajorCode and major.isNotFull():
                            tmpStu.isAdmit = True
                            major.add(tmpStu)
                            admitNum -= 1
        while tmpHeap.size() > 0:#整合退档学生
            retireHeap.add(tmpStu.pop())

class scuAdmit(AdmitStrategy):
    #专业级差
    def admit(self):
        for major in bjut.major:
            major.mates = []
            major.MajorLess = major.MajorNum
        while tmpHeap.size() > 0:
            tmpHeap.pop()
        for student in myClass:
            tmpHeap.add(deepcopy(student))
        while retireHeap.size() > 0:
            retireHeap.pop()
        while retryHeap.size() > 0:
            retryHeap.pop()

        jicha = [0, 3, 4, 5, 6]
        AdmitCount = 1
        tmpHeap1 = []
        tmpHeap1.append(MaxHeap())
        for student in tmpHeap._data:
            for major in bjut.major:
                if student.will[0] == major.MajorCode:
                    if major.isNotFull():
                        major.add(student)
                    else:
                        tmpHeap1[0].add(student)
        tmpHeap1.append(MaxHeap())
        tmpHeap1.append(MaxHeap())
        tmpHeap1.append(MaxHeap())
        tmpHeap1.append(MaxHeap())

        while AdmitCount < 5:    
            while tmpHeap1[AdmitCount - 1].size() > 0:
                student = tmpHeap1[AdmitCount - 1].pop()
                for major in bjut.major:
                    if student.will[AdmitCount] == major.MajorCode:
                        if major.isNotFull():
                            major.add(student)
                        else:
                            tmpStu = major.pop()
                            tmpjc = tmpStu.will.index(major.MajorCode)
                            if student.scores['total'] - jicha[AdmitCount] > tmpStu.scores['total'] - tmpjc:
                                major.add(student)
                                tmpHeap1[tmpjc + 1].add(tmpStu)
                            else:
                                major.add(tmpStu)
                                tmpHeap1[AdmitCount].add(student)
            AdmitCount += 1

        #整合退档学生
        for tmplist in tmpHeap1:
            for student in tmplist._data:
                if student.isAdjust == 'yes':
                    retryHeap.add(student)
                else:
                    retireHeap.add(student)              

class Context(object):
    def __init__(self, AdmitStrategy):
        self.AdmitStrategy = AdmitStrategy

    def set_AdmitStrategy(self, AdmitStrategy):
        self.AdmitStrategy = AdmitStrategy
    
    def admit(self):
        return self.AdmitStrategy.admit()
#===============================gui=================================
#重写的多列listbox
class MultiListbox(Frame): 
    def __init__(self,master,lists): 
        Frame.__init__(self,master) 
        self.lists = [] 
        for l, w in lists: 
            frame = Frame(self) 
            frame.pack(side=LEFT, 
            expand=YES, fill=BOTH) 
            Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X) 
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0, relief=FLAT, exportselection=FALSE) 
            lb.pack(expand=YES, fill=BOTH) 
            self.lists.append(lb) 
            lb.bind("<B1-Motion>",lambda e, s=self: s._select(e.y)) 
            lb.bind("<Button-1>",lambda e,s=self: s._select(e.y)) 
            lb.bind("<Leave>",lambda e: "break") 
            lb.bind("<B2-Motion>",lambda e,s=self: s._b2motion(e.x,e.y)) 
            lb.bind("<Button-2>",lambda e,s=self: s._button2(e.x,e.y)) 
        frame = Frame(self) 
        frame.pack(side=LEFT, fill=Y) 
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X) 
        sb = Scrollbar(frame,orient=VERTICAL, command=self._scroll) 
         
        self.lists[0]["yscrollcommand"] = sb.set 
        sb.pack(side=LEFT, fill=Y)
    
    def _select(self, y): 
        row = self.lists[0].nearest(y) 
        self.selection_clear(0, END) 
        self.selection_set(row) 
        return "break" 
    
    def _button2(self, x, y): 
        for l in self.lists: 
            l.scan_mark(x,y) 
        return "break" 
    
    def _b2motion(self, x, y): 
        for l in self.lists: 
            l.scan_dragto(x, y) 
        return "break" 
    
    def _scroll(self, *args): 
        for l in self.lists: 
            l.yview(*args)
        return "break" 
    
    def curselection(self): 
        return self.lists[0].curselection() 
    
    def delete(self, first, last=None): 
        for l in self.lists: 
            l.delete(first,last) 
        
    def get(self, first, last=None): 
        result = [] 
        for l in self.lists: 
            result.append(l.get(first,last)) 
        if last: 
            return apply(map, [None] + result) 
        return result 
    
    def index(self, index): 
        self.lists[0],index(index) 
    
    def insert(self, index, *elements): 
        for e in elements: 
            i = 0 
            for l in self.lists: 
                l.insert(index, e[i]) 
                i = i + 1 
    
    def size(self): 
        return self.lists[0].size() 
    
    def see(self, index): 
        for l in self.lists:
            l.see(index) 
    
    def selection_anchor(self, index): 
        for l in self.lists: 
            l.selection_anchor(index) 
            
    def selection_clear(self, first, last=None): 
        for l in self.lists: 
            l.selection_clear(first,last) 
    
    def selection_includes(self, index): 
        return self.lists[0].seleciton_includes(index) 
    
    def selection_set(self, first, last=None): 
        for l in self.lists: 
            l.selection_set(first, last) 

#窗口创建
class CreatWindow(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.ceratWidgets()
        messagebox.showinfo("Message","Welcome!") #弹出消息窗口
    
    def ceratWidgets(self):
        #框架布局
        self.Msgframe = LabelFrame(root, height = 670, width = 1590, text = 'information', padx = 10, pady = 10)
        self.Msgframe.pack_propagate(0)
        self.Msgframe.pack()                        
        self.Cmdframe = LabelFrame(root, height = 220, width = 1270, text = 'command', pady = 10)
        self.Cmdframe.pack_propagate(0)
        self.Cmdframe.pack(side = 'right')
        self.ModeFrame = LabelFrame(root, height = 220, width = 350, text = 'set mode', padx = 10 , pady = 10) 
        self.ModeFrame.pack_propagate(0)   
        self.ModeFrame.pack(side = 'left')                               

        #information--------列表框
        self.listbox0 = MultiListbox(self.Msgframe, [['INFORMATION',50]])
        self.listbox0.pack(expand=YES, fill=BOTH, side = LEFT)
        self.listbox1 = MultiListbox(self.Msgframe, (('ID', 5), ('Name', 5), ('Age', 3), ('sex', 6), ('isAdjust',5), ('Total', 5), ('Chinese', 5), ('Math', 5), ('English', 5), ('Comp', 5), ('Will', 20)))      
        self.listbox1.pack(expand=YES, fill=BOTH, side = RIGHT)
        #command------------button
        self.mbtn0 = Button(self.ModeFrame, text = 'Grade\nPriority', width = 15, height = 5, command = self.mbtn0Inf)
        self.mbtn0.pack(pady = 20)
        self.mbtn1 = Button(self.ModeFrame, text = 'Major\nDifferential', width = 15, height = 5, command = self.mbtn1Inf)
        self.mbtn1.pack()
        self.btn0 = Button(self.Cmdframe, text = 'School\nInformation', width = 15, height = 5, command = self.btn0Inf, state = DISABLED)
        self.btn0.grid(row = 0, column = 0, padx = 40, pady = 60)        
        self.btn1 = Button(self.Cmdframe, text = 'Student\nInformation', width = 15, height = 5, command = self.btn1Inf, state = DISABLED)
        self.btn1.grid(row = 0, column = 1, padx = 40, pady = 60)       
        self.btn3 = Button(self.Cmdframe, text = 'Dispensing\nStudent', width = 15, height = 5, command = self.btn3Inf, state = DISABLED)
        self.btn3.grid(row = 0, column = 3, padx = 40, pady = 60)
        self.btn4 = Button(self.Cmdframe, text = 'Retired\nStudent', width = 15, height = 5, command = self.btn4Inf, state = DISABLED)
        self.btn4.grid(row = 0, column = 4, padx = 40, pady = 60)
        self.btn5 = Button(self.Cmdframe, text = 'Result\nof\nAdmission', width = 15, height = 5, command = self.btn5Inf, state = DISABLED)
        self.btn5.grid(row = 0, column = 2, padx = 40, pady = 60)
        self.btn6 = Button(self.Cmdframe, text = 'Exit', width = 15, height = 5, command = root.quit).grid(row = 0, column = 5, padx = 20, pady = 60) 
    
    def mbtn0Inf(self):
        self.mbtn1['state'] = 'normal'
        self.mbtn0['state'] = 'disabled'
        self.btn0['state'] = 'normal'
        self.btn1['state'] = 'normal'
        admit = Context(bjutAdmit())
        admit.admit()
    
    def mbtn1Inf(self):
        self.mbtn0['state'] = 'normal'
        self.mbtn1['state'] = 'disabled'
        self.btn0['state'] = 'normal'
        self.btn1['state'] = 'normal'
        admit = Context(scuAdmit())
        admit.admit()

    def btn0Inf(self): 
        self.listbox0.delete(0, END)
        self.listbox0.insert(END, ['SchoolCode:%s' %bjut.schCode], ['SchoolName:%s' %bjut.schName], ['MajorInformation:'], ['    code:name,num'])
        for major in bjut.major:
            self.listbox0.insert(END, ['    %s:%s,%s'%(major.MajorCode, major.MajorName, major.MajorNum)])    
        messagebox.showinfo("Message","Operation succeeded!") #弹出消息窗口
        
    def btn1Inf(self):       
        self.btn3['state'] = 'normal'
        self.btn4['state'] = 'normal'
        self.btn5['state'] = 'normal'
        
        self.listbox1.delete(0, END)
        for student in myClass:
            self.listbox1.insert(END, student.strIfo())
        messagebox.showinfo("Message","Operation succeeded!") #弹出消息窗口              

    def btn3Inf(self):
        self.listbox1.delete(0, END)
        for student in retryHeap._data:
            self.listbox1.insert(END, student.strIfo())  
        messagebox.showinfo("Message","Operation succeeded!") #弹出消息窗口       

    def btn4Inf(self):
        self.listbox1.delete(0, END)
        for student in retireHeap._data:
            self.listbox1.insert(END, student.strIfo())      
        messagebox.showinfo("Message","Operation succeeded!") #弹出消息窗口        
    
    def btn5Inf(self):
        self.listbox0.delete(0, END)
        self.listbox1.delete(0, END)
        
        for major in bjut.major:
            self.listbox0.insert(END, ['MajorCode:%s' %major.MajorCode], ['MajorName:%s' %major.MajorName], ['less:%s' %major.MajorLess], [''])
            for student in major.mates:
                tmplist = student.strIfo()
                tmplist.pop()
                tmplist.append(str('%s' %major.MajorCode))
                self.listbox1.insert(END, tmplist)
    
        messagebox.showinfo("Message","Operation succeeded!") #弹出消息窗口  
#=======================load information============================
def LoadSchInfo():   
    #load school information 
    f = open('/home/yanglin/homework/school information.txt', 'r')
    f_list = f.readline().strip().split()
    SchoolName = f_list.pop()
    SchoolCode = int(f_list.pop())
    bjut = SchIfo(SchoolCode, SchoolName)
    for line in f.readlines():
        line_list = line.strip().split()
        MajorLess = int(line_list.pop())
        MajorNum = int(line_list.pop())
        MajorName = line_list.pop()
        MajorCode = int(line_list.pop())
        bjut.addMajor(MajorCode, MajorName, MajorNum, MajorLess)
    f.close()   
    return bjut

def LoadStuInfo():
    #load student information
    f = open('/home/yanglin/homework/student information.txt', 'r')
    myClass = []
    f_list1 = f.readlines()
    while len(f_list1) > 0:
        basicinf = f_list1.pop(0).strip().split()
        name = basicinf.pop(0)
        snum = int(basicinf.pop(0))
        age = int(basicinf.pop(0))     
        sex = basicinf.pop(0)
        isAdjust = basicinf.pop(0)
        tmpstudent = StuIfo(name, age, snum, sex, isAdjust)
        tmpstudent.setFullscore(eval(f_list1.pop(0).strip()))
        for will in f_list1.pop(0).strip().strip("[]").split(","):
            tmpstudent.addWill(int(will))
        myClass.append(tmpstudent)
    f.close()
    return myClass
#===============================main================================
if __name__ == '__main__':  
    bjut = deepcopy(LoadSchInfo())
    myClass = deepcopy(LoadStuInfo())
    retireHeap = MaxHeap()
    retryHeap = MaxHeap()
    tmpHeap = MaxHeap()
    for student in myClass:
       tmpHeap.add(student)

    root = Tk()
    root.title('学生志愿管理系统')
    #设置窗口大小
    width = 1600
    height = 900
    #设置居中
    screenwidth = root.winfo_screenwidth() 
    screenheight = root.winfo_screenheight() 
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2) 
    root.geometry(alignstr)
    #设置窗口不可变
    root.resizable(width = False, height = False)

    app = CreatWindow(master = root)
    app.mainloop()