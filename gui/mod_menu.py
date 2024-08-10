from tkinter import Tk, Label, Button, Frame
from tkinter import ttk
from configs.config import BG, FG
from configs.offsets import (
    BASE_ADDRESS_ARMOR, BASE_ADDRESS_LUKE,
    BASE_ADDRESS_SPLASER, OFFSETS_ARMOR, OFFSETS_LUKE,
    OFFSETS_SPLASER, BASE_ADDRESS_HEALTH, OFFSETS_HEALTH
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
        self.update_position()
        self.win.overrideredirect(True)  # Remove the window border
        self.win.attributes("-topmost", True)  # Always on top
        self.win.attributes("-alpha", 0.9)  # Semi-transparent
        self.win.configure(background=BG)

        self.create_widgets(window_title)

        self.life_hack_active = Event()
        self.armor_hack_active = Event()
        self.luke_hack_active = Event()
        self.splaser_hack_active = Event()
        self.orbs_hack_active = Event()
        self.game_running = True

        self.threads = []

    def create_widgets(self, window_title):
        # Frame for title
        title_frame = Frame(self.win, bg=BG)
        title_frame.pack(pady=10)

        self.title_label = Label(title_frame, text=window_title, font=('Helvetica', 16, 'bold'), bg=BG, fg=FG)
        self.title_label.pack()

        # Creating Notebook for tabs
        notebook = ttk.Notebook(self.win)
        notebook.pack(pady=10, padx=10, expand=True, fill='both')

        # Frame for each tab
        tab1 = Frame(notebook, bg=BG)
        tab2 = Frame(notebook, bg=BG)

        notebook.add(tab1, text='Tab 1')

        # Adding buttons to Tab 1
        self.life_btn = Button(tab1, text="Enable Health Hack", font=('Helvetica', 14), bg='#4CAF50', fg='white',
                               command=self.toggle_life_hack, width=20)
        self.life_btn.pack(pady=5, fill='x')

        self.armor_btn = Button(tab1, text="Enable Armor Hack", font=('Helvetica', 14), bg='#4CAF50', fg='white',
                                command=self.toggle_armor_hack, width=20)
        self.armor_btn.pack(pady=5, fill='x')

        self.luke_btn = Button(tab1, text="Enable Luke Hack", font=('Helvetica', 14), bg='#4CAF50', fg='white',
                               command=self.toggle_luke_hack, width=20)
        self.luke_btn.pack(pady=5, fill='x')

        self.splaser_btn = Button(tab1, text="Enable Splaser Hack", font=('Helvetica', 14), bg='#4CAF50', fg='white',
                                  command=self.toggle_splaser_hack, width=20)
        self.splaser_btn.pack(pady=5, fill='x')

        self.orbs_btn = Button(tab2, text="Max Orbs Hack", font=('Helvetica', 14), bg='#4CAF50', fg='white',
                               command=self.orbs_hack, width=20)
        self.orbs_btn.pack(pady=5, fill='x')

    def update_position(self):
        try:
            # Try to get the game window position and size
            game_window = gw.getWindowsWithTitle('AssaultCube')[0]
            x = game_window.left + (game_window.width - self.width) // 2
            y = game_window.top + (game_window.height - self.height) // 2
        except IndexError:
            # If the game window is not found, center the menu on the primary screen
            screen_width, screen_height = pyautogui.size()
            x = (screen_width - self.width) // 2
            y = (screen_height - self.height) // 2
        self.win.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def toggle_life_hack(self):
        if self.life_hack_active.is_set():
            self.life_hack_active.clear()
            self.life_btn.config(text="Enable Health Hack")
        else:
            self.life_hack_active.set()
            self.life_btn.config(text="Disable Health Hack")
            self.start_thread(self.life_hack)

    def toggle_armor_hack(self):
        if self.armor_hack_active.is_set():
            self.armor_hack_active.clear()
            self.armor_btn.config(text="Enable Armor Hack")
        else:
            self.armor_hack_active.set()
            self.armor_btn.config(text="Disable Armor Hack")
            self.start_thread(self.armor_hack)

    def toggle_luke_hack(self):
        if self.luke_hack_active.is_set():
            self.luke_hack_active.clear()
            self.luke_btn.config(text="Enable Luke Hack")
        else:
            self.luke_hack_active.set()
            self.luke_btn.config(text="Disable Luke Hack")
            self.start_thread(self.luke_hack)

    def toggle_splaser_hack(self):
        if self.splaser_hack_active.is_set():
            self.splaser_hack_active.clear()
            self.splaser_btn.config(text="Enable Splaser Hack")
        else:
            self.splaser_hack_active.set()
            self.splaser_btn.config(text="Disable Splaser Hack")
            self.start_thread(self.splaser_hack)

    def life_hack(self):
        while self.life_hack_active.is_set() and self.game_running:
            try:
                self.mem_handler.write_value(BASE_ADDRESS_HEALTH, OFFSETS_HEALTH, 200)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False
                break
            sleep(0.1)  # Short sleep to prevent high CPU usage

    def armor_hack(self):
        while self.armor_hack_active.is_set() and self.game_running:
            try:
                self.mem_handler.write_value(BASE_ADDRESS_ARMOR, OFFSETS_ARMOR, 4)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False
                break
            sleep(0.1)  # Short sleep to prevent high CPU usage

    def luke_hack(self):
        while self.luke_hack_active.is_set() and self.game_running:
            try:
                self.mem_handler.write_value(BASE_ADDRESS_LUKE, OFFSETS_LUKE, 5)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False
                break
            sleep(0.1)  # Short sleep to prevent high CPU usage

    def splaser_hack(self):
        while self.splaser_hack_active.is_set() and self.game_running:
            try:
                self.mem_handler.write_value(BASE_ADDRESS_SPLASER, OFFSETS_SPLASER, 3000)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False
                break
            sleep(0.1)  # Short sleep to prevent high CPU usage

    def orbs_hack(self):
        if self.game_running:
            try:
                self.mem_handler.write_value(BASE_ADDRESS_ORBS, OFFSETS_ORBS, 3)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False

    def start_thread(self, target):
        thread = Thread(target=target)
        thread.start()
        self.threads.append(thread)

    def stop_hacks(self):
        self.life_hack_active.clear()
        self.armor_hack_active.clear()
        self.luke_hack_active.clear()
        self.splaser_hack_active.clear()
        self.orbs_hack_active.clear()

        for thread in self.threads:
            thread.join()

    def exit_program(self):
        self.stop_hacks()
        self.win.destroy()
