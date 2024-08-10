from tkinter import Tk, Label, Button, Frame
from tkinter import ttk
from configs.config import BG, FG
from configs.offsets import (
    BASE_ADDRESS_ARMOR, OFFSETS_ARMOR, BASE_ADDRESS_HEALTH, OFFSETS_HEALTH
)
import pygetwindow as gw
import pyautogui
from threading import Thread, Event
from time import sleep

class ModMenu:
    def __init__(self, window_title, width, height, mem_handler):
        self.mem_handler = mem_handler
        self.width = width
        self.height = height
        self.win = Tk()
        self.win.overrideredirect(True)  # Loại bỏ viền cửa sổ
        self.win.attributes("-topmost", True)  # Luôn ở trên cùng
        self.win.attributes("-alpha", 0.9)  # Độ trong suốt
        self.win.configure(background=BG)

        self.current_selection = 0
        self.options = ['draw_box', 'draw_name', 'draw_health', 'life_hack', 'armor_hack', 'exit']
        self.option_labels = {}

        self.life_hack_active = False
        self.armor_hack_active = False

        self.draw_box_active = False
        self.draw_name_active = False
        self.draw_health_active = False

        self.game_running = True

        self.create_widgets(window_title)
        self.start_tracking_position()  # Bắt đầu theo dõi vị trí của cửa sổ game
        self.threads = []

        self.win.bind("<Up>", self.navigate)
        self.win.bind("<Down>", self.navigate)
        self.win.bind("<Left>", self.toggle_option)
        self.win.bind("<Right>", self.toggle_option)
        self.win.bind("<Return>", self.execute_option)  # Thêm phím Enter để kích hoạt nút

    def create_widgets(self, window_title):
        title_frame = Frame(self.win, bg=BG)
        title_frame.pack(pady=10)

        self.title_label = Label(title_frame, text=window_title, font=('Helvetica', 16, 'bold'), bg=BG, fg=FG)
        self.title_label.pack()

        notebook = ttk.Notebook(self.win)
        notebook.pack(pady=10, padx=10, expand=True, fill='both')

        tab1 = Frame(notebook, bg=BG)

        notebook.add(tab1, text='Tab 1')

        self.option_labels['draw_box'] = Label(tab1, text="Draw Box: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['draw_box'].pack(pady=5, fill='x')

        self.option_labels['draw_name'] = Label(tab1, text="Draw Name: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['draw_name'].pack(pady=5, fill='x')

        self.option_labels['draw_health'] = Label(tab1, text="Draw Health: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['draw_health'].pack(pady=5, fill='x')

        self.option_labels['life_hack'] = Label(tab1, text="Health Hack: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['life_hack'].pack(pady=5, fill='x')

        self.option_labels['armor_hack'] = Label(tab1, text="Armor Hack: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['armor_hack'].pack(pady=5, fill='x')

        self.option_labels['exit'] = Button(self.win, text="Exit", font=('Helvetica', 14), bg=BG, fg=FG,
                               command=self.exit_program, width=20)
        self.option_labels['exit'].pack(pady=20, fill='x')

    def navigate(self, event):
        if event.keysym == "Up":
            self.current_selection = (self.current_selection - 1) % len(self.options)
        elif event.keysym == "Down":
            self.current_selection = (self.current_selection + 1) % len(self.options)
        self.update_selection()

    def toggle_option(self, event):
        option = self.options[self.current_selection]
        if option == 'draw_box':
            self.draw_box_active = not self.draw_box_active
            state = "ON" if self.draw_box_active else "OFF"
            self.option_labels['draw_box'].config(text=f"Draw Box: {state}")
        elif option == 'draw_name':
            self.draw_name_active = not self.draw_name_active
            state = "ON" if self.draw_name_active else "OFF"
            self.option_labels['draw_name'].config(text=f"Draw Name: {state}")
        elif option == 'draw_health':
            self.draw_health_active = not self.draw_health_active
            state = "ON" if self.draw_health_active else "OFF"
            self.option_labels['draw_health'].config(text=f"Draw Health: {state}")
        elif option == 'life_hack':
            self.life_hack_active = not self.life_hack_active
            state = "ON" if self.life_hack_active else "OFF"
            self.option_labels['life_hack'].config(text=f"Health Hack: {state}")
            if self.life_hack_active:
                self.start_thread(self.life_hack)
        elif option == 'armor_hack':
            self.armor_hack_active = not self.armor_hack_active
            state = "ON" if self.armor_hack_active else "OFF"
            self.option_labels['armor_hack'].config(text=f"Armor Hack: {state}")
            if self.armor_hack_active:
                self.start_thread(self.armor_hack)

    def execute_option(self, event):
        option = self.options[self.current_selection]
        if option == 'exit':
            self.exit_program()

    def update_selection(self):
        for i, option in enumerate(self.options):
            label = self.option_labels[option]
            if i == self.current_selection:
                label.config(bg='#4CAF50', fg='white')
            else:
                label.config(bg=BG, fg=FG)

    def update_position(self):
        try:
            game_window = gw.getWindowsWithTitle('AssaultCube')[0]
            x = game_window.left + (game_window.width - self.width) // 2
            y = game_window.top + (game_window.height - self.height) // 2
        except IndexError:
            screen_width, screen_height = pyautogui.size()
            x = (screen_width - self.width) // 2
            y = (screen_height - self.height) // 2
        self.win.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def start_tracking_position(self):
        def track_position():
            while self.game_running:
                self.update_position()
                sleep(0.1)  # Cập nhật vị trí mỗi 100ms

        track_thread = Thread(target=track_position, daemon=True)
        track_thread.start()

    def life_hack(self):
        while self.life_hack_active and self.game_running:
            try:
                self.mem_handler.write_value(BASE_ADDRESS_HEALTH, OFFSETS_HEALTH, 199)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False
                break
            sleep(0.1)

    def armor_hack(self):
        while self.armor_hack_active and self.game_running:
            try:
                self.mem_handler.write_value(BASE_ADDRESS_ARMOR, OFFSETS_ARMOR, 199)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False
                break
            sleep(0.1)

    def start_thread(self, target):
        thread = Thread(target=target)
        thread.start()
        self.threads.append(thread)

    def stop_hacks(self):
        self.life_hack_active = False
        self.armor_hack_active = False

        for thread in self.threads:
            thread.join()

    def exit_program(self):
        self.game_running = False  # Ngừng theo dõi vị trí
        self.stop_hacks()
        self.win.destroy()
