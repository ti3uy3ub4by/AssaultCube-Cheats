import pyMeow as pm
from gui.mod_menu import ModMenu
from threading import Thread
from memory.memory_reader import PymemHandler
import keyboard as kb
from configs.config import OPEN
from time import sleep, time
import atexit
import psutil
import sys

from matrix.matrix_handling import esp_loop


def wait_for_game(process_name="ac_client.exe", timeout=30):
    start_time = time()
    while True:
        elapsed_time = time() - start_time
        remaining_time = int(timeout - elapsed_time)

        if remaining_time <= 0:
            print(f"{process_name} not found within {timeout} seconds. Exiting...")
            sys.exit(1)  # Thoát chương trình khi hết thời gian chờ

        for proc in psutil.process_iter():
            if proc.name() == process_name:
                return proc.pid  # Game found, return pid

        print(f"Waiting for {process_name} to start... ({remaining_time}s remaining)")
        sleep(1)  # Kiểm tra mỗi giây để cập nhật thời gian đếm ngược


def keybinds(modmenu):
    isopen = True
    while True:
        if kb.is_pressed(OPEN):
            if isopen:
                modmenu.win.withdraw()
                isopen = False
            else:
                modmenu.update_position()
                modmenu.win.deiconify()
                isopen = True
                modmenu.win.focus_force()
            sleep(0.5)  # Add a delay to prevent the key press from being registered multiple times


def check_game_running(modmenu):
    while True:
        game_running = any(proc.name() == "ac_client.exe" for proc in psutil.process_iter())
        if not game_running:
            modmenu.game_running = False
            modmenu.stop_hacks()
            modmenu.win.destroy()
            break
        sleep(1)


def cleanup(modmenu, mem_handler):
    modmenu.stop_hacks()
    mem_handler.close()


if __name__ == "__main__":
    # Chờ đợi game được mở trong 30 giây, nếu không sẽ thoát
    game_pid = wait_for_game(timeout=30)

    try:
        mem_handler = PymemHandler("ac_client.exe")
        modmenu = ModMenu("AssaultCube Cheats", 350, 550, mem_handler)  # Adjusted window size for tabs

        keybinds_thread = Thread(target=keybinds, args=(modmenu,))
        keybinds_thread.daemon = True
        keybinds_thread.start()

        check_game_running_thread = Thread(target=check_game_running, args=(modmenu,))
        check_game_running_thread.daemon = True
        check_game_running_thread.start()

        proc = pm.open_process("ac_client.exe")
        base = pm.get_module(proc, "ac_client.exe")["base"]

        esp_thread = Thread(target=esp_loop, args=(proc, base, modmenu))
        esp_thread.daemon = True
        esp_thread.start()

        atexit.register(cleanup, modmenu, mem_handler)

        modmenu.win.mainloop()

    except Exception as e:
        print(f"Failed to initialize the mod menu: {e}")
        sys.exit(1)
