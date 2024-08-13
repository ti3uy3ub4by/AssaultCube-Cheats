import pygetwindow as gw
import pyautogui
from threading import Thread
from time import sleep
from tkinter import Tk, Label, Button, Frame
from tkinter import ttk
from configs.config import BG, FG
import keyboard
from configs.offsets import Pointer, Offsets, FastFireOffsets


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

        self.visible = False  # Trạng thái hiển thị menu

        self.current_selection = 0
        self.options = ['life_hack', 'draw_box', 'draw_name', 'draw_health', 'draw_line', 'fast_shoot', 'fast_knife', 'exit']
        self.option_labels = {}

        self.life_hack_active = False
        self.fast_shoot_active = False
        self.fast_knife_active = False


        self.draw_box_active = False
        self.draw_name_active = False
        self.draw_health_active = False
        self.draw_line_active = False

        self.game_running = True

        self.create_widgets(window_title)
        self.threads = []

        self.win.bind("<Up>", self.navigate)
        self.win.bind("<Down>", self.navigate)
        self.win.bind("<Left>", self.toggle_option)
        self.win.bind("<Right>", self.toggle_option)
        self.win.bind("<Return>", self.execute_option)

        # Bắt đầu lắng nghe phím F1
        self.start_key_listener()

    def create_widgets(self, window_title):
        title_frame = Frame(self.win, bg=BG)
        title_frame.pack(pady=10)

        self.title_label = Label(title_frame, text=window_title, font=('Helvetica', 16, 'bold'), bg=BG, fg=FG)
        self.title_label.pack()

        notebook = ttk.Notebook(self.win)
        notebook.pack(pady=10, padx=10, expand=True, fill='both')

        tab1 = Frame(notebook, bg=BG)

        notebook.add(tab1, text='Tab 1')

        self.option_labels['life_hack'] = Label(tab1, text="Health Hack: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['life_hack'].pack(pady=5, fill='x')

        self.option_labels['draw_box'] = Label(tab1, text="Draw Box: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['draw_box'].pack(pady=5, fill='x')

        self.option_labels['draw_name'] = Label(tab1, text="Draw Name: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['draw_name'].pack(pady=5, fill='x')

        self.option_labels['draw_health'] = Label(tab1, text="Draw Health: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['draw_health'].pack(pady=5, fill='x')

        self.option_labels['draw_line'] = Label(tab1, text="Draw Line: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['draw_line'].pack(pady=5, fill='x')

        self.option_labels['fast_shoot'] = Label(tab1, text="Fast Shoot: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['fast_shoot'].pack(pady=5, fill='x')

        self.option_labels['fast_knife'] = Label(tab1, text="Fast Knife: OFF", font=('Helvetica', 14), bg=BG, fg=FG)
        self.option_labels['fast_knife'].pack(pady=5, fill='x')

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
        if option == 'life_hack':
            self.life_hack_active = not self.life_hack_active
            state = "ON" if self.life_hack_active else "OFF"
            self.option_labels['life_hack'].config(text=f"Health Hack: {state}")
            if self.life_hack_active:
                self.start_thread(self.life_hack)
        elif option == 'draw_box':
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
        elif option == 'draw_line':
            self.draw_line_active = not self.draw_line_active
            state = "ON" if self.draw_line_active else "OFF"
            self.option_labels['draw_line'].config(text=f"Draw Line: {state}")
        elif option == 'fast_shoot':
            self.fast_shoot_active = not self.fast_shoot_active
            state = "ON" if self.fast_shoot_active else "OFF"
            self.option_labels['fast_shoot'].config(text=f"Fast Shoot: {state}")
            if self.fast_shoot_active:
                self.start_thread(self.fast_shoot)
        elif option == 'fast_knife':
            self.fast_knife_active = not self.fast_knife_active
            state = "ON" if self.fast_knife_active else "OFF"
            self.option_labels['fast_knife'].config(text=f"Fast Knife: {state}")
            if self.fast_knife_active:
                self.start_thread(self.fast_knife)

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

    def toggle_visibility(self):
        if self.visible:
            self.win.withdraw()
        else:
            self.update_position()
            self.win.deiconify()
            self.win.focus_force()
        self.visible = not self.visible

    def start_key_listener(self):
        def listen_f1():
            while self.game_running:
                if keyboard.is_pressed("F1"):
                    self.toggle_visibility()
                    sleep(0.3)  # Tránh việc toggle quá nhanh

        key_thread = Thread(target=listen_f1, daemon=True)
        key_thread.start()

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

    def life_hack(self):
        while self.life_hack_active and self.game_running:
            try:
                self.mem_handler.write_value(Pointer.local_player, [Offsets.health], 101)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False
                break
            sleep(0.1)

    def fast_shoot(self):
        while self.fast_shoot_active and self.game_running:
            try:
                for offset in [FastFireOffsets.assault_rifle, FastFireOffsets.sniper, FastFireOffsets.shotgun]:
                    self.mem_handler.write_value(Pointer.local_player, [offset], 0)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False
                break
            sleep(0.1)

    def fast_knife(self):
        while self.fast_knife_active and self.game_running:
            try:
                self.mem_handler.write_value(Pointer.local_player, [Offsets.knife_speed], 0)
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
        self.fast_shoot_active = False
        self.fast_knife_active = False

        for thread in self.threads:
            thread.join()

    def exit_program(self):
        self.game_running = False
        self.stop_hacks()
        for thread in self.threads:
            thread.join(timeout=1)
        self.win.destroy()