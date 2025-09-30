import math
import sys
from PyQt6.QtCore import QTimer, QPoint
from PyQt6.QtWidgets import QFrame, QApplication
from PyQt6.QtGui import QPainter, QBrush, QColor
import json
import os

SETTINGS_FILE = "planets_settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        print(f"Ошибка: Файл настроек {SETTINGS_FILE} не найден. Завершение.")
        sys.exit(1)
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def degree_to_radian(degree):
    return degree * math.pi / 180

from PyQt6.QtCore import Qt

class Circle(QFrame):
    def __init__(self, color, size, parent=None):
        super().__init__(parent)
        self.color = color
        self.resize(size, size)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.angle = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(0.75)
        brush = QBrush(QColor(self.color))
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        radius = min(self.width(), self.height()) // 2
        painter.drawEllipse(self.rect().center(), radius, radius)

    def rotate_self(self, angle_increment):
        self.angle = (self.angle + angle_increment) % 360
        self.update()

class Window(QFrame):
    def __init__(self, app_obj: QApplication):
        super().__init__()
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        height = app_obj.primaryScreen().availableGeometry().height()
        self.resize(int(height * 0.6), int(height * 0.6))
        self.setWindowTitle("Планеты")

        self.center_x = int(self.width() / 2)
        self.center_y = int(self.height() / 2)

        self.planets = []
        self.angles = []
        self.angle_speeds = []
        self.self_rot_speeds = []
        self.orbit_radii = []
        self.sizes = []

        settings = load_settings()

        for p in settings['planets']:
            planet = Circle(p['color'], p['size'], self)
            x = self.center_x + p['radius'] * math.cos(degree_to_radian(0)) - p['size'] // 2
            y = self.center_y + p['radius'] * math.sin(degree_to_radian(0)) - p['size'] // 2
            planet.move(int(x), int(y))
            planet.show()

            self.planets.append(planet)
            self.angles.append(0)
            self.angle_speeds.append(p['angle_speed'])
            self.self_rot_speeds.append(p['self_rot_speed'])
            self.orbit_radii.append(p['radius'])
            self.sizes.append(p['size'])

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_positions)
        self.timer.start(30)

    def update_positions(self):
        for i, planet in enumerate(self.planets):
            self.angles[i] = (self.angles[i] + self.angle_speeds[i]) % 360
            radius = self.orbit_radii[i]
            size = self.sizes[i]
            x = self.center_x + radius * math.cos(degree_to_radian(self.angles[i])) - size // 2
            y = self.center_y + radius * math.sin(degree_to_radian(self.angles[i])) - size // 2
            planet.move(int(x), int(y))
            planet.rotate_self(self.self_rot_speeds[i])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window(app)
    window.show()
    sys.exit(app.exec())
