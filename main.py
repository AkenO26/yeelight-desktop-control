import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
import yeelight as yl
from yeelight.flows import *


def main():
    file = open("bulbIP.txt", "r")
    text = file.read()

    while validate_ip(text) != True:
        get_bulbIP()
        file.close()
        file = open("bulbIP.txt", "r")
        text = file.read()
    file.close()
    bulb = yl.Bulb(text)

    main_window = tk.Tk()
    main_window.title("Yeelight quick control panel")
    w = 600
    h = 300
    main_window.minsize(w, h)
    main_window.maxsize(w, h)
    ws = main_window.winfo_screenwidth()
    hs = main_window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    main_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    main_window.iconbitmap("images/myIcon.ico")

    color_picker_button_image = tk.PhotoImage(file="images/color_picker_button.png")
    switch_off_img = tk.PhotoImage(file="images/switch-off.png")
    switch_on_img = tk.PhotoImage(file="images/switch-on.png")
    yellow_light_button_image = tk.PhotoImage(file="images/yellow_button.png")
    normal_light_button_image = tk.PhotoImage(file="images/normal_button.png")
    white_light_button_image = tk.PhotoImage(file="images/white_button.png")

    def switch_btn_pressed():
        bulb.toggle()
        if bulb.get_properties()["power"] == "off":
            button.config(image=switch_off_img, borderwidth=0)
        else:
            button.config(image=switch_on_img, borderwidth=0)

    def init_btn_pressed():
        if bulb.get_properties()["power"] == "off":
            return switch_off_img
        else:
            return switch_on_img

    button = tk.Button(main_window, image=init_btn_pressed(), command=switch_btn_pressed, height=95, borderwidth=0)
    button.place(x=370, y=50)

    def scale_to_bulb(val):
        bulb.set_brightness(int(val))
        print(bulb.get_properties()["bright"])

    brightness_scale = tk.Scale(main_window, orient="horizontal", from_=0, to=100, length=500, width=30, showvalue=0,
                                command=scale_to_bulb,
                                resolution=10, bg="#8BFFC7", borderwidth=0, activebackground="#8BFFC7",
                                sliderrelief="flat", troughcolor="#C4C4C4")
    brightness_scale.place(x=50, y=250)
    brightness_scale.set(bulb.get_properties()["bright"])

    OPTIONS = [
        "Default",
        "Alarm",
        "Candle flicker",
        "Christmas",
        "Date night",
        "Disco",
        "Happy birthday",
        "Home",
        "LSD",
        "Movie",
        "Night mode",
        "Police",
        "Police 2",
        "Random loop",
        "RGB",
        "Romance",
        "Slowdown",
        "Strobe",
        "Strobe color",
        "Sunrise",
        "Sunset",
        "Temp"
    ]

    variable = tk.StringVar(main_window)
    variable.set(OPTIONS[0])

    def ok(event):
        if combobox_dropdown.get() == "Alarm":
            bulb.start_flow(yl.flows.alarm(duration=250))
        elif combobox_dropdown.get() == "Candle flicker":
            bulb.start_flow(yl.flows.candle_flicker())
        elif combobox_dropdown.get() == "Christmas":
            bulb.start_flow(yl.flows.christmas(duration=250, brightness=100, sleep=3000))
        elif combobox_dropdown.get() == "Date night":
            bulb.start_flow(yl.flows.date_night(duration=500, brightness=50))
        elif combobox_dropdown.get() == "Disco":
            bulb.start_flow(yl.flows.disco(bpm=120))
        elif combobox_dropdown.get() == "Happy birthday":
            bulb.start_flow(yl.flows.happy_birthday())
        elif combobox_dropdown.get() == "Home":
            bulb.start_flow(yl.flows.home(duration=500, brightness=80))
        elif combobox_dropdown.get() == "LSD":
            bulb.start_flow(yl.flows.lsd(duration=3000, brightness=100))
        elif combobox_dropdown.get() == "Movie":
            bulb.start_flow(yl.flows.movie(duration=500, brightness=50))
        elif combobox_dropdown.get() == "Night mode":
            bulb.start_flow(yl.flows.night_mode(duration=500, brightness=1))
        elif combobox_dropdown.get() == "Police":
            bulb.start_flow(yl.flows.police(duration=300, brightness=100))
        elif combobox_dropdown.get() == "Police2":
            bulb.start_flow(yl.flows.police2(duration=250, brightness=100))
        elif combobox_dropdown.get() == "Random loop":
            bulb.start_flow(yl.flows.random_loop(duration=750, brightness=100, count=9))
        elif combobox_dropdown.get() == "RGB":
            bulb.start_flow(yl.flows.rgb(duration=250, brightness=100, sleep=3000))
        elif combobox_dropdown.get() == "Romance":
            bulb.start_flow(yl.flows.romance())
        elif combobox_dropdown.get() == "Slowdown":
            bulb.start_flow(yl.flows.slowdown(duration=2000, brightness=100, count=8))
        elif combobox_dropdown.get() == "Strobe":
            bulb.start_flow(yl.flows.strobe())
        elif combobox_dropdown.get() == "Strobe color":
            bulb.start_flow(yl.flows.strobe_color(brightness=100))
        elif combobox_dropdown.get() == "Sunrise":
            bulb.start_flow(yl.flows.sunrise())
        elif combobox_dropdown.get() == "Sunset":
            bulb.start_flow(yl.flows.sunset())
        elif combobox_dropdown.get() == "Temp":
            bulb.start_flow(yl.flows.temp())
        elif combobox_dropdown.get() == "Default":
            bulb.stop_flow()

    def defocus(event):
        event.widget.master.focus_set()

    combobox_dropdown = ttk.Combobox(main_window, state="readonly", value=OPTIONS, justify="center", width=15)
    combobox_dropdown.current(0)

    combobox_dropdown.bind("<<ComboboxSelected>>", ok)
    combobox_dropdown.bind("<FocusIn>", defocus)
    combobox_dropdown.place(x=20, y=90)

    combobox_dropdown.option_add("*TCombobox*Listbox.selectBackground", "#8BFFC7")
    combobox_dropdown.option_add("*TCombobox*Listbox.selectForeground", "black")

    def color():
        color = colorchooser.askcolor()[0]
        print([0])
        bulb.set_rgb(color[0], color[1], color[2])

    color_picker_button = tk.Button(main_window, image=color_picker_button_image, borderwidth=0, command=color)

    color_picker_button.place(x=150, y=50)

    yellow_light_button = tk.Button(main_window, image=yellow_light_button_image,
                                    command=lambda: bulb.set_color_temp(3123), height=95, borderwidth=0)
    yellow_light_button.place(x=50, y=150)

    normal_light_button = tk.Button(main_window, image=normal_light_button_image,
                                    command=lambda: bulb.set_color_temp(4003), height=95, borderwidth=0)
    normal_light_button.place(x=220, y=150)

    blue_light_button = tk.Button(main_window, image=white_light_button_image,
                                  command=lambda: bulb.set_color_temp(5276), height=95, borderwidth=0)
    blue_light_button.place(x=400, y=150)

    main_window.mainloop()


def get_bulbIP():
    splash_window = tk.Tk()
    splash_window.title("Bulb setup")
    w = 350
    h = 150
    splash_window.minsize(w, h)
    splash_window.maxsize(w, h)
    ws = splash_window.winfo_screenwidth()
    hs = splash_window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    splash_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    splash_window.iconbitmap("images/myIcon.ico")

    set_button_image = tk.PhotoImage(file="images/set.png")

    label = tk.Label(splash_window, text="Please set the bulb IP : ")
    label.pack(padx=5, pady=5, side="left")

    IP = tk.StringVar()
    entry = tk.Entry(splash_window, width=20, textvariable=IP)
    entry.pack(padx=5, pady=5, side="left")
    entry.focus_force()

    def save_bulb():
        bulb = entry.get()
        with open("bulbIP.txt", "w") as reader:
            reader.truncate(0)
            reader.write(bulb)
        splash_window.destroy()

    set_btn = tk.Button(splash_window, image=set_button_image, borderwidth=0, command=save_bulb)
    set_btn.pack(padx=5, pady=5, side="left")

    splash_window.mainloop()


def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


main()
