import motor
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget


class ApiConnection:
    def __init__(self):
        self.cpu_frequency = 170e6
        self.motor_manager = motor.MotorManager()
        self.command_times = []
        self.current_index = 0
        self.current_motor_name = ""
        self.simulated = False

    @property
    def current_motor(self):
        return self.motor_manager.motors()[self.current_index]

    def pseudo_time(self):
        self.command_times.append(time.time_ns())
        return len(self.command_times) - 1

    def connect_motor(self, name: str):
        self.current_index = 0
        self.current_motor_name = name
        motors = self.motor_manager.get_motors_by_name(
            [name], allow_simulated=self.simulated
        )
        self.motor_manager.set_auto_count()
        self.cpu_frequency = motors[0].get_cpu_frequency()

    def connect_current_motor(self):
        self.connect_motor(self.current_motor_name)

    def connect_all(self):
        self.current_index = 0
        self.motor_manager.get_connected_motors(connect=True)

    def read_current_motor(self):
        return self.motor_manager.read()[self.current_index]

    def read_all(self):
        return self.motor_manager.read()

    def command_open(self):
        self.motor_manager.set_command_mode(motor.ModeDesired.Open)
        self.motor_manager.write_saved_commands()

    def command_damped(self):
        self.motor_manager.set_command_mode(motor.ModeDesired.Damped)
        self.motor_manager.write_saved_commands()

    def command_driver_enable(self):
        self.motor_manager.set_command_mode(motor.ModeDesired.DriverEnable)
        self.motor_manager.write_saved_commands()

    def command_current_tuning(
        self, amplitude, frequency, mode=motor.Square, bias=0.0
    ):
        command = motor.Command(
            host_timestamp=self.pseudo_time(), mode=motor.CurrentTuning
        )
        command.current_tuning.amplitude = amplitude
        command.current_tuning.frequency = frequency
        command.current_tuning.bias = bias
        command.current_tuning.mode = mode
        self.motor_manager.write([command])


class ApiTab(QWidget):
    def __init__(
        self,
        name: str,
        api_connection: ApiConnection,
        **kwargs,
    ):
        super(ApiTab, self).__init__(**kwargs)
        self.name = name
        self.api_connection = api_connection
        self.setAutoFillBackground(True)
        self.update_time_ms = 100
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

    def update(self):
        self.status = self.api_connection.read_current_motor()

    def pause(self):
        self.timer.stop()

    def unpause(self):
        self.timer.start(self.update_time_ms)


class StatusDisplay(QPushButton):
    def __init__(self, *args, **kwargs):
        super(StatusDisplay, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        pass

    def keyPressEvent(self, event):
        pass


class LineStatus(QLineEdit):
    def __init__(self, name, *args, **kwargs):
        super(LineStatus, self).__init__(*args, **kwargs)
        palette = QPalette()
        color = QPalette.color(self.palette(), QPalette.ColorRole.Window)
        palette.setColor(QPalette.ColorRole.Base, color)
        self.setPalette(palette)
        self.setToolTip(name)
        self.setReadOnly(True)


class DoubleLineStatus(LineStatus):
    def __init__(
        self,
        name: str,
        initial_value: float = 0.0,
        units: str = "",
        decimals: int = 2,
        width: int = 6,
        *args,
        **kwargs,
    ):
        super(DoubleLineStatus, self).__init__(name, *args, **kwargs)
        self._value = initial_value
        self.suffix = f" [{units}]" if units else ""
        self.format_decimals = decimals
        self.format_width = width
        self.setValue(initial_value)

    @property
    def value(self):
        return self._value

    def setValue(self, val: float):
        format = f"{self.format_width}.{self.format_decimals}f"
        text = f"{val:{format}}{self.suffix}"
        self._value = val
        self.setText(text)


class DoubleParameterStatus(DoubleLineStatus):
    def __init__(
        self,
        name: str,
        api_connection: ApiConnection,
        units: str = "",
        decimals: int = 2,
        width: int = 6,
        *args,
        **kwargs,
    ):
        super(DoubleParameterStatus, self).__init__(
            name,
            initial_value=0.0,
            units=units,
            decimals=decimals,
            width=width,
            *args,
            **kwargs,
        )
        self.name = name
        self.api_connection = api_connection

    def update(self):
        self.setValue(float(self.api_connection.current_motor[self.name].get()))


class LabelLineStatus(LineStatus):
    def __init__(self, name: str, *args, **kwargs):
        super(LabelLineStatus, self).__init__(name, *args, **kwargs)
        self._spacing = 14
        self._label = QLabel(self)
        self._label.setText(name)
        self.updateLabelRectangle()

    def updateLabelRectangle(self):
        bbox = self.fontMetrics().boundingRect(self._label.text())
        self.setContentsMargins(bbox.width() + self._spacing, 0, 0, 0)
        rect = self._label.rect()
        rect.setHeight(self.height())
        rect.moveLeft(0)
        self._label.setGeometry(rect)

    def resizeEvent(self, event):
        super(LabelLineStatus, self).resizeEvent(event)
        self.updateLabelRectangle()


class DoubleLabelLineStatus(LabelLineStatus):
    def __init__(
        self,
        name: str,
        initial_value: float = 0.0,
        units: str = "",
        decimals: int = 2,
        width: int = 6,
        *args,
        **kwargs,
    ):
        super(DoubleLabelLineStatus, self).__init__(name, *args, **kwargs)
        self._value = initial_value
        self.suffix = f" [{units}]" if units else ""
        self.format_decimals = decimals
        self.format_width = width
        self.setValue(initial_value)

    @property
    def value(self):
        return self._value

    def setValue(self, val: float):
        format = f"{self.format_width}.{self.format_decimals}f"
        text = f"{val:{format}}{self.suffix}"
        self._value = val
        self.setText(text)

class DoubleParameterSpinBox(QDoubleSpinBox):
    def __init__(
        self,
        name: str,
        api_connection: ApiConnection,
        increment:float=0.1,
        minimum:float=0.0,
        maximum:float=1.0e9,
        units: str = "",
        decimals: int = 2,
        *args,
        **kwargs,
    ):
        super(DoubleParameterSpinBox, self).__init__(*args, **kwargs)
        self.name = name
        self.api_connection = api_connection
        self.setToolTip(name)
        self.setDecimals(decimals)
        self.setSingleStep(increment)
        self.setRange(minimum, maximum)
        if units:
            self.setSuffix(f" [{units}]")
        self.valueChanged.connect(self.write_edit)

    def update(self):
        try:
            self.blockSignals(True)
            parameter = self.api_connection.current_motor[self.name]
            val = float(parameter.get())
            self.setValue(val)
        except ValueError as e:
            print(f'ERROR<{e}>. Failed to read parameter {self.name}')
        finally:
            self.blockSignals(False)

    def write_edit(self, val:float):
        try:
            print(f'Writing {self.name} = {self.text()} ({val})')
            self.api_connection.current_motor[self.name] = self.text()
        except ValueError as e:
            print(f'ERROR<{e}>. Failed to write parameter {self.name}')

