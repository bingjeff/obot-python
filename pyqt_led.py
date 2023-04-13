import numpy as np

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton

LED_COLORS = {
    "black": np.array([0x00, 0x00, 0x00], dtype=np.uint8),
    "white": np.array([0xFF, 0xFF, 0xFF], dtype=np.uint8),
    "blue": np.array([0x73, 0xCE, 0xF4], dtype=np.uint8),
    "green": np.array([0xAD, 0xFF, 0x2F], dtype=np.uint8),
    "orange": np.array([0xFF, 0xA5, 0x00], dtype=np.uint8),
    "purple": np.array([0xAF, 0x00, 0xFF], dtype=np.uint8),
    "red": np.array([0xF4, 0x37, 0x53], dtype=np.uint8),
    "yellow": np.array([0xFF, 0xFF, 0x00], dtype=np.uint8),
}


def _qss_format(radius: float, color: np.ndarray):
    gradient = (0.5 * (LED_COLORS["white"] - color)).astype(np.uint8) + color
    gradient_str = f"{gradient[0]:02X}{gradient[1]:02X}{gradient[2]:02X}"
    color_str = f"{color[0]:02X}{color[1]:02X}{color[2]:02X}"
    return f"""
QPushButton {{
    border: 3px solid lightgray;
    border-radius: {radius}px;
    background-color: QLinearGradient(
        y1: 0,
        y2: 1,
        stop: 0.2 #{gradient_str},
        stop: 0.8 #{color_str},
        stop: 1.0 #{color_str}
    );
}}
    """


class Led(QPushButton):
    def __init__(self, on_color: str = "green", off_color: str = "red"):
        super(Led, self).__init__()

        self._on_qss = ""
        self._off_qss = ""
        self._end_radius = 0

        self._status = False

        self._on_color = LED_COLORS[on_color]
        self._off_color = LED_COLORS[off_color]
        self._height = self.sizeHint().height()

    # =================================================== Reimplemented Methods
    def sizeHint(self):
        base_radius = 30
        width = int(base_radius)
        height = int(base_radius)
        return QSize(width, height)

    def resizeEvent(self, event):
        self._height = self.size().height()
        QPushButton.resizeEvent(self, event)

    def setFixedSize(self, width, height):
        del width
        self._height = height
        QPushButton.setFixedSize(self, height, height)

    # ============================================================== Properties
    @property
    def _height(self):
        return self.__height

    @_height.setter
    def _height(self, height):
        self.__height = height
        self._update_qss()
        self.set_status(self._status)

    @_height.deleter
    def _height(self):
        del self.__height

    # ================================================================= Methods
    def _update_qss(self):
        self._end_radius = int(0.5 * self.__height)
        self._on_qss = _qss_format(self._end_radius, self._on_color)
        self._off_qss = _qss_format(self._end_radius, self._off_color)        

    def set_status(self, status):
        self._status = status
        if self._status:
            self.setStyleSheet(self._on_qss)
        else:
            self.setStyleSheet(self._off_qss)

    def turn_on(self):
        self.set_status(True)

    def turn_off(self):
        self.set_status(False)

    def is_on(self):
        return self._status

    def is_off(self):
        return not self._status


class LedStrip:
    def __init__(self, names:list[str], on_color: str = "green", off_color: str = "red"):
        self.names = names
        self.leds = {n:Led(on_color=on_color, off_color=off_color) for n in names}
        for name in self.names:
            self.leds[name].setToolTip(name)
    
    def update(self, values=list[bool]):
        for name, value in zip(self.names, values):
            self.leds[name].set_status(value)

    def update_by_names(self, values=dict[str, bool]):
        for name, value in values.items():
            self.leds[name].set_status(value)

class LedGrid:
    def __init__(self, header:list[str], names:list[str], on_color: str = "green", off_color: str = "red"):
        self.header = header
        self.names = names
        self.led_strips = {h:LedStrip(names, on_color=on_color, off_color=off_color) for h in header}
    
    def update(self, values=list[list[bool]]):
        for name, value in zip(self.header, values):
            self.led_strips[name].update(value)

    def update_by_names(self, values=dict[str, dict[str, bool]]):
        for name, value in values.items():
            self.led_strips[name].update_by_names(value)
