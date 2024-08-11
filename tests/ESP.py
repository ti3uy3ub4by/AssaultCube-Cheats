import pyMeow as pm
import pyautogui

try:
    proc = pm.open_process("ac_client.exe")
    base = pm.get_module(proc, "ac_client.exe")["base"]
except Exception as e:
    print(f"Failed to open process or get base module: {e}")


class Pointer:
    player_count = 0x18AC0C
    entity_list = 0x18AC04
    view_matrix = 0x17DFD0


class Offsets:
    name = 0x205
    health = 0xEC
    armor = 0xF0
    team = 0x30C
    pos = 0x4
    fpos = 0x28


class Colors:
    cyan = pm.get_color("green")
    orange = pm.get_color("red")
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
        self.color = Colors.cyan if self.team else Colors.orange
        self.pos3d = pm.r_vec3(proc, self.addr + Offsets.pos)
        self.fpos3d = pm.r_vec3(proc, self.addr + Offsets.fpos)
        self.pos2d = self.fpos2d = None
        self.head = self.width = self.center = None

    def wts(self, vm):
        try:
            self.pos2d = pm.world_to_screen(vm, self.pos3d)
            self.fpos2d = pm.world_to_screen(vm, self.fpos3d)

            screen_width, screen_height = pyautogui.size()
            if self.pos2d and self.fpos2d and \
                    0 <= self.pos2d["x"] <= screen_width and 0 <= self.pos2d["y"] <= screen_height and \
                    0 <= self.fpos2d["x"] <= screen_width and 0 <= self.fpos2d["y"] <= screen_height:
                self.head = self.fpos2d["y"] - self.pos2d["y"]
                self.width = self.head / 2
                self.center = self.width / 2
                return True
            else:
                raise ValueError(f"2D Position out of bounds: pos2d={self.pos2d}, fpos2d={self.fpos2d}")
        except Exception as e:
            print(f"Error in wts: {e}")
            return False

    def draw_box(self):
        if self.pos2d:
            pm.draw_rectangle(
                posX=self.pos2d["x"] - self.center,
                posY=self.pos2d["y"] - self.center / 2,
                width=self.width,
                height=self.head + self.center / 2,
                color=pm.fade_color(self.color, 0.1),
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
        if self.pos2d:
            textSize = pm.measure_text(self.name, 15) / 2
            pm.draw_text(
                text=self.name,
                posX=self.pos2d["x"] - textSize,
                posY=self.pos2d["y"],
                fontSize=15,
                color=Colors.white,
            )

    def draw_health(self):
        if self.pos2d:
            pm.draw_rectangle(
                posX=self.pos2d["x"] - self.center,
                posY=self.pos2d["y"] - self.head / 2 - 10,  # Đặt thanh máu trên đầu nhân vật
                width=self.width,
                height=5,  # Chiều cao của thanh máu
                color=Colors.black,
            )
            pm.draw_rectangle(
                posX=self.pos2d["x"] - self.center,
                posY=self.pos2d["y"] - self.head / 2 - 10,
                width=self.width * (self.health / 100),  # Chiều dài tỉ lệ với sức khỏe
                height=5,
                color=self.color,
            )

    def draw_snapline(self):
        if self.pos2d:
            # Lấy độ phân giải màn hình thực tế
            screen_width, screen_height = pyautogui.size()

            # Xác định điểm gốc của Snapline (chỉnh sửa để đảm bảo ở giữa đáy màn hình)
            line_origin = (screen_width // 2, screen_height - 1)  # Đảm bảo đúng vị trí ở dưới cùng

            # Xác định điểm kết thúc của Snapline (vị trí 2D của đối tượng)
            line_end = (self.pos2d["x"], self.pos2d["y"])

            # Vẽ đường Snapline từ gốc đến đối tượng
            pm.draw_line(
                startPosX=line_origin[0],
                startPosY=line_origin[1],
                endPosX=line_end[0],
                endPosY=line_end[1],
                color=self.color
            )


class ModMenu:
    def __init__(self, draw_box_active, draw_name_active, draw_health_active, draw_snapline_active):
        self.draw_box_active = draw_box_active
        self.draw_name_active = draw_name_active
        self.draw_health_active = draw_health_active
        self.draw_snapline_active = draw_snapline_active


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
                        if modmenu.draw_snapline_active:  # Vẽ Snapline từ người chơi đến đối tượng
                            ent.draw_snapline()
                except Exception as e:
                    print(f"Error processing entity: {e}")
                    continue
        pm.end_drawing()


# Khởi tạo đối tượng modmenu với các chế độ cần thiết và chạy vòng lặp esp
modmenu = ModMenu(draw_box_active=True, draw_name_active=True, draw_health_active=True, draw_snapline_active=True)
esp_loop(proc, base, modmenu)
