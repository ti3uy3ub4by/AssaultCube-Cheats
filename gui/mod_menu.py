import pygetwindow as gw
import pyautogui
from threading import Thread
from time import sleep
from tkinter import Tk, Label, Frame
from tkinter import ttk
from configs.config import BG, FG
import keyboard
from configs.offsets import Pointer, Offsets, FastFireOffsets, AmmoOffsets


class ModMenu:
    def __init__(self, window_title, width, height, mem_handler):
        self.mem_handler = mem_handler
        self.width = width
        self.height = height
        self.win = Tk()
        self.win.overrideredirect(True)  # Loại bỏ viền cửa sổ
        self.win.attributes("-topmost", True)  # Luôn ở trên cùng
        self.win.attributes("-alpha", 0.7)  # Độ trong suốt
        self.win.configure(background=BG)

        self.visible = False  # Trạng thái hiển thị menu

        self.current_selection = 0
        self.options = ['life_hack', 'draw_box', 'draw_name', 'draw_health',
                        'draw_line', 'fast_shoot', 'fast_knife', 'fast_walk', 'set_ammo', 'exit']
        self.option_labels = {}

        self.life_hack_active = False
        self.fast_shoot_active = False
        self.fast_knife_active = False
        self.fast_walk_active = False
        self.set_ammo_active = False

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
        # Tạo tiêu đề
        title_label = Label(self.win, text=window_title, font=('Helvetica', 14, 'bold'), bg=BG, fg='white')
        title_label.pack(pady=5)

        # Nhóm Health Functions
        self.create_group("Health Functions", [
            ('life_hack', "Infinity Health")
        ])

        # Nhóm Visual Functions
        self.create_group("Visual Functions", [
            ('draw_box', "Draw Box"),
            ('draw_name', "Draw Name"),
            ('draw_health', "Draw Health"),
            ('draw_line', "Draw Line")
        ])

        # Nhóm Memory Functions
        self.create_group("Memory Functions", [
            ('fast_shoot', "Fast Shoot"),
            ('fast_knife', "Fast Knife"),
            ('fast_walk', "Fast Walk"),
            ('set_ammo', "Set Ammo")
        ])

        # Nút Exit
        exit_button = Label(self.win, text="Exit", font=('Helvetica', 14, 'bold'), bg=BG, fg='red')
        exit_button.pack(pady=10)
        self.option_labels['exit'] = exit_button

    def create_group(self, group_name, options):
        group_frame = Frame(self.win, bg=BG)
        group_frame.pack(fill='x', padx=10, pady=5)

        group_label = Label(group_frame, text=f"[{group_name}]", font=('Helvetica', 12, 'bold'), fg='yellow', bg=BG)
        group_label.pack(anchor='w')

        for option_key, option_text in options:
            option_frame = Frame(group_frame, bg=BG)
            option_frame.pack(fill='x', padx=10, pady=2)

            option_name_label = Label(option_frame, text=option_text, font=('Helvetica', 10), bg=BG, fg=FG)
            option_name_label.pack(side='left')

            self.option_labels[option_key] = Label(option_frame, text="OFF", font=('Helvetica', 10), bg=BG, fg=FG)
            self.option_labels[option_key].pack(side='right')

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
            if self.life_hack_active:
                self.option_labels['life_hack'].config(text="ON", fg="green")
                self.start_thread(self.life_hack)  # Khởi chạy thread
            else:
                self.option_labels['life_hack'].config(text="OFF", fg="red")

        elif option == 'draw_box':
            self.draw_box_active = not self.draw_box_active
            if self.draw_box_active:
                self.option_labels['draw_box'].config(text="ON", fg="green")
            else:
                self.option_labels['draw_box'].config(text="OFF", fg="red")

        elif option == 'draw_name':
            self.draw_name_active = not self.draw_name_active
            if self.draw_name_active:
                self.option_labels['draw_name'].config(text="ON", fg="green")
            else:
                self.option_labels['draw_name'].config(text="OFF", fg="red")

        elif option == 'draw_health':
            self.draw_health_active = not self.draw_health_active
            if self.draw_health_active:
                self.option_labels['draw_health'].config(text="ON", fg="green")
            else:
                self.option_labels['draw_health'].config(text="OFF", fg="red")

        elif option == 'draw_line':
            self.draw_line_active = not self.draw_line_active
            if self.draw_line_active:
                self.option_labels['draw_line'].config(text="ON", fg="green")
            else:
                self.option_labels['draw_line'].config(text="OFF", fg="red")

        elif option == 'fast_shoot':
            self.fast_shoot_active = not self.fast_shoot_active
            if self.fast_shoot_active:
                self.option_labels['fast_shoot'].config(text="ON", fg="green")
                self.start_thread(self.fast_shoot)  # Khởi chạy thread
            else:
                self.option_labels['fast_shoot'].config(text="OFF", fg="red")

        elif option == 'fast_knife':
            self.fast_knife_active = not self.fast_knife_active
            if self.fast_knife_active:
                self.option_labels['fast_knife'].config(text="ON", fg="green")
                self.start_thread(self.fast_knife)  # Khởi chạy thread
            else:
                self.option_labels['fast_knife'].config(text="OFF", fg="red")

        elif option == 'fast_walk':
            self.fast_walk_active = not self.fast_walk_active
            if self.fast_walk_active:
                self.option_labels['fast_walk'].config(text="ON", fg="green")
                self.start_thread(self.fast_walk)  # Khởi chạy thread
            else:
                self.option_labels['fast_walk'].config(text="OFF", fg="red")

        elif option == 'set_ammo':
            self.set_ammo_active = not self.set_ammo_active
            if self.set_ammo_active:
                self.option_labels['set_ammo'].config(text="ON", fg="green")
                self.start_thread(self.set_ammo)  # Khởi chạy thread
            else:
                self.option_labels['set_ammo'].config(text="OFF", fg="red")

    def execute_option(self, event):
        option = self.options[self.current_selection]
        if option == 'exit':
            self.exit_program()

    def update_selection(self):
        for i, option in enumerate(self.options):
            label = self.option_labels[option]
            if i == self.current_selection:
                label.config(bg='#4CAF50')  # Chỉ thay đổi màu nền khi được chọn
            else:
                label.config(bg=BG)  # Khôi phục màu nền khi không được chọn

            # Giữ nguyên màu sắc fg đã thiết lập trong toggle_option
            if getattr(self, f"{option}_active", False):
                label.config(fg="green")
            elif option != 'exit':  # Chỉ đặt lại màu đỏ nếu không phải là nút 'exit'
                label.config(fg="red")

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
                    sleep(0.9)  # Tránh việc toggle quá nhanh

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

    def fast_walk(self):
        speed_boost_active = False
        try:
            while self.fast_walk_active and self.game_running:
                if keyboard.is_pressed('shift') and not speed_boost_active:
                    self.mem_handler.write_value(Pointer.local_player, [Offsets.walk_speed], 3)
                    speed_boost_active = True
                elif not keyboard.is_pressed('shift') and speed_boost_active:
                    self.mem_handler.write_value(Pointer.local_player, [Offsets.walk_speed], 0)
                    speed_boost_active = False
                sleep(0.1)
        except Exception as e:
            print(f"Error setting walk speed: {e}")

    def set_ammo(self):
        while self.set_ammo_active and self.game_running:
            try:
                if keyboard.is_pressed('1'):  # Kiểm tra nếu phím '1' được nhấn
                    for offset in [AmmoOffsets.assault_rifle, AmmoOffsets.sniper, AmmoOffsets.shotgun,
                                   AmmoOffsets.pistol,
                                   AmmoOffsets.submachine_gun, AmmoOffsets.grenade]:
                        self.mem_handler.write_value(Pointer.local_player, [offset], 99)
                    sleep(0.5)
            except Exception as e:
                print(f"Error reading memory: {e}")
                self.game_running = False

    def start_thread(self, target):
        thread = Thread(target=target)
        thread.start()
        self.threads.append(thread)

    def stop_hacks(self):
        self.life_hack_active = False
        self.fast_shoot_active = False
        self.fast_knife_active = False
        self.fast_walk_active = False
        self.set_ammo_active = False

        for thread in self.threads:
            thread.join()

    def exit_program(self):
        self.game_running = False
        self.stop_hacks()
        for thread in self.threads:
            thread.join(timeout=1)
        self.win.destroy()
