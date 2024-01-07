import gui 
from gui import Colors
import calculator
from tkinter import ttk
import tkinter as tk
import log
log.info("Starting Calculator [Class Project, Made by Divyansh]")


WIDTH = 350
HEIGHT = 550


class MyWindow:  
    SPECIAL_CTRL_SYMBOLS = ("=","C")
    CALC_NUMS = ("C","(",")","1","2","3","4","5","6","7","8","9",".","0","π")
    
    def replace_entry_input(self):
        text = self.input_box.get()
        new_text = ""
        for i in text:
            ch = i
            if i == "*":
                ch = calculator.CALC_CMDS["product"]
            
            elif i == "/":
                ch = calculator.CALC_CMDS["divide"]
            
            elif i == "-":
                ch = calculator.CALC_CMDS["subtract"]
            
            new_text += i
        print(new_text)
    def __init__(self):
        self.win = gui.Window("Calculator",WIDTH,HEIGHT)

        #label
        self.r_label = tk.Text(font="Serif 12",state="disabled",height=8,bg="#111",fg="#aaa",relief="flat",borderwidth="0")
        self.r_label.config(spacing1=1,spacing2=1,spacing3=1)
        self.r_label.pack(anchor='n',fill="both",ipadx=10,ipady=10)

        insert_subtract = lambda:self.input_box.insert(tk.INSERT,"−")
        insert_multiply = lambda:self.input_box.insert(tk.INSERT,"×")
        insert_divide = lambda:self.input_box.insert(tk.INSERT,"÷")

        
        sb = tk.Scrollbar(orient="horizontal",troughcolor=Colors.SCROLLBAR_BG)
        vcmd = self.win.register(self.handle_entry)
        entry = tk.Entry(font="Serif 20",state="normal",justify=tk.RIGHT,xscrollcommand=sb.set,validate="all",validatecommand=(vcmd,"%S"),bg=Colors.ENTRY_BG,fg=Colors.PRIMARY_TEXT)
        entry.pack(anchor='n',fill='x',ipadx=10,ipady=10)
        entry.bind("<Return>", lambda e: self.calculateResult())
        entry.bind("-", lambda e: insert_subtract())
        entry.bind("*", lambda e: insert_multiply())
        entry.bind("/", lambda e: insert_divide())


        sb.pack(anchor='n',fill='x')
        sb.config(command=entry.xview)
        

        self.input_box = entry
        self.buttonFrame = self.win.getFrame(self.win)
        self.numBtnFrame = self.win.getFrame(self.buttonFrame)
        self.controlBtnFrame = self.win.getFrame(self.buttonFrame)


        self.buttonFrame.grid_columnconfigure(0,weight=1)
        self.buttonFrame.grid_columnconfigure(1,weight=1)
        self.buttonFrame.grid_rowconfigure(0,weight=1)
        self.buttonFrame.pack(fill="both",anchor="s")
        self.numBtnFrame.grid(column=0,row=0,sticky='nsew')
        self.controlBtnFrame.grid(column=1,row=0,sticky="nsew")
    def handle_entry(self, S):
        # check if entry is valid
        for i in S:
            if not (i in calculator.operators or i in "e(.)π" or i.isdigit()) or i in "-*/":
                return False
        return True

    def calculateResult(self):
        exp = self.input_box.get()
        result = str(calculator.evaluateExpression(exp)).replace("-", "−").strip()
        if result == "None":
            result = "Invalid syntax"
        print("result is : ", result)
        self.input_box.delete(0,len(self.input_box.get()))
        self.input_box.insert(tk.INSERT,str(result).strip())
        self.input_box.xview("end")

        s1 =  exp + " =\n" + str(result) if result != "None" else result
        output = str(self.r_label.get("1.0",tk.END)).replace("Invalid syntax\n―――――――――――――――――――――\n","").strip()+"\n"+ s1 +"\n―――――――――――――――――――――\n"
        #save the result to label
        self.r_label.config(state="normal")
        self.r_label.delete("1.0",tk.END)
        self.r_label.insert("1.0",output)
        self.r_label.see(tk.END)
        self.r_label.config(state="disable")

    def generateNumButtons(self,ls):
        buttons_ls = []
        row = 0
        col = 0
        for num_str in ls:
            btn = self.win.createNumButton(self.numBtnFrame,num_str, lambda txt = num_str: self.numBtnClick(txt))
            btn.grid(column=col,row=row)
            if num_str in MyWindow.SPECIAL_CTRL_SYMBOLS:
                btn.config(bg=Colors.SPECIAL_BUTTON,activebackground=Colors.SPECIAL_BUTTON)
            buttons_ls.append(btn)
            self.numBtnFrame.grid_columnconfigure(col,weight=1)
            self.numBtnFrame.grid_rowconfigure(row,weight=1)

            
            if col < 2:
                col+=1
            else:
                col = 0
                row +=1
        return ls
    def genrateControlButtons(self,dict):
        ctrl_btn_ls = []
        row = 0
        col = 0
        for i in dict:
            if dict[i] == "square" or dict[i] == "factorial":
                i = "x"+i
            ctrl_btn = self.win.createControlButton(self.controlBtnFrame,i,lambda txt = i: self.ctrlBtnClick(txt))
            ctrl_btn.grid(column=col,row=row)

            ctrl_btn_ls.append(ctrl_btn)
            if i in MyWindow.SPECIAL_CTRL_SYMBOLS:
                ctrl_btn.config(bg=Colors.SPECIAL_BUTTON,activebackground=Colors.SPECIAL_BUTTON)
                ctrl_btn.grid(columnspan=2)
            self.controlBtnFrame.grid_columnconfigure(col,weight=1)
            self.controlBtnFrame.grid_rowconfigure(row,weight=1)
            if col < 1:
                col+=1
            else:
                col = 0
                row +=1
        return ctrl_btn_ls
    
    def start(self):
        self.buttonFrame.pack(anchor='n',fill='both')
        num_btn_lst = self.generateNumButtons(MyWindow.CALC_NUMS)
        cmd_btn_lst = self.genrateControlButtons(calculator.CALC_CMDS)
        self.win.mainloop()

    def numBtnClick(self,txt):
        if self.input_box != None:
            length = len(self.input_box.get())
            if txt == "C":
                self.input_box.delete(self.input_box.index(tk.INSERT) - 1, tk.INSERT)
            else:
                self.input_box.insert(tk.INSERT,txt)   
                self.input_box.xview("end")


    def ctrlBtnClick(self,txt):
        ctrl = str(txt).replace("x","")
        if self.input_box != None:
            if ctrl == "=":
                self.calculateResult()
                
            else:
                self.input_box.insert(tk.INSERT,ctrl)
                self.input_box.xview("end")

MyWindow().start()
