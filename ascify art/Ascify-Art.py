
"""
╔═══╗           ╔═╗         ╔═══╗    ╔╗
║╔═╗║           ║╔╝         ║╔═╗║   ╔╝╚╗
║║ ║║╔══╗╔══╗╔╗╔╝╚╗╔╗ ╔╗    ║║ ║║╔═╗╚╗╔╝
║╚═╝║║══╣║╔═╝╠╣╚╗╔╝║║ ║║    ║╚═╝║║╔╝ ║║
║╔═╗║╠══║║╚═╗║║ ║║ ║╚═╝║    ║╔═╗║║║  ║╚╗
╚╝ ╚╝╚══╝╚══╝╚╝ ╚╝ ╚═╗╔╝    ╚╝ ╚╝╚╝  ╚═╝
                   ╔═╝║
                   ╚══╝
Version: 0.9
Developer: Akash Bora (Akascape)
License: MIT
More info: https://github.com/Akascape/Ascify-Art
"""

import customtkinter
import sys
import tkinter as tk
from tkinter import ttk, font, filedialog
import threading
import os
from PIL import Image, ImageDraw, ImageTk, ImageFont, ImageEnhance, UnidentifiedImageError
import CTkColorPicker
import math
import glob
import matplotlib.font_manager
import webbrowser
import random
from tkinterdnd2 import TkinterDnD, DND_ALL

customtkinter.set_appearance_mode("Dark")

class CTk(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
        
root = CTk()
root.geometry("1100x600")
root.minsize(800,430)
root.title("Ascify Art")
root.configure(fg_color="#1e2434")
root.columnconfigure((0,1), weight=1)
root.rowconfigure(1, weight=1)
root.bind("<1>", lambda event: event.widget.focus_set())
root.wm_iconbitmap()

def get_path(event):
    dropped_file = event.data.replace("{","").replace("}", "")
    openfile(dropped_file)
        
root.drop_target_register(DND_ALL)
root.dnd_bind("<<Drop>>", get_path)

if sys.platform.startswith("win"):
    # Apply the mica theme for windows if possible (works with windows 11)
    try:
        from ctypes import windll, byref, sizeof, c_int
        HWND = windll.user32.GetParent(root.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x34241e)), sizeof(c_int))
    except:
        pass
    
def exit_program():
    x = tk.messagebox.askquestion("Exit?", "Do you want to close this program?")
    if x=="yes":
        root.destroy()
    else:
        return

def resource(relative_path):
    # resource finder via pyinstaller
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

icopath = ImageTk.PhotoImage(file=resource("icon.png"))
root.iconphoto(False, icopath)
root.protocol("WM_DELETE_WINDOW", exit_program)

app_color = random.choice(["#487a7d", "#e49c04", "#84b701", "#e52aff", "#5591c8"])

frame_image = customtkinter.CTkFrame(root, width=350, fg_color="#1b202c", corner_radius=20)
frame_image.grid(column=1, row=0, rowspan=10, sticky="nsew", padx=20, pady=20)
frame_image.rowconfigure(0, weight=1)
frame_image.columnconfigure(0, weight=1)

label_image = customtkinter.CTkLabel(frame_image, width=350, fg_color="#1b202c", corner_radius=0, text="")
label_image.grid(sticky="nsew", padx=5, pady=5)

title = customtkinter.CTkImage(Image.open(resource("title.png")), size=(250,40))
label_1 = customtkinter.CTkLabel(root, text="", image=title)
label_1.grid(row=0, column=0, sticky="wen", pady=20)

file = ""
previous = ""
background = "black"
frame_no = 0
ascii_string = ""
sequence = False

