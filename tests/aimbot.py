import pyMeow as pm
from configparser import ConfigParser

class Aimbot:
    def __init__(self):
        # Khởi tạo các biến cấu hình và trạng thái ban đầu của aimbot
        self.config = dict()  # Lưu cấu hình từ file config.ini
        self.region = dict()  # Xác định vùng FOV trên màn hình
        self.enemy_in_fov = bool()  # Trạng thái có đối thủ trong FOV hay không
        self.paused = bool()  # Trạng thái tạm dừng của aimbot
        # Định nghĩa các màu sắc sử dụng trong việc vẽ đồ họa
        self.colors = {
            "blue": pm.get_color("skyblue"),
            "red": pm.get_color("red"),
            "orange": pm.get_color("orange"),
        }

    def read_config(self):
        # Đọc cấu hình từ file config.ini
        c = ConfigParser()
        c.read("config.ini")
        try:
            # Lưu các thông số cấu hình vào biến self.config
            self.config = {
                "fps": c.getint("Main", "fps"),
                "draw_fps": c.getboolean("Main", "draw_fps"),
                "color": pm.get_color(c.get("Main", "color")),
                "similarity": c.getint("Main", "similarity"),
                "fov": c.getint("Main", "fov"),
                "pause_btn": c.getint("Main", "pause_btn"),
                "autoaim": c.getboolean("Aimbot", "autoaim"),
                "aimkey": c["Aimbot"]["aimkey"],
                "mark_color": pm.get_color(c.get("Aimbot", "mark_color")),
                "smooth": c.getint("Aimbot", "smooth"),
            }
        except Exception as e:
            # Thoát chương trình nếu không tìm thấy file cấu hình hoặc cấu hình không hợp lệ
            quit(f"config.ini missing or invalid ({e})")

    def run(self):
        # Khởi tạo overlay để hiển thị FPS và các yếu tố khác lên màn hình
        pm.overlay_init(fps=self.config["fps"])
        # Tính toán vùng FOV dựa trên độ phân giải màn hình và kích thước FOV
        self.region = {
            "x": pm.get_screen_width() // 2 - self.config["fov"] // 2,
            "y": pm.get_screen_height() // 2 - self.config["fov"] // 2,
        }
        # Bắt đầu vòng lặp chính của aimbot
        self.main_loop()

    def main_loop(self):
        # Vòng lặp chính của aimbot, liên tục chạy cho đến khi overlay đóng
        while pm.overlay_loop():
            # Quét vùng FOV để tìm pixel có màu của đối thủ
            pixel = self.scan_pixel()
            # Cập nhật trạng thái có đối thủ trong FOV hay không
            self.enemy_in_fov = len(pixel) > 10
            pm.begin_drawing()  # Bắt đầu vẽ đồ họa lên màn hình
            if self.config["draw_fps"]:
                # Nếu được cấu hình, vẽ FPS lên góc trên cùng bên trái màn hình
                pm.draw_fps(0, 0)
            self.draw_fov()  # Vẽ vùng FOV lên màn hình
            self.check_pause()  # Kiểm tra trạng thái tạm dừng

            if not self.paused:
                if self.enemy_in_fov:
                    # Nếu có đối thủ trong FOV, tính toán và vẽ giới hạn bao quanh mục tiêu
                    bounds = self.calc_bounds(pixel)
                    self.draw_bounds(bounds)
                    # Tính toán điểm ngắm và thực hiện ngắm
                    aim_point = self.calc_aim_point(bounds)
                    if self.config["autoaim"]:
                        self.aim(aim_point, self.config["smooth"])
                    elif pm.mouse_pressed(self.config["aimkey"]):
                        self.aim(aim_point, self.config["smooth"])
            else:
                # Hiển thị chữ "Pause" khi aimbot đang tạm dừng
                pm.draw_text(
                    text="Pause",
                    posX=pm.get_screen_width() // 2 - pm.measure_text("Pause", 20) // 2,
                    posY=(pm.get_screen_height() // 2) - 10,
                    fontSize=20,
                    color=self.colors["orange"]
                )
            pm.end_drawing()  # Kết thúc vẽ đồ họa lên màn hình

    def draw_fov(self):
        # Vẽ vùng FOV lên màn hình dưới dạng hình chữ nhật với các góc được bo tròn
        pm.draw_rectangle_rounded_lines(
            posX=self.region["x"],
            posY=self.region["y"],
            width=self.config["fov"],
            height=self.config["fov"],
            roundness=0.1,
            segments=5,
            # Màu sắc thay đổi tùy vào việc có đối thủ trong FOV hay không
            color=self.colors["red"] if self.enemy_in_fov else self.colors["blue"],
            lineThick=1.2
        )

    def scan_pixel(self):
        # Tìm kiếm các pixel trong vùng FOV có màu sắc giống với màu đối thủ
        return list(pm.pixel_search_colors(
            x=self.region["x"],
            y=self.region["y"],
            width=self.config["fov"],
            height=self.config["fov"],
            colors=[self.config["color"]],
            similarity=self.config["similarity"]
        ))

    def calc_bounds(self, pixel):
        # Tính toán giới hạn bao quanh đối thủ dựa trên các pixel tìm được
        minX, minY = float("inf"), float("inf")
        maxX, maxY = float("-inf"), float("-inf")

        for p in pixel:
            minX = min(minX, p["x"])
            minY = min(minY, p["y"])
            maxX = max(maxX, p["x"])
            maxY = max(maxY, p["y"])

        return {"x": minX, "y": minY, "width": maxX - minX, "height": maxY - maxY}

    def draw_bounds(self, bounds):
        # Vẽ giới hạn bao quanh đối thủ lên màn hình
        pm.draw_rectangle_lines(
            posX=self.region["x"] + bounds["x"],
            posY=self.region["y"] + bounds["y"],
            width=bounds["width"],
            height=bounds["height"],
            color=self.config["mark_color"],
            lineThick=1.2,
        )

    def calc_aim_point(self, bounds):
        # Tính toán điểm ngắm, là trung tâm của giới hạn đối thủ
        point = {
            "x": self.region["x"] + bounds["x"] + bounds["width"] // 2,
            "y": self.region["y"] + bounds["y"] + bounds["height"] // 2
        }
        # Vẽ một vòng tròn nhỏ tại điểm ngắm này để hiển thị lên màn hình
        pm.draw_circle(
            centerX=point["x"],
            centerY=point["y"],
            radius=5,
            color=self.config["mark_color"]
        )
        return point

    def aim(self, point, smooth):
        # Di chuyển chuột đến điểm ngắm, có thể yêu cầu driver đặc biệt tùy vào game
        pm.mouse_move(
            x=(point["x"] - pm.get_screen_width() // 2) // smooth,
            y=(point["y"] - pm.get_screen_height() // 2) // smooth,
            relative=True
        )

    def check_pause(self):
        # Kiểm tra nếu phím tạm dừng được nhấn, chuyển đổi trạng thái tạm dừng của aimbot
        if pm.key_pressed(self.config["pause_btn"]):
            self.paused = not self.paused

if __name__ == "__main__":
    # Khởi tạo đối tượng Aimbot và bắt đầu chương trình
    aimbot = Aimbot()
    aimbot.read_config()  # Đọc cấu hình từ file config.ini
    aimbot.run()  # Chạy vòng lặp chính của aimbot
