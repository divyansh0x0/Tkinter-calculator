import tkinter as tk
from tkinter import ttk
class Colors:
    def color_variant(hex_color, brightness_offset=1):
        """ takes a color like #87c95f and produces a lighter or darker variant """
        if len(hex_color) != 7:
            raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
        rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
        new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
        new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
        # hex() produces "0x88", we want just "88"
        return "#" + "".join([hex(i)[2:] for i in new_rgb_int])
    BACKGROUND = "#121212"
    PRIMARY_TEXT = "#FFFFFF"

    SCROLLBAR_BG = "#202020"
    SCROLLBAR_THUMB = [('active',"#111"),('pressed',"#111"),('!pressed',"#111")] 
    NUM_BUTTON = "#232323"
    PRESSED_NUM_BUTTON = "#212121"

    CONTROL_BUTTON ='#262626'
    PRESSED_CONTROL_BUTTON ='#242424'
    
    SPECIAL_BUTTON ="#000"

    ENTRY_BG = "#121212"
    




class Window(tk.Tk):                  
    def __init__(self, name:str, width:int,height:int) -> None:
        tk.Tk.__init__(self)
        self.name = name
        self.width = width
        self.height = height
        x = int((self.winfo_screenwidth()-width)/2)
        y = int((self.winfo_screenheight()-height)/2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title(name)
        self.resizable(False,False)  
        
        print("window created")

    def createNumButton(self,owner,text:str, cmd) -> ttk.Button:
        btn = tk.Button(master=owner,borderwidth=0,activebackground=Colors.PRESSED_NUM_BUTTON, activeforeground=Colors.PRIMARY_TEXT,fg=Colors.PRIMARY_TEXT,bg=Colors.NUM_BUTTON,text=text,width=1,command=cmd)
        btn.grid(ipadx=20,ipady=20,sticky='nsew')
        return btn
    
    def createControlButton(self,owner,text:str,cmd) ->ttk.Button:
        btn = tk.Button(owner,text=text,borderwidth=0,activebackground=Colors.PRESSED_CONTROL_BUTTON, activeforeground=Colors.PRIMARY_TEXT,fg=Colors.PRIMARY_TEXT,bg=Colors.CONTROL_BUTTON,width=1,command=cmd)
        
        btn.grid(ipadx=20,ipady=20,sticky='nsew')
        return btn
    def getFrame(self, owner) -> ttk.Frame:
        frame = ttk.Frame(owner)
        
        return frame

