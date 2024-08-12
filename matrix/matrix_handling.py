import pyMeow as pm
import pyautogui
from time import sleep
from configs.offsets import Pointer, Offsets, AmmoOffsets, FastFireOffsets, PositionOffsets

try:
    proc = pm.open_process("ac_client.exe")
    base = pm.get_module(proc, "ac_client.exe")["base"]
except Exception as e:
    print(f"Failed to open process or get base module: {e}")

# Check proc và base
if not proc or not base:
    print("Process or base module is invalid. Exiting...")
    exit(1)


class Colors:
    team1 = pm.get_color("green")
    team2 = pm.get_color("red")
    white = pm.get_color("white")
    black = pm.get_color("black")


class Entity:
    def __init__(self, proc, addr):
        self.proc = proc
        self.addr = addr
        self.health = pm.r_int(proc, addr + Offsets.health)
        if self.health <= 0:
            raise Exception("Entity is not alive.")
        self.name = pm.r_string(proc, addr + Offsets.name)
        self.armor = pm.r_int(proc, addr + Offsets.armor)
        self.team = pm.r_int(proc, addr + Offsets.team)
        self.color = Colors.team1 if self.team else Colors.team2
        self.pos3d = pm.r_vec3(proc, self.addr + Offsets.pos)
        self.fpos3d = pm.r_vec3(proc, self.addr + Offsets.fpos)
        self.pos2d = self.fpos2d = None
        self.head = self.width = self.center = None

    def is_valid_pos(self, pos2d, screen_width, screen_height):
        return 0 <= pos2d["x"] <= screen_width and 0 <= pos2d["y"] <= screen_height

    def wts(self, vm):
        self.pos2d = pm.world_to_screen(vm, self.pos3d)
        self.fpos2d = pm.world_to_screen(vm, self.fpos3d)

        screen_width, screen_height = pyautogui.size()

        if not (self.pos2d and self.fpos2d and
                self.is_valid_pos(self.pos2d, screen_width, screen_height) and
                self.is_valid_pos(self.fpos2d, screen_width, screen_height)):
            return False  # Không làm gì thêm nếu tọa độ không hợp lệ

        self.head = self.fpos2d["y"] - self.pos2d["y"]
        self.width = self.head / 2
        self.center = self.width / 2
        return True

    def draw_box(self):
        pm.draw_rectangle(
            posX=self.pos2d["x"] - self.center,
            posY=self.pos2d["y"] - self.center / 2,
            width=self.width,
            height=self.head + self.center / 2,
            color=pm.fade_color(self.color, 0.3),
        )
        pm.draw_rectangle_lines(
            posX=self.pos2d["x"] - self.center,
            posY=self.pos2d["y"] - self.center / 2,
            width=self.width,
            height=self.head + self.center / 2,
            color=self.color,
            lineThick=1.2,
        )

    def draw_name(self):
        textSize = pm.measure_text(self.name, 15) / 2
        pm.draw_text(
            text=self.name,
            posX=self.pos2d["x"] - textSize,
            posY=self.pos2d["y"],
            fontSize=15,
            color=Colors.white,
        )

    def draw_health(self):
        # Vẽ khung đen cho thanh máu
        pm.draw_rectangle(
            posX=self.pos2d["x"] - self.center,
            posY=self.pos2d["y"] - self.head / 2 - 10,  # Đặt thanh máu trên đầu nhân vật
            width=self.width,
            height=5,  # Chiều cao của thanh máu
            color=Colors.black,
        )
        # Vẽ thanh máu
        pm.draw_rectangle(
            posX=self.pos2d["x"] - self.center,
            posY=self.pos2d["y"] - self.head / 2 - 10,
            width=self.width * (self.health / 100),  # Chiều dài tỉ lệ với sức khỏe
            height=5,
            color=self.color,
        )

    def draw_line(self):
        if self.pos2d:
            screen_width, screen_height = pyautogui.size()
            line_origin = (screen_width // 2, screen_height - 1)
            line_end = (self.pos2d["x"], self.pos2d["y"])
            pm.draw_line(
                startPosX=line_origin[0],
                startPosY=line_origin[1],
                endPosX=line_end[0],
                endPosY=line_end[1],
                color=self.color
            )


def esp_loop(proc, base, modmenu):
    pm.overlay_init(target="AssaultCube", fps=144, trackTarget=True)
    while pm.overlay_loop():
        pm.begin_drawing()
        pm.draw_fps(10, 10)
        player_count = pm.r_int(proc, base + Pointer.player_count)
        if player_count > 1:
            ent_buffer = pm.r_ints(
                proc, pm.r_int(proc, base + Pointer.entity_list), player_count
            )[1:]
            v_matrix = pm.r_floats(proc, base + Pointer.view_matrix, 16)
            for addr in ent_buffer:
                try:
                    ent = Entity(proc, addr)
                    if ent.wts(v_matrix):
                        if modmenu.draw_box_active:
                            ent.draw_box()
                        if modmenu.draw_name_active:
                            ent.draw_name()
                        if modmenu.draw_health_active:
                            ent.draw_health()
                        if modmenu.draw_line_active:
                            ent.draw_line()
                except Exception as e:
                    continue
        pm.end_drawing()
        sleep(0.01)