def operation():
    # main function that will do the magic
    global image, outputImage, ascii_string

    if not file:
        return

    def getChar(inputInt):
        return charArray[math.floor(inputInt*interval)]

    chars = textbox.get('1.0', tk.END)[::-1]
    charArray = list(chars)
    charLength = len(charArray)
    interval = charLength/256
    scaleFactor = round(slider_scale.get(), 3)
    oneCharWidth = int(slider_width.get())
    oneCharHeight = int(slider_height.get())
    s = int(slider_size.get())
    im = Image.open(file).convert('RGB')

    if selected_font:
        fnt = ImageFont.truetype(selected_font, s)
    else:
        fnt = ImageFont.load_default()

    width, height = im.size
    im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.Resampling.NEAREST)
    width, height = im.size
    pix = im.load()
    outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = background)
    d = ImageDraw.Draw(outputImage)

    new_r = int(slider_r.get())
    new_g = int(slider_g.get())
    new_b = int(slider_b.get())
    auto = automatic.get()
    
    ascii_string = ""
    # replace the pixels with text
    for i in range(height):
        for j in range(width):
            r, g, b = pix[j, i]

            if auto==0:
                if r>=new_r: r = new_r
                if g>=new_g: g = new_g
                if b>=new_b: b = new_b

            h = int(r/3 + g/3 + b/3)
            pix[j, i] = (h, h, h)
            d.text((j*oneCharWidth, i*oneCharHeight), getChar(h), font = fnt, fill = (r, g, b))
            ascii_string += str(getChar(h))
        ascii_string += "\n"
        
    # some other enhancements like saturation and brightness
    outputImage = ImageEnhance.Color(outputImage).enhance(slider_sat.get())
    outputImage = ImageEnhance.Brightness(outputImage).enhance(slider_br.get())

    # update the label
    image = customtkinter.CTkImage(outputImage, size=(frame_image.winfo_height(),frame_image.winfo_height()*img.size[1]/img.size[0]))
    label_image.configure(image=image)

