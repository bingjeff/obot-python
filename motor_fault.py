import motor_widgets
import pyqt_led

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QMargins
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout


class FaultTab(motor_widgets.ApiTab):
    def __init__(
        self,
        api_connection: motor_widgets.ApiConnection,
        **kwargs,
    ):
        super(FaultTab, self).__init__("fault", api_connection, **kwargs)

        status_layout = QGridLayout()
        status_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        status_layout.setContentsMargins(QMargins(20, 0, 20, 0))
        status_layout.setSpacing(1)
        self.header_names = [
            f"{c}:{m.name()}"
            for c, m in enumerate(
                self.api_connection.motor_manager.get_connected_motors(
                    connect=False
                )
            )
        ]
        self.mode_widgets = {
            h: motor_widgets.LineStatus(f"{h}-mode")
            for h in self.header_names
        }
        error_names = self.api_connection.current_motor.error_mask().keys()
        self.led_widgets = pyqt_led.LedGrid(
            self.header_names, error_names, on_color="red", off_color="green"
        )
        for c, header_name in enumerate(self.header_names, start=1):
            status_layout.addWidget(
                QLabel(header_name),
                0,
                c,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )
            status_layout.addWidget(
                self.mode_widgets[header_name],
                1,
                c,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )
            led_strip = self.led_widgets.led_strips[header_name]
            for r, error_name in enumerate(error_names, start=2):
                led = led_strip.leds[error_name]
                led.setFixedSize(30, 30)
                status_layout.addWidget(
                    led, r, c, alignment=Qt.AlignmentFlag.AlignCenter
                )
        for r, error_name in enumerate(error_names, start=2):
            label = QLabel(error_name)
            label.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            status_layout.addWidget(label, r, 0)

        command_layout = QVBoxLayout()
        button = QPushButton("driver_enable")
        button.clicked.connect(self.api_connection.command_driver_enable)
        command_layout.addWidget(button)
        button = QPushButton("open")
        button.clicked.connect(self.api_connection.command_open)
        command_layout.addWidget(button)
        button = QPushButton("damped")
        button.clicked.connect(self.api_connection.command_damped)
        command_layout.addWidget(button)

        layout = QHBoxLayout()
        layout.addLayout(status_layout)
        layout.addLayout(command_layout)
        self.setLayout(layout)

    def pause(self):
        super(FaultTab, self).pause()
        self.api_connection.connect_current_motor()

    def update(self):
        self.api_connection.connect_all()
        statuses = self.api_connection.read_all()
        for status, header_name in zip(statuses, self.header_names):
            self.mode_widgets[header_name].setText(
                f"{status.flags.mode.name.lower()}"
            )
            self.led_widgets.led_strips[header_name].update_by_names(
                status.flags.error.bits
            )
