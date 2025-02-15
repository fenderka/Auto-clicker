import sys
import time
import threading
from pynput import mouse, keyboard
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QRadioButton, QSpinBox, QGroupBox, QMessageBox,
                             QFrame, QFormLayout)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush


class AutoClickerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.auto_clicker = AutoClicker()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Современный Автокликер")  # Заголовок окна
        self.setGeometry(100, 100, 600, 400)  # Размеры и позиция окна

        # --- Цветовая палитра (градиент и мягкие цвета) ---
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(40, 40, 45))
        gradient.setColorAt(1, QColor(30, 30, 30))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        palette.setColor(QPalette.WindowText, QColor(230, 230, 230))
        palette.setColor(QPalette.Base, QColor(60, 60, 65))
        palette.setColor(QPalette.AlternateBase, QColor(50, 50, 55))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(230, 230, 230))
        palette.setColor(QPalette.Button, QColor(60, 60, 65))
        palette.setColor(QPalette.ButtonText, QColor(230, 230, 230))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(100, 149, 237))  # CornflowerBlue
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

        # --- Шрифты ---
        font_title = QFont("Arial", 16, QFont.Bold)
        font_label = QFont("Arial", 12)
        font_button = QFont("Arial", 12, QFont.Bold)

        # --- Интерфейс и стили CSS ---
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 12px;
            }
            QGroupBox {
                border: 1px solid #666;
                border-radius: 12px;
                margin-top: 1.5em;
                padding: 15px;
                background: transparent;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #eee;
                font-weight: bold;
                font-size: 14px;
            }
            QLabel {
                color: #eee;
                background: transparent;
            }
            QLineEdit, QSpinBox {
                border: 1px solid #888;
                border-radius: 6px;
                padding: 6px;
                background-color: #444;
                color: #eee;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #356cb3;
            }
            QPushButton:pressed {
                background-color: #284b78;
            }
            QRadioButton {
                color: #eee;
                background: transparent;
            }
            QFrame {
                background-color: #666;
                border: none;
            }
        """)

        # --- Интервал кликов ---
        interval_group = QGroupBox("Интервал Кликов")
        interval_group.setFont(font_title)
        interval_layout = QFormLayout()

        self.hours_label = QLabel("Часы:")
        self.hours_input = QSpinBox()
        self.hours_input.setMaximum(99)

        self.minutes_label = QLabel("Минуты:")
        self.minutes_input = QSpinBox()
        self.minutes_input.setMaximum(59)

        self.seconds_label = QLabel("Секунды:")
        self.seconds_input = QSpinBox()
        self.seconds_input.setMaximum(59)

        self.milliseconds_label = QLabel("Миллисекунды:")
        self.milliseconds_input = QSpinBox()
        self.milliseconds_input.setMaximum(999)

        interval_layout.addRow(self.hours_label, self.hours_input)
        interval_layout.addRow(self.minutes_label, self.minutes_input)
        interval_layout.addRow(self.seconds_label, self.seconds_input)
        interval_layout.addRow(self.milliseconds_label, self.milliseconds_input)

        interval_group.setLayout(interval_layout)

        # --- Разделитель ---
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        # --- Позиция курсора ---
        position_group = QGroupBox("Позиция Курсора")
        position_group.setFont(font_title)
        position_layout = QVBoxLayout()

        self.current_location_radio = QRadioButton("Текущая Позиция")
        self.current_location_radio.setChecked(True)

        self.pick_location_radio = QRadioButton("Выбрать Позицию")
        self.x_label = QLabel("X:")
        self.x_input = QSpinBox()
        self.y_label = QLabel("Y:")
        self.y_input = QSpinBox()

        pick_location_layout = QHBoxLayout()
        pick_location_layout.addWidget(self.x_label)
        pick_location_layout.addWidget(self.x_input)
        pick_location_layout.addWidget(self.y_label)
        pick_location_layout.addWidget(self.y_input)

        position_layout.addWidget(self.current_location_radio)
        position_layout.addWidget(self.pick_location_radio)
        position_layout.addLayout(pick_location_layout)

        position_group.setLayout(position_layout)

        # --- Кнопки ---
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Старт (F6)")
        self.start_button.clicked.connect(self.start_clicking)

        self.stop_button = QPushButton("Стоп (F6)")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_clicking)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # --- Главный макет ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(interval_group)
        main_layout.addWidget(separator)
        main_layout.addWidget(position_group)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # --- Клавишный прослушиватель ---
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()

    def start_clicking(self):
        try:
            hours = self.hours_input.value()
            minutes = self.minutes_input.value()
            seconds = self.seconds_input.value()
            milliseconds = self.milliseconds_input.value()

            if hours == 0 and minutes == 0 and seconds == 0 and milliseconds == 0:
                raise ValueError("Интервал кликов не может быть равен 0!")

            delay = (hours * 3600 + minutes * 60 + seconds) + milliseconds / 1000
            self.auto_clicker.set_delay(delay)

            if self.current_location_radio.isChecked():
                self.auto_clicker.set_click_position("current")
            elif self.pick_location_radio.isChecked():
                x = self.x_input.value()
                y = self.y_input.value()
                self.auto_clicker.set_click_position("fixed", x, y)

            self.auto_clicker.start_clicking()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.animateButton(self.stop_button, True)

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e), QMessageBox.Ok)

    def stop_clicking(self):
        self.auto_clicker.stop_clicking()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.animateButton(self.stop_button, False)

    def on_press(self, key):
        if key == keyboard.Key.f6:
            if self.auto_clicker.running:
                self.stop_clicking()
            else:
                self.start_clicking()

    def animateButton(self, button, start):
        color_start = QColor("#356cb3") if start else QColor("#d9534f")
        color_end = QColor("#d9534f") if start else QColor("#4a90e2")

        self.animation = QPropertyAnimation(button, b"background-color")
        self.animation.setDuration(500)
        self.animation.setStartValue(color_start)
        self.animation.setEndValue(color_end)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()


class AutoClicker:  # Логика автокликера
    def __init__(self):
        self.running = False
        self.delay = 0.1
        self.button = mouse.Button.left
        self.click_type = "single"
        self.click_position = "current"
        self.x = None
        self.y = None

    def set_delay(self, delay):
        self.delay = delay

    def set_mouse_button(self, button):
        self.button = mouse.Button.left if button == "left" else mouse.Button.right

    def set_click_position(self, position, x=None, y=None):
        self.click_position = position
        self.x = x
        self.y = y

    def start_clicking(self):
        self.running = True
        threading.Thread(target=self.click_loop, daemon=True).start()

    def stop_clicking(self):
        self.running = False

    def click_loop(self):
        mouse_controller = mouse.Controller()

        while self.running:
            if self.click_position == "fixed" and self.x is not None and self.y is not None:
                mouse_controller.position = (self.x, self.y)

            if self.click_type == "single":
                mouse_controller.click(self.button)
            elif self.click_type == "double":
                mouse_controller.click(self.button, 2)

            time.sleep(self.delay)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = AutoClickerGUI()
    gui.show()
    sys.exit(app.exec_())