def openfile(prefile=None):
    # opening and loading the file
    global file, image, img, dir_, sequence, previous
    if not prefile:
        file = filedialog.askopenfilename(filetypes=[('Images', ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*webp']),
                                                     ('All Files', '*.*')])
    else:
        file = prefile
    if os.path.exists(file):
        # check if imported image is valid or not
        try:
            Image.open(file)
        except UnidentifiedImageError:
            tk.messagebox.showerror("Oops!", "Not a valid image file!")
            file = previous
            return

        sequence = False
        previous = file

        if len(os.path.basename(file))>=50:
            open_button.configure(
                text=f"{os.path.basename(file)[:40]}...{os.path.basename(file)[-3:]}"
            )
        else:
            open_button.configure(text=os.path.basename(file))

        img = Image.open(file)
        image = customtkinter.CTkImage(img)
        label_image.configure(image=image)
        image.configure(size=(frame_image.winfo_height(),frame_image.winfo_height()*img.size[1]/img.size[0]))

        dir_ = os.path.dirname(file)
        if len(dir_)>=30:
            entry_location.configure(text=f"{dir_[:25]}...{dir_[-5:]}")
        else:
            entry_location.configure(text=dir_)

        var.set(f"{os.path.basename(file)[:-4]}_Ascified")

        try:
            root.unbind("<KeyRelease-Left>")
            root.unbind("<KeyRelease-Right>")
            RightClickMenu.delete("Next Frame")
            RightClickMenu.delete("Previous Frame")
        except:
            None
    elif previous!="":
        file = previous

def frame_next():
    # load next frame of sequence
    global frame_no, file
    if frame_no<len(allitems)-1:
        file = allitems[frame_no+1]
        frame_no+=1
        operation()

def frame_previous():
    # load previous frame of sequence
    global frame_no, file
    if frame_no>0:
        file = allitems[frame_no-1]
        frame_no-=1
        operation()

def open_sequence():
    # opening a sequence of images (folder)

    global dir_, file, img, image, allitems, sequence
    if dir_img := filedialog.askdirectory():
        allitems = glob.glob(dir_img+'\*.png')
        allitems.extend(glob.glob(dir_img+'\*.jpeg'))
        allitems.extend(glob.glob(dir_img+'\*.jpg'))
        allitems.extend(glob.glob(dir_img+'\*.bmp'))
        allitems.extend(glob.glob(dir_img+'\*.webp'))

        if len(allitems) == 0:
            tk.messagebox.showinfo("Oops!", "No valid image files present in this folder!")
            return

        sequence = True
        if len(dir_img)>=50:
            open_button.configure(text=f"{dir_img[:40]}...{dir_img[-3:]}")
        else:
            open_button.configure(text=dir_img)

        dir_ = os.path.dirname(dir_img)
        if len(dir_)>=30:
            entry_location.configure(text=f"{dir_[:25]}...{dir_[-5:]}")
        else:
            entry_location.configure(text=dir_)

        try:
            RightClickMenu.delete("Next Frame")
            RightClickMenu.delete("Previous Frame")
        except:
            None

        var.set(f"{os.path.basename(dir_img)}_Ascified")
        RightClickMenu.add_command(label="Next Frame", command=lambda: frame_next())
        RightClickMenu.add_command(label="Previous Frame", command=lambda: frame_previous())

        file = allitems[0]
        img = Image.open(file)
        image = customtkinter.CTkImage(img)
        label_image.configure(image=image)
        image.configure(size=(frame_image.winfo_height(),frame_image.winfo_height()*img.size[1]/img.size[0]))
        root.bind("<KeyRelease-Left>", lambda e: frame_previous())
        root.bind("<KeyRelease-Right>", lambda e: frame_next())

def resize_event(event):
    # dynamic resize of the image with UI
    global image
    if image!="":
        image.configure(size=(event.height,event.height*img.size[1]/img.size[0]))

open_button = customtkinter.CTkButton(root, text="OPEN", fg_color=app_color, command=openfile)
open_button.grid(row=1, column=0, sticky="wen", pady=20, padx=(20,0))
root.bind("<Control-o>", lambda e: openfile())

image = ""

# TABS
frame_image.bind("<Configure>", resize_event)
tabview = customtkinter.CTkTabview(root, fg_color="#1b202c",
                                   segmented_button_fg_color="#0e1321",
                                   segmented_button_selected_color=app_color,
                                   segmented_button_unselected_color="#0e1321",
                                   segmented_button_selected_hover_color=app_color)
tabview.grid(row=1, column=0, padx=(20, 0), pady=(80, 20), sticky="nsew")
tabview.add("Characters")
tabview.add("Size")
tabview.add("Colors")
tabview.add("Font")
tabview.add("Export")

def show_original():
    # show original image (right click on the image)
    global image
    if file:
        image = customtkinter.CTkImage(img)
        image.configure(size=(frame_image.winfo_height(),frame_image.winfo_height()*img.size[1]/img.size[0]))
        label_image.configure(image=image)

def copy_ascii():
    operation()
    root.clipboard_append(ascii_string)
        
RightClickMenu = tk.Menu(frame_image, tearoff=False, background='#343e5a', fg='white', borderwidth=0, bd=0, activebackground=app_color)
RightClickMenu.add_command(label="Show Original", command=lambda: show_original())
RightClickMenu.add_command(label="Show Ascified", command=lambda: operation())
RightClickMenu.add_command(label="Copy Ascii Text", command=lambda: copy_ascii())

root.bind("<Return>", lambda e: operation())
                 
def do_popup(event, frame):
    try: frame.tk_popup(event.x_root, event.y_root)
    finally: frame.grab_release()

label_image.bind("<Button-3>", lambda event: do_popup(event, frame=RightClickMenu))

RightClickMenu2 = tk.Menu(frame_image, tearoff=False, background='#343e5a', fg='white', borderwidth=0, bd=0, activebackground=app_color)
RightClickMenu2.add_command(label="Open Image Sequence", command=lambda: open_sequence())

open_button.bind("<Button-3>", lambda event: do_popup(event, frame=RightClickMenu2))

# TAB 1 (Characters)
tabview.tab("Characters").rowconfigure((0,1), weight=1)
tabview.tab("Characters").columnconfigure(0, weight=1)

label_2 = customtkinter.CTkLabel(tabview.tab("Characters"), text="Enter characters:")
label_2.grid(row=0, column=0, sticky="wn", pady=10, padx=20)

text_live = customtkinter.CTkCheckBox(tabview.tab("Characters"), fg_color=app_color, text="Live Preview",
                                      hover=False, command=lambda: operation() if text_live.get()==1 else None)
text_live.grid(row=0, column=0, padx=20, pady=10, sticky="ne")
text_live.select()

textbox = customtkinter.CTkTextbox(tabview.tab("Characters"), fg_color="#282c35", undo=True)
textbox._textbox.configure(selectbackground=app_color)
textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(50,20), sticky="nsew")
textbox.insert(tk.END, "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
textbox.bind("<KeyRelease>", lambda event: operation() if text_live.get()==1 else None)

                
def cut_text():
    """ cut text operation """
    copy_text()
    try: textbox.delete(tk.SEL_FIRST, tk.SEL_LAST)
    except: pass
        
def copy_text():
    """ copy text operation """                                                                                                                  
    try:
        root.clipboard_clear()
        root.clipboard_append(textbox.get(tk.SEL_FIRST, tk.SEL_LAST))
    except: pass
        
def paste_text():
    """ paste text operation """
    try: textbox.insert(textbox.index('insert'), root.clipboard_get())
    except: pass
        
def clear_all_text():
    """ clears sll the text """
    try:
        textbox.delete(0.0,"end")
    except: pass

        
copy_menu = tk.Menu(textbox, tearoff=False, background='#343e5a', fg='white', borderwidth=0, bd=0, activebackground=app_color)
        
copy_menu.add_command(label="Cut", command=cut_text)
copy_menu.add_command(label="Copy", command=copy_text)
copy_menu.add_command(label="Paste", command=paste_text)
copy_menu.add_command(label="Clear", command=clear_all_text)
        
textbox.bind("<Button-3>", lambda event: do_popup(event, frame=copy_menu))

# TAB 2 (Size)
tabview.tab("Size").columnconfigure(0, weight=1)

label_4 = customtkinter.CTkLabel(tabview.tab("Size"), text="Character size: 15")
label_4.grid(row=0, column=0, sticky="wn", pady=10, padx=20)

slider_size = customtkinter.CTkSlider(
    tabview.tab("Size"),
    hover=False,
    height=20,
    button_color="white",
    from_=1,
    to=100,
    command=lambda e: label_4.configure(text=f"Character size: {int(e)}"),
)

slider_size.bind("<ButtonRelease-1>", lambda event: operation())
slider_size.grid(row=1, column=0, sticky="we", pady=0, padx=20)
slider_size.set(15)

label_14 = customtkinter.CTkLabel(tabview.tab("Size"), text="Scale factor: 0.09")
label_14.grid(row=2, column=0, sticky="wn", pady=10, padx=20)

slider_scale = customtkinter.CTkSlider(
    tabview.tab("Size"),
    hover=False,
    height=20,
    button_color="white",
    from_=0.01,
    to=0.2,
    command=lambda e: label_14.configure(
        text=f"Scale factor: {str(round(e, 3))}"
    ),
)
slider_scale.set(0.09)
slider_scale.bind("<ButtonRelease-1>", lambda event: operation())
slider_scale.grid(row=3, column=0, sticky="we", pady=0, padx=20)

label_12 = customtkinter.CTkLabel(tabview.tab("Size"), text="Scale width: 10")
label_12.grid(row=4, column=0, sticky="wn", pady=10, padx=20)

slider_width = customtkinter.CTkSlider(
    tabview.tab("Size"),
    hover=False,
    height=20,
    button_color="white",
    from_=1,
    to=30,
    command=lambda e: label_12.configure(text=f"Scale width: {int(e)}"),
)
slider_width.set(10)
slider_width.bind("<ButtonRelease-1>", lambda event: operation())
slider_width.grid(row=5, column=0, sticky="we", pady=0, padx=20)

label_13 = customtkinter.CTkLabel(tabview.tab("Size"), text="Scale height: 18")
label_13.grid(row=6, column=0, sticky="wn", pady=10, padx=20)

slider_height = customtkinter.CTkSlider(
    tabview.tab("Size"),
    hover=False,
    height=20,
    button_color="white",
    from_=1,
    to=30,
    command=lambda e: label_13.configure(text=f"Scale height: {int(e)}"),
)
slider_height.set(18)
slider_height.bind("<ButtonRelease-1>", lambda event: operation())
slider_height.grid(row=7, column=0, sticky="we", pady=0, padx=20)

# TAB 3 (Colors)
tabview.tab("Colors").columnconfigure(0, weight=1)

def toggle_rgb():
    # Turn off/on automatic colors
    if automatic.get()==1:
        slider_r.configure(state="disabled", button_color="grey")
        slider_g.configure(state="disabled", button_color="grey")
        slider_b.configure(state="disabled", button_color="grey")
        label_3.configure(state="disabled")
    else:
        slider_r.configure(state="normal", button_color="white")
        slider_g.configure(state="normal", button_color="white")
        slider_b.configure(state="normal", button_color="white")
        label_3.configure(state="normal")
    operation()

automatic = customtkinter.CTkSwitch(tabview.tab("Colors"), text="Automatic Colors",
                                    progress_color=app_color, command=toggle_rgb)
automatic.grid(row=0, column=0, sticky="wn", pady=10, padx=20)

# IMAGE ENHANCEMENTS
label_3 = customtkinter.CTkLabel(tabview.tab("Colors"), text="RGB Space:")
label_3.grid(row=1, column=0, sticky="wn", pady=10, padx=20)

slider_r = customtkinter.CTkSlider(tabview.tab("Colors"), height=20, progress_color="red",
                                   hover=False, button_color="white", from_=0, to=255)
slider_r.bind("<ButtonRelease-1>", lambda event: operation())
slider_r.set(255)
slider_r.grid(row=2, column=0, sticky="wen", pady=10, padx=20)

slider_b = customtkinter.CTkSlider(tabview.tab("Colors"), height=20, progress_color="blue",
                                   hover=False, button_color="white", from_=0, to=255)
slider_b.bind("<ButtonRelease-1>", lambda event: operation())
slider_b.grid(row=3, column=0, sticky="wen", pady=10, padx=20)
slider_b.set(255)

slider_g = customtkinter.CTkSlider(tabview.tab("Colors"), height=20, progress_color="green",
                                   hover=False, button_color="white", from_=0, to=255)
slider_g.bind("<ButtonRelease-1>", lambda event: operation())
slider_g.grid(row=4, column=0, sticky="wen", pady=10, padx=20)
slider_g.set(255)

label_6 = customtkinter.CTkLabel(tabview.tab("Colors"), text="Background:")
label_6.grid(row=5, column=0, sticky="wn", pady=10, padx=20)

def change_bg():
    # open my special color picker
    global background
    pick_color = CTkColorPicker.AskColor(fg_color="#1e2434", bg_color="#1b202c", button_color=app_color)
    pick_color.wm_iconbitmap()
    root.after(200, lambda: pick_color.iconphoto(False, icopath))

    color = pick_color.get()
    if color is None:
        return
    bg_color.configure(fg_color=color)
    background = color
    operation()

bg_color = customtkinter.CTkButton(tabview.tab("Colors"), corner_radius=20, fg_color="black", border_width=2,
                                         text="", hover=False, command=change_bg)
bg_color.grid(row=5, column=0, sticky="wn", padx=(100,20), pady=10)

label_7 = customtkinter.CTkLabel(tabview.tab("Colors"), text="Saturation:")
label_7.grid(row=6, column=0, sticky="wn", pady=10, padx=20)

slider_sat = customtkinter.CTkSlider(tabview.tab("Colors"), height=20, width=10, hover=False, button_color="white", from_=0, to=10)
slider_sat.set(1)
slider_sat.bind("<ButtonRelease-1>", lambda event: operation())
slider_sat.grid(row=6, column=0, sticky="wen", pady=15, padx=(100,20))

label_8 = customtkinter.CTkLabel(tabview.tab("Colors"), text="Brightness:")
label_8.grid(row=7, column=0, sticky="wn", pady=10, padx=20)

slider_br = customtkinter.CTkSlider(tabview.tab("Colors"), height=20, width=10, hover=False, button_color="white", from_=0, to=15)
slider_br.set(1)
slider_br.bind("<ButtonRelease-1>", lambda event: operation())
slider_br.grid(row=7, column=0, sticky="wen", pady=15, padx=(100,20))

automatic.toggle()

# TAB-3 (Fonts)
selected_font = ""

def change_font(font):
    # change selected font
    global selected_font
    selected_font = font
    operation()

def populate(frame):
    # load system fonts  (not all at once because it will lag)
    global loaded_fonts, all_fonts, l
    all_fonts = matplotlib.font_manager.findSystemFonts()

    l = len(all_fonts) if len(all_fonts)<100 else 50
    for filename in sorted(all_fonts)[:l]:
        if "Emoji" not in filename and "18030" not in filename:
            font_load = ImageFont.FreeTypeFont(filename)
            if (font_load.getname()[1]).lower()!="regular":
                name = " ".join(font_load.getname())
            else:
                name = font_load.getname()[0]
            try:
                label = customtkinter.CTkButton(frame, text=name, font=(name, 16), fg_color="#1b202c", text_color="white",
                                            anchor="w", command=lambda event=filename: change_font(event)).grid(sticky="w")
                loaded_fonts.append(name)
            except: pass
            
tabview.tab("Font").rowconfigure(0, weight=1)
tabview.tab("Font").columnconfigure(0, weight=1)

loaded_fonts = []

frame = customtkinter.CTkScrollableFrame(tabview.tab("Font"), fg_color="transparent")
frame.grid(padx=2, pady=2, sticky="news")

threading.Thread(target= lambda: populate(frame)).start()

tabview.tab("Export").rowconfigure(6, weight=1)
tabview.tab("Export").columnconfigure(0, weight=1)

def add_more_fonts():
    # load 50 more system fonts, not all at once because it will lag
    global loaded_fonts, l
    for filename in sorted(all_fonts)[l:l+50]:
        if "Emoji" not in filename and "18030" not in filename:
            font_load = ImageFont.FreeTypeFont(filename)
            if (font_load.getname()[1]).lower()!="regular":
                name = " ".join(font_load.getname())
            else:
                name = font_load.getname()[0]

            label = customtkinter.CTkButton(frame, text=name, font=(name, 16), fg_color="#1b202c", text_color="white",
                                                anchor="w", command=lambda event=filename: change_font(event)).grid(sticky="w")
            loaded_fonts.append(name)

    l+=50
    if l>len(all_fonts)-50:
        l = len(all_fonts)

def loadcustom():
    # load custom font file
    global selected_font
    if font_open := filedialog.askopenfilename(
        filetypes=[('Font Files', ['*.ttf', '*.otf', '*.TTF'])]
    ):
        selected_font = font_open
        operation()

load_more = customtkinter.CTkButton(tabview.tab("Font"), fg_color="#1b2f30", text="Load More", hover=False, command=add_more_fonts)
load_more.grid(row=1, sticky="sew", columnspan=2)

RightClickMenu3 = tk.Menu(frame_image, tearoff=False, background='#343e5a', fg='white', borderwidth=0, bd=0, activebackground=app_color)
RightClickMenu3.add_command(label="Load Font File", command=lambda: loadcustom())
load_more.bind("<Button-3>", lambda event: do_popup(event, frame=RightClickMenu3))

# TAB-4 (Export)
label_5 = customtkinter.CTkLabel(tabview.tab("Export"), text="Export As")
label_5.grid(row=0, column=0, sticky="wn", pady=10, padx=20)

var = tk.StringVar()
entry_save = customtkinter.CTkEntry(tabview.tab("Export"), textvariable=var, corner_radius=20, width=10)
entry_save.grid(row=1, column=0, sticky="ew", padx=(20, 100))
entry_save._entry.configure(selectbackground=app_color)

format_ = customtkinter.CTkComboBox(tabview.tab("Export"), values=["png", "jpg", "bmp"], width=75, corner_radius=20,
                                    state="readonly")
format_.grid(row=1, column=0, sticky="e", padx=20)
format_.set("png")

def changedir():
    global dir_
    dir_ = filedialog.askdirectory()
    if not dir_:
        return
    if len(dir_)>=30:
        entry_location.configure(text=f"{dir_[:25]}...{dir_[-5:]}")
    else:
        entry_location.configure(text=dir_)

def export():
    # Saving rendered images
    global file, convert_seq
    if not file:
        tk.messagebox.showinfo("Uh!","Please import an image!")
        return
    save.configure(state=tk.DISABLED, fg_color="grey30")
    open_button.configure(state=tk.DISABLED)
    if sequence is False:
        # single image save
        operation()
        exported_file = os.path.join(dir_, f"{var.get()}.{format_.get()}")
        if os.path.exists(exported_file):
            res1 = tk.messagebox.askquestion("Warning!","Do you want to replace the old file with the new one? \n(Process not reversible!)")
            if res1=='yes':
                outputImage.save(exported_file)
            elif res1=='no':
                save.configure(state="normal", fg_color=app_color)
                open_button.configure(state="normal")
                return
        else:
            outputImage.save(exported_file)
        tk.messagebox.showinfo("Exported", "Image successfully saved")

    else:
        new_dir = os.path.join(dir_, var.get())

        if os.path.exists(new_dir):
            tk.messagebox.showinfo("Warning!", "A folder with this name already exists, please try a new name!")
        else:
            label_11.grid(row=4, column=0, sticky="w", padx=25, pady=0)
            progress_bar.grid(row=5, column=0, sticky="we", padx=20, pady=(0,20))
            cancel_button.grid(row=4, column=0, sticky="ne", padx=(0,20))
            os.mkdir(new_dir)

            # image sequence
            count = 1
            for i in allitems:
                if convert_seq==False:
                    break
                progress_bar.set(count/len(allitems))
                label_11.configure(text=f"Frame: {str(count)}")
                file = i
                operation()
                exported_file = os.path.join(
                    new_dir,
                    f"{os.path.basename(file)[:-4]}_ascified.{format_.get()}",
                )
                outputImage.save(exported_file)
                count+=1

            tk.messagebox.showinfo("Exported", "Images successfully saved")
            convert_seq = True

        label_11.grid_forget()
        progress_bar.grid_forget()
        cancel_button.grid_forget()

    save.configure(state="normal", fg_color=app_color)
    open_button.configure(state="normal")

def new_window():
    # About window

    info.unbind("<Button-1>")

    def exit_top_level():
        top_level.destroy()
        info.bind("<Button-1>", lambda event: new_window())

    def web(link):
        webbrowser.open_new_tab(link)

    top_level = customtkinter.CTkToplevel(root)
    top_level.config(background="#1b202c")
    top_level.protocol("WM_DELETE_WINDOW", exit_top_level)
    top_level.minsize(400,200)
    top_level.title("About")
    top_level.transient(root)
    top_level.resizable(width=False, height=False)
    top_level.wm_iconbitmap()
    root.after(200, lambda: top_level.iconphoto(False, icopath))

    label_top = customtkinter.CTkLabel(top_level, fg_color="#1b202c", text="Ascify-Art v0.9", font=("Roboto",15))
    label_top.grid(padx=20, pady=20, sticky="w")

    desc = "Developed by Akash Bora (Akascape) \n \nLicense: MIT \nCopyright 2024"
    label_disc = customtkinter.CTkLabel(top_level, fg_color="#1b202c", text=desc, justify="left", font=("Roboto",12))
    label_disc.grid(padx=20, pady=0, sticky="w")

    label_logo = customtkinter.CTkLabel(top_level, text="", image=logo, bg_color="#1b202c")
    label_logo.place(x=230,y=30)

    link = customtkinter.CTkLabel(top_level, fg_color="#1b202c", text="Official Page", justify="left", font=("",13), text_color="light blue")
    link.grid(padx=20, pady=0, sticky="w")
    link.bind("<Button-1>", lambda event: web("https://github.com/Akascape/Ascify-Art"))
    link.bind("<Enter>", lambda event: link.configure(font=("", 13, "underline"), cursor="hand2"))
    link.bind("<Leave>", lambda event: link.configure(font=("", 13), cursor="arrow"))

    link2 = customtkinter.CTkLabel(top_level, fg_color="#1b202c", text="Documentation", justify="left", anchor="n", font=("",13), text_color="light blue")
    link2.grid(padx=20, pady=0, sticky="nw")
    link2.bind("<Button-1>", lambda event: web("https://github.com/Akascape/Ascify-Art/wiki"))
    link2.bind("<Enter>", lambda event: link2.configure(font=("", 13, "underline"), cursor="hand2"))
    link2.bind("<Leave>", lambda event: link2.configure(font=("", 13), cursor="arrow"))

logo = customtkinter.CTkImage(Image.open(resource("icon.png")), size=(150,150))

entry_location = customtkinter.CTkButton(tabview.tab("Export"), corner_radius=20, width=10, fg_color="#343638", border_width=2,
                                         text="Browse Location", hover=False, command=changedir)
entry_location.grid(row=2, column=0, sticky="ew", padx=20, pady=20)

label_11 = customtkinter.CTkLabel(tabview.tab("Export"), text="Frame: 1")
progress_bar = customtkinter.CTkProgressBar(tabview.tab("Export"), height=20, width=10, progress_color=app_color)
progress_bar.set(0)

save = customtkinter.CTkButton(tabview.tab("Export"), corner_radius=20, width=10, fg_color=app_color,
                                         text="SAVE", hover=False, command=lambda: threading.Thread(target=export).start())
save.grid(row=3, column=0, sticky="ew", padx=20, pady=20)

root.bind("<Control-s>", lambda e: threading.Thread(target=export).start())

def stop_sequence():
    # stop sequence conversion
    global convert_seq
    convert_seq = False

convert_seq = True

cancel_button = customtkinter.CTkButton(tabview.tab("Export"), text="x", width=10, height=20, corner_radius=10,
                                        fg_color="grey30", hover_color=app_color, command=stop_sequence)

info = customtkinter.CTkLabel(tabview.tab("Export"), text="About", font=("",13))

info.bind("<Button-1>", lambda event: new_window())
info.bind("<Enter>", lambda event: info.configure(font=("", 13, "underline"), cursor="hand2"))
info.bind("<Leave>", lambda event: info.configure(font=("", 13), cursor="arrow"))
info.grid(row=6, column=0, sticky="sw", padx=20, pady=20)

root.mainloop()
#------------------------------------------------------------------------------------------------#
