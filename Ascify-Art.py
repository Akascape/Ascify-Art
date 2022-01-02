from tkinter import *
import math
import tkinter
from tkinter import Tk, Entry, Button, Label, ttk, messagebox, filedialog
import os
import webbrowser
import sys
import pkg_resources
import glob
import shutil
required = {'pillow','matplotlib'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
missingset=[*missing,]
if missing:
    res=messagebox.askquestion("Module Error","Some modules are not installed, do you want to download and install them?")
    if res=="yes":
        for x in range(len(missingset)):
            y=missingset[x]
            os.system('python -m pip install '+y)
        from PIL import Image, ImageDraw, ImageFont
        import matplotlib.font_manager
        pass
    elif res=="no":
        print("Error: Required modules not available! \nWithout the modules you can't use this program. Please install them first!")
        sys.exit()
else:
    from PIL import Image, ImageDraw, ImageFont
    import matplotlib.font_manager
def resource_path0(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
def openfile():
    global file, folder
    if firstLabel['text']=="Choose Image":
        file=tkinter.filedialog.askopenfilename(filetypes =[('PNG', '*.png'),('All Files', '*.*')])
        folder=""
    else:
        folder=tkinter.filedialog.askdirectory()
        file=""
    if(len(file)>=1 or len(folder)>=1):
        Img['text']='OPEN AGAIN'
        Img['bg']='#D0CECE'
    else:
        Img['text']='OPEN'
        Img['bg']="#82CC6C"
def prestep():
    if Img['text']=='OPEN AGAIN':           
        if len(CharEntry.get())>=1:
            if len(Size.get())==0:
                messagebox.showerror("OOPS!","Please enter a valid size!")
                return() 
            else:
                pass
        else:
            messagebox.showerror("OOPS!","Please enter some characters!")
            return() 
    else:
        messagebox.showerror("OOPS!","Please choose the image first!")
        return()
    if firstLabel['text']=="Choose Image":
        global file
        if os.path.exists(file[:-4]+"_Ascified.png"):
            res1=messagebox.askquestion("Warning!","Do you want to replace the old output file with the new one? \n(Process not reversible!)")
            if res1=='yes':
                os.remove(file[:-4]+"_Ascified.png")
                if var5.get()==1:
                    os.remove(file[:-4]+"_Ascified.txt")
            elif res1=='no':
                return()
        Convert(file)
        messagebox.showinfo("Done! :)","Image Ascified!")
    else:
        global newfolder
        allitems=glob.glob(folder+'\*.png')
        allitems.extend(glob.glob(folder+'\*.jpeg'))
        allitems.extend(glob.glob(folder+'\*.jpg'))
        if len(allitems)==0:
            messagebox.showerror("OOPS!","No image files in this folder!")
            return() 
        prefolder=os.path.dirname(folder)
        prefile=os.path.basename(folder)
        newfolder=prefolder+"/"+prefile+"_Ascified"
        if os.path.isdir(newfolder):
            res2=messagebox.askquestion("Warning!","Do you want to replace the old output folder with the new one? \n(Process not reversible!)")
            if res2=='yes':
                shutil.rmtree(newfolder)       
            elif res2=='no':
                return()
        os.mkdir(newfolder)
        count=1
        for i in allitems:
            file=i.replace(os.sep, '/')
            Convert(file)
            Log.place(x=210,y=240)
            Log.config(text=count)
            root.update_idletasks()
            count+=1
        Log.place_forget()
        messagebox.showinfo("Done! :)","Image Ascified!")
def Convert(file):
    try:
        Log.place(x=185,y=235)
        Log.config(text=".  ")
        Disabled()
        root.update_idletasks()
        chars=CharEntry.get()[::-1]
        prefile=os.path.basename(file)
        charArray = list(chars)
        charLength = len(charArray)
        interval = charLength/256
        scaleFactor = 0.09
        oneCharWidth = 10
        oneCharHeight = 18
        def getChar(inputInt):
            return charArray[math.floor(inputInt*interval)]
        if var5.get()==1:
            if firstLabel['text']=="Choose Image":
                text_file = open(file[:-4]+"_Ascified.txt", "w")
            else:
                if os.path.exists(newfolder+"/Text version/"):
                    pass
                else:
                    os.mkdir(newfolder+"/Text version/")
                text_file = open(newfolder+"/Text version/"+prefile[:-4]+"_Ascified.txt", "w")
        im = Image.open(file)
        getfont=fontbox.get()
        y=flist.index(getfont)
        z=plist[y]
        final=z+"\\"+getfont
        s=Size.get()
        fnt = ImageFont.truetype(final, int(s))
        width, height = im.size
        im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
        width, height = im.size
        pix = im.load()
        Log.config(text=".. ")
        root.update_idletasks()
        outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = (0, 0, 0))
        d = ImageDraw.Draw(outputImage)
        for i in range(height):
            for j in range(width):
                r, g, b = pix[j, i]
                h = int(r/3 + g/3 + b/3)
                pix[j, i] = (h, h, h)
                if var5.get()==1:
                    text_file.write(getChar(h))
                d.text((j*oneCharWidth, i*oneCharHeight), getChar(h), font = fnt, fill = (r, g, b))
            if var5.get()==1:
                text_file.write('\n')
        Log.config(text="...")
        root.update_idletasks()
        if firstLabel['text']=="Choose Image":
            outputImage.save(file[:-4]+"_Ascified.png")
        else:
            outputImage.save(newfolder+"/"+prefile[:-4]+"_Ascified.png")
        if var5.get()==1:   
            text_file.close()
        Log.place_forget()
        Enabled()
    except:
        Log.place_forget()
        messagebox.showerror("OOPS! :(","Something went wrong!")
        Enabled()
def callback(url):
    webbrowser.open_new_tab("https://github.com/Akascape/Ascify-Art")
def info():
    messagebox.showinfo("HELP",
    "This program can crate art with colored ASCII characters!"
    "\n➤Click the OPEN button and choose your image file"
    "\n➤Then choose the font, size and character you want in the output"
    "\n➤Then simply click the CREATE button, the output image and text file will be saved in the same root diretory."
    "\n\nDeveloper: Akash Bora (a.k.a. Akascape)\nIf you have any issue then contact me on Github."
    "\nVersion-0.2")
def Disabled():
    Img['state']=DISABLED
    CharEntry['state']=DISABLED
    fontbox['state']=DISABLED
    Size['state']=DISABLED
    btn['state']=DISABLED
    tbox['state']=DISABLED
def Enabled():
    Img['state']=NORMAL
    CharEntry['state']=NORMAL
    fontbox['state']=NORMAL
    Size['state']=NORMAL
    btn['state']=NORMAL
    tbox['state']=NORMAL
def switch():
    EntryVar.set("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
def switch2():
    if firstLabel['text']=="Choose Image":
        firstLabel.config(text="Choose Sequence")
        Img['text']='OPEN'
        Img['bg']="#82CC6C"
        root.update_idletasks()
    else:
        firstLabel.config(text="Choose Image")
        Img['text']='OPEN'
        Img['bg']="#82CC6C"
        root.update_idletasks()
root= Tk()
root.title("Ascify-Art")
root.resizable(width=False, height=False)
path=resource_path0("Programicon.ico")
root.wm_iconbitmap(path)
root.columnconfigure(0,weight=1)
root.geometry("400x300")
root.configure(bg='#FFFFFF')
Label(root, text="ASCIFY-ART", font=("Impact",17),bd=1, fg="#5DBCD2", bg="#FFFFFF").grid()
firstLabel=Label(root, text="Choose Image", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF")
firstLabel.grid()
Img=Button(root, width=50,bg="#82CC6C",fg="white",highlightthickness=1,borderwidth=0.2,text="OPEN",relief="groove", command=openfile)
Img.grid()
Label(root, text="Choose Font", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF").place(x=100,y=80)
fonts= matplotlib.font_manager.findSystemFonts()
flist=[]
plist=[]
for i in fonts:
    f=os.path.basename(i)
    p=os.path.dirname(i)
    flist.append(f)
    plist.append(p)
fontbox=ttk.Combobox(root,values=sorted(flist), font="Verdana 10", width=10, height=9)
fontbox.current(0)
fontbox.place(x=90,y=105)
EntryVar= StringVar()
Label(root, text="Characters", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF").place(x=165,y=132)
CharEntry=Entry(root,bg="light blue",width=50,borderwidth=3,textvariable=EntryVar)
EntryVar.set("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
CharEntry.place(x=40,y=155)
Label(root, text="Size", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF").place(x=250,y=80)
sizevar=IntVar()
Size=Entry(root,bg="light blue",width=3,borderwidth=3,textvariable=sizevar)
sizevar.set(15)
Size.place(x=250,y=105)
btn=Button(width=25, height=2,text="CREATE",font=("Cambria", 9),bg="#5DBCD2",fg="#FFFFFF",borderwidth=0,highlightthickness=2,padx=0,pady=0,command=prestep)
btn.place(x=110,y=200)
Log=Label(root,text="", font=("Calibri",20), fg="#5DBCD2", bg="#FFFFFF")
dev=Label(root, text='Developed by Akascape | ',bg='#FFFFFF',fg="#6D76CD", font=("Impact",10))
dev.place(x=5,y=280)
link=Label(root, text="Github Link",font=('Impact',10),bg='#FFFFFF',fg="#6D76CD", cursor="hand2")
link.place(x=140,y=280)
link.bind("<Button-1>", lambda e:
callback("https://github.com/Akascape/Ascify-Art"))
infobtn= Button(root, width=2,bg="#FFFFFF",fg="black", text="ⓘ",font=(10),relief="sunken",cursor='hand2', highlightthickness=0,borderwidth=0,padx=0,pady=0,command=info)
infobtn.place(x=377,y=275)
rebtn= Button(root, width=2,bg="#FFFFFF",fg="black", text="⟳",font=(10),relief="sunken",cursor='hand2', highlightthickness=0,borderwidth=0,padx=0,pady=0,command=switch)
rebtn.place(x=350,y=153)
Change=Button(root, width=2,bg="#FFFFFF",fg="black", text="🔃",font=(10),relief="sunken",cursor='hand2', highlightthickness=0,borderwidth=0,padx=0,pady=0,command=switch2)
Change.place(x=355,y=29)
var5 = IntVar()
var5.set(1)
tbox=Checkbutton(root, text="Export Text",bg="#FFFFFF",variable=var5,onvalue=1, offvalue=0)
tbox.place(x=340,y=250, anchor='center')
root.mainloop()
#By Akash Bora(a.k.a Akascape)
