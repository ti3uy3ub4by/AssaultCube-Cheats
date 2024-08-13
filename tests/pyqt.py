from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton


class ModMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AssaultCube Mod Menu")
        self.setGeometry(100, 100, 400, 300)

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        esp_tab = QWidget()
        hacks_tab = QWidget()
        general_tab = QWidget()

        tabs.addTab(esp_tab, "ESP Settings")
        tabs.addTab(hacks_tab, "Hacks")
        tabs.addTab(general_tab, "General")

        esp_layout = QVBoxLayout()
        esp_tab.setLayout(esp_layout)
        esp_layout.addWidget(QLabel("Draw Box: OFF"))
        esp_layout.addWidget(QLabel("Draw Name: OFF"))
        esp_layout.addWidget(QLabel("Draw Health: OFF"))
        esp_layout.addWidget(QLabel("Draw Line: OFF"))

        hacks_layout = QVBoxLayout()
        hacks_tab.setLayout(hacks_layout)
        hacks_layout.addWidget(QLabel("Health Hack: OFF"))
        hacks_layout.addWidget(QLabel("Armor Hack: OFF"))

        general_layout = QVBoxLayout()
        general_tab.setLayout(general_layout)
        exit_button = QPushButton("Exit")
        general_layout.addWidget(exit_button)

        exit_button.clicked.connect(self.close)


if __name__ == "__main__":
    app = QApplication([])
    window = ModMenu()
    window.show()
    app.exec_()
