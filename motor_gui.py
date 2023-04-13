#!/usr/bin/env python3

import sys

import motor_current_tuning
import motor_fault
import motor_widgets

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QSlider,
    QComboBox,
    QMenuBar,
    QCheckBox,
    QMenu,
    QPlainTextEdit,
)
from PyQt5.QtGui import QPalette, QColor, QDoubleValidator

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)



# class ApiNumberEdit(ApiWidget):
#     def __init__(self, name, api_connection, description=None, tooltip=None, value=0.0, **kwargs):
#         super(NumberEdit, self).__init__(name, api_connection, description, tooltip, **kwargs)
#         self.number_widget = QLineEdit()
#         self.number_widget.setValidator(QDoubleValidator())
#         self.number_widget.editingFinished.connect(self.editingFinished)

#         self.setNumber(value)
#         self.layout.addWidget(self.label)
#         self.layout.addWidget(self.number_widget)
#         self.setLayout(self.layout)


# class NumberEdit(QWidget):
#     signal = pyqtSignal(float)
#     def __init__(self, name, description=None, tooltip=None, value=0):
#         super(NumberEdit, self).__init__()

#         if description is None:
#             description = name
#         self.layout = QHBoxLayout()
#         self.name = name
#         self.label = QLabel(description)
#         if tooltip is None:
#             tooltip = name
#         self.label.setToolTip(tooltip)
#         self.layout.addWidget(self.label)
#         self.number_widget = QLineEdit()
#         self.number_widget.setValidator(QDoubleValidator())
#         self.setNumber(value)
#         self.number_widget.editingFinished.connect(self.editingFinished)
#         self.layout.addWidget(self.number_widget)
#         self.setLayout(self.layout)

#     def setNumber(self, number):
#         num = str(number)
#         try:
#             num = str(int(num))
#         except ValueError:
#             try:
#                 num = "{:.4f}".format(float(num))
#             except ValueError:
#                 pass
#         self.number_widget.setText(num)

#     def getNumber(self):
#         return float(self.number_widget.text())

#     def editingFinished(self):
#         self.signal.emit(float(self.number_widget.text()))

# class NumberDisplay(NumberEdit):
#     def __init__(self, *args, **kwargs):
#         super(NumberDisplay, self).__init__(*args, **kwargs)
#         self.number_widget.setReadOnly(True)


# class APIEdit(NumberEdit):
#     def __init__(self, name, api_connection, description=None, tooltip=None, *args, **kwargs):
#         self.api_connection = api_connection
#         if tooltip is None:
#             tooltip = "api: " + name
#         else:
#             tooltip = "api: {}\n{}".format(name, tooltip)
#         super(APIEdit, self).__init__(name, description, tooltip, *args, **kwargs)

#     def editingFinished(self):
#         self.api_connection.current_motor[self.name] = self.number_widget.text()
#         return super().editingFinished()

#     def update(self):
#         if not self.number_widget.hasFocus():
#             val = self.api_connection.current_motor[self.name].get()
#             self.number_widget.setText(val)

# class APIDisplay(APIEdit):
#     def __init__(self, *args, **kwargs):
#         super(APIDisplay, self).__init__(*args, **kwargs)
#         self.number_widget.setReadOnly(True)

# class APIBool(QWidget):
#     def __init__(self, name, description=None, tooltip=None, *args, **kwargs):
#         super(APIBool, self).__init__(*args, **kwargs)

#         if description is None:
#             description = name
#         self.layout = QHBoxLayout()
#         self.name = name
#         self.checkbox = QCheckBox()
#         self.layout.addWidget(self.checkbox)
#         self.label = QLabel(description)
#         if tooltip is None:
#             tooltip = "api: " + name
#         else:
#             tooltip = "api: {}\n{}".format(name, tooltip)
#         self.label.setToolTip(tooltip)
#         self.layout.addWidget(self.label)
#         self.checkbox.clicked.connect(self.clicked)
#         self.setLayout(self.layout)

#     def update(self):
#         val = current_motor()[self.name].get()
#         self.checkbox.setChecked(val != "0")

#     def clicked(self, on):
#         if on:
#             current_motor()[self.name] = str(1)
#             print("{}=1".format(self.name))
#         else:
#             current_motor()[self.name] = str(0)
#             print("{}=0".format(self.name))

# class APIDir(APIBool):
#     def __init__(self, *args, **kwargs):
#         super(APIDir, self).__init__(*args, **kwargs)

#     def update(self):
#         val = float(current_motor()[self.name].get())
#         status = val == 1.0 or val == 0.0
#         self.checkbox.setChecked(status)

#     def clicked(self, on):
#         if on:
#             current_motor()[self.name] = str(1)
#             print("{}=1".format(self.name))
#         else:
#             current_motor()[self.name] = str(-1)
#             print("{}=0".format(self.name))

# class NumberEditSlider(NumberEdit):
#     def __init__(self, *args, **kwargs):
#         super(NumberEditSlider, self).__init__(*args, **kwargs)
#         self.slider = QSlider(Qt.Orientation.Horizontal)
#         self.slider.valueChanged.connect(self.valueChanged)
#         self.number_widget.editingFinished.connect(self.valueChangedEdit)
#         self.layout.addWidget(self.slider)
#         #self.setLayout(layout)

#     def valueChanged(self, value):
#         self.setNumber(value)
#         self.signal.emit(float(value))

#     def valueChangedEdit(self):
#         self.slider.setValue(int(float(self.number_widget.text())))

# class ParameterEdit(NumberEdit):
#     def __init__(self, *args, **kwargs):
#         super(ParameterEdit, self).__init__(*args, **kwargs)
#         self.signal.connect(self.set_value)

#     def refresh_value(self):
#         self.setNumber(current_motor()[self.name].get())

#     def set_value(self, value):
#         print("set {}={}".format(self.name, value))
#         current_motor()[self.name] = str(value)

# class StatusCombo(QWidget):
#     signal = pyqtSignal(str, str)
#     def __init__(self, *args, **kwargs):
#         super(StatusCombo, self).__init__(*args, **kwargs)

#         self.layout = QHBoxLayout()
#         self.combo_box = QComboBox()
#         self.layout.addWidget(self.combo_box)
#         self.text_widget = QLineEdit()
#         self.text_widget.editingFinished.connect(self.editingFinished)
#         self.layout.addWidget(self.text_widget)
#         self.setLayout(self.layout)


#     def setText(self, number):
#         self.text_widget.setText(str(number))

#     def editingFinished(self):
#         self.signal.emit(self.combo_box.currentText(), self.text_widget.text())

# class StatusTab(MotorTab):
#     def __init__(self, *args, **kwargs):
#         super(StatusTab, self).__init__(*args, **kwargs)
#         self.setAutoFillBackground(True)

#         self.name = "status"
#         #print("init: " + self.name)
#         #self.field_names = current_motor()["help"].get().split('\n')
#         self.field_names = current_motor().get_api_options()

#         self.statuses = []
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignTop)
#         layout.setContentsMargins(QMargins(0,0,0,0))
#         for i in range(5):
#             self.statuses.append(StatusCombo())
#             layout.addWidget(self.statuses[i])
#             self.statuses[i].signal.connect(self.valueEdit)
#             self.statuses[i].combo_box.addItems(self.field_names)
#         self.statuses[0].combo_box.setCurrentText("vbus")
#         self.setLayout(layout)


#     def valueEdit(self, s, v):
#         print("value edit: {}={}".format(s,v))
#         if v:
#             current_motor()[s] = v

#     def update(self):
#         super(StatusTab, self).update()
#         for status in self.statuses:
#             if not status.text_widget.hasFocus():
#                 val = current_motor()[status.combo_box.currentText()].get()
#                 status.setText(val)


# class PlotTab(MotorTab):
#     global motor_manager

#     def __init__(self):
#         super(PlotTab, self).__init__()

#         self.name = "plot"
#         self.update_time = 10

#         self.chart = QChart()
#         self.chart_view = QChartView(self.chart)
#         self.chart_view.setRubberBand(QChartView.VerticalRubberBand)
#         self.layout = QVBoxLayout()
#         self.combo_box = QComboBox()
#         self.combo_box.addItems(["motor_position", "joint_position", "iq", "torque"])
#         self.layout.addWidget(self.combo_box)
#         self.layout.addWidget(self.chart_view)
#         self.setLayout(self.layout)

#         self.series = QLineSeries()
#         self.chart.addSeries(self.series)
#         self.axis_x = QValueAxis()
#         self.axis_x.setTickCount(10)
#         self.axis_x.setTitleText("Time (s)")
#         self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
#         self.series.attachAxis(self.axis_x)
#         self.axis_y = QValueAxis()
#         self.axis_y.setTickCount(10)
#         self.axis_y.setTitleText("Value")
#         self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
#         self.series.attachAxis(self.axis_y)
#         self.axis_y.setRange(-100,100)

#         s = motor_manager.read()[0]
#         self.mcu_timestamp = s.mcu_timestamp
#         self.t_seconds = 0.0
#         self.series.append(0, getattr(s, self.combo_box.currentText()))


#     def update(self):
#         super(PlotTab, self).update()
#         s = self.status
#         self.t_seconds += (motor.diff_mcu_time(s.mcu_timestamp, self.mcu_timestamp))/cpu_frequency
#         self.mcu_timestamp = s.mcu_timestamp
#         self.series.append(self.t_seconds, getattr(s, self.combo_box.currentText()))
#         if len(self.series) > 500:
#             self.series.remove(0)
#         self.axis_x.setMax(self.t_seconds)
#         self.axis_x.setMin(self.series.at(0).x())
#         self.axis_y.setMin(min([d.y() for d in self.series.pointsVector()]))
#         self.axis_y.setMax(max([d.y() for d in self.series.pointsVector()]))


# class PlotTab2(MotorTab):
#     global motor_manager

#     def __init__(self):
#         super(PlotTab2, self).__init__()

#         self.name = "plot2"
#         self.update_time = 10

#         self.chart = QChart()
#         self.chart_view = QChartView(self.chart)
#         self.chart_view.setRubberBand(QChartView.VerticalRubberBand)
#         self.layout = QVBoxLayout()
#         self.combo_box = QComboBox()
#         self.field_names = current_motor()["help"].get().split('\n')
#         self.combo_box.addItems(self.field_names)
#         self.layout.addWidget(self.combo_box)
#         self.combo_box.setCurrentText("vbus")
#         self.layout.addWidget(self.chart_view)
#         self.setLayout(self.layout)

#         self.series = QLineSeries()
#         self.series.setUseOpenGL(True)
#         self.chart.addSeries(self.series)
#         self.axis_x = QValueAxis()
#         self.axis_x.setTickCount(10)
#         self.axis_x.setTitleText("Time (s)")
#         self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
#         self.series.attachAxis(self.axis_x)
#         self.axis_y = QValueAxis()
#         self.axis_y.setTickCount(10)
#         self.axis_y.setTitleText("Value")
#         self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
#         self.series.attachAxis(self.axis_y)
#         self.axis_y.setRange(-100,100)

#         self.combo_box.currentIndexChanged.connect(lambda: self.series.removeAll())

#         s = motor_manager.read()[0]
#         self.mcu_timestamp = s.mcu_timestamp
#         self.t_seconds = 0.0
#       #  val = current_motor()[self.combo_box.currentText()].get()
#       #  self.series.append(0, getattr(s, self.combo_box.currentText()))


#     def update(self):
#         super(PlotTab2, self).update()
#         s = self.status
#         self.t_seconds += (motor.diff_mcu_time(s.mcu_timestamp, self.mcu_timestamp))/cpu_frequency
#         self.mcu_timestamp = s.mcu_timestamp
#         val = current_motor()[self.combo_box.currentText()].get()
#         try:
#             self.series.append(self.t_seconds, float(val))
#             if len(self.series) > 500:
#                 self.series.remove(0)
#             self.axis_y.setMin(min([d.y() for d in self.series.pointsVector()]))
#             self.axis_y.setMax(max([d.y() for d in self.series.pointsVector()]))
#             self.axis_x.setMax(self.t_seconds)
#             self.axis_x.setMin(self.series.at(0).x())
#         except ValueError:
#             pass

# class VelocityTab(MotorTab):
#     def __init__(self, *args, **kwargs):
#         super(VelocityTab, self).__init__(*args, **kwargs)

#         self.update_time = 50

#         self.name = "velocity"
#         self.numbers = []
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignTop)
#         self.widget = NumberEditSlider("velocity")
#         #self.widget.number_widget.editingFinished.connect(self.position_update)
#         self.widget.slider.setMinimum(-1000)
#         self.widget.slider.setMaximum(1000)
#         self.widget.slider.setPageStep(50)
#         self.widget.signal.connect(self.velocity_update)

#         self.chart = QChart()
#         self.chart_view = QChartView(self.chart)
#         self.chart_view.setRubberBand(QChartView.VerticalRubberBand)
#         self.series = QLineSeries()
#         self.series.setUseOpenGL(True)
#         self.chart.addSeries(self.series)
#         self.axis_x = QValueAxis()
#         self.axis_x.setTickCount(10)
#         self.axis_x.setTitleText("Time (s)")
#         self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
#         self.series.attachAxis(self.axis_x)
#         self.axis_y = QValueAxis()
#         self.axis_y.setTickCount(10)
#         self.axis_y.setTitleText("Motor velocity (rad/s)")
#         self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
#         self.series.attachAxis(self.axis_y)
#         self.axis_y.setRange(-100,100)

#         parameter_layout = QGridLayout()
#         self.kp = ParameterEdit("vkp","kp")
#         self.ki = ParameterEdit("vki","ki")
#         self.max = ParameterEdit("vmax","current limit")
#         self.max.signal.connect(lambda val: current_motor()["vki_limit"].set(str(val)))
#         self.accel = ParameterEdit("vacceleration_limit","acceleration limit")
#         self.imax = ParameterEdit("imax","voltage limit")
#         self.imax.signal.connect(self.set_imax)
#         self.filter = ParameterEdit("voutput_filt", "output filter")

#         parameter_layout.addWidget(self.kp,0,0)
#         parameter_layout.addWidget(self.ki,0,1)
#         parameter_layout.addWidget(self.max,1,0)
#         parameter_layout.addWidget(self.accel,1,1)
#         parameter_layout.addWidget(self.imax,2,0)
#         parameter_layout.addWidget(self.filter,2,1)

#         layout.addWidget(self.widget)
#         self.velocity_measured = NumberDisplay("velocity measured")
#         layout.addWidget(self.chart_view)
#         layout.addWidget(self.velocity_measured)
#         layout.addLayout(parameter_layout)
#         self.setLayout(layout)
#         self.mcu_timestamp = 0
#         self.motor_position = 0
#         self.t_seconds = 0.0

#     def update(self):
#         super(VelocityTab, self).update()
#         dt = (motor.diff_mcu_time(self.status.mcu_timestamp, self.mcu_timestamp))/cpu_frequency
#         self.t_seconds += dt
#         self.mcu_timestamp = self.status.mcu_timestamp
#         dp = self.status.motor_position - self.motor_position
#         self.motor_position = self.status.motor_position
#         self.velocity_measured.setNumber(dp/dt)

#         if (abs(dp/dt) < 10000):
#             # reject rollovers
#             try:
#                 self.series.append(self.t_seconds, dp/dt)
#                 if len(self.series) > 200:
#                     self.series.remove(0)
#                 self.axis_y.setMin(min([d.y() for d in self.series.pointsVector()]))
#                 self.axis_y.setMax(max([d.y() for d in self.series.pointsVector()]))
#                 self.axis_x.setMax(self.t_seconds)
#                 self.axis_x.setMin(self.series.at(0).x())
#             except ValueError:
#                 pass

#     def velocity_update(self):
#         p = float(self.widget.number_widget.text())
#         print("velocity command " + str(p))
#         motor_manager.set_command_velocity([p])
#         motor_manager.set_command_mode(motor.ModeDesired.Velocity)
#         motor_manager.write_saved_commands()

#     def set_imax(self, val):
#         current_motor()["imax"].set(str(val))
#         current_motor()["idmax"].set(str(val))
#         current_motor()["iki_limit"].set(str(val))
#         current_motor()["idki_limit"].set(str(val))

#     def unpause(self):
#         self.kp.refresh_value()
#         self.ki.refresh_value()
#         self.max.refresh_value()
#         self.imax.refresh_value()
#         self.accel.refresh_value()
#         self.filter.refresh_value()
#         return super().unpause()


# class LogTab(MotorTab):
#     def __init__(self, *args, **kwargs):
#         super(LogTab, self).__init__(*args, **kwargs)

#         self.name = "log"
#         self.numbers = []

#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignTop)
#         self.widget = QPlainTextEdit()

#         layout.addWidget(self.widget)
#         self.setLayout(layout)

#     def update(self):
#         super(LogTab, self).update()
#         while True:
#             log = current_motor()["log"].get()
#             if log == "log end":
#                 break
#             else:
#                 self.widget.appendPlainText(log)

# class CalibrateTab(MotorTab):
#     def __init__(self, *args, **kwargs):
#         super(CalibrateTab, self).__init__(*args, **kwargs)

#         self.name = "calibrate"
#         self.numbers = []

#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignTop)
#         self.index_offset = APIDisplay("index_offset_measured")
#         layout.addWidget(self.index_offset)

#         self.current_d = APIDisplay("id", "id measured (A)")
#         layout.addWidget(self.current_d)

#         self.phase_lock_current = NumberEdit("phase lock current (A)", tooltip="command.current_desired")
#         self.phase_lock_current.setNumber(current_motor()["startup_phase_lock_current"])
#         layout.addWidget(self.phase_lock_current)

#         mode_layout = QHBoxLayout()
#         self.button = QPushButton("phase lock")
#         self.button.setToolTip("command.mode_desired = PHASE_LOCK")
#         self.button.clicked.connect(self.phase_lock)
#         mode_layout.addWidget(self.button)

#         self.obutton = QPushButton("open")
#         self.obutton.setToolTip("command.mode_desired = OPEN")
#         self.obutton.clicked.connect(mode_open)
#         mode_layout.addWidget(self.obutton)

#         self.jbutton = QPushButton("joint position")
#         self.jbutton.setToolTip("command.mode_desired = JOINT_POSITION")
#         self.jbutton.clicked.connect(self.joint_position)
#         mode_layout.addWidget(self.jbutton)

#         layout.addLayout(mode_layout)

#         boollayout = QHBoxLayout()
#         self.position_limits_disable = APIBool("disable_position_limits", "disable position limits")
#         self.phase_mode = APIBool("phase_mode", "phase mode", "fast_loop_param.phase_mode")
#         boollayout.addWidget(self.position_limits_disable)
#         boollayout.addWidget(self.phase_mode)
#         layout.addLayout(boollayout)


#         self.obias = APIEdit("obias", "output bias (rad)", "main_loop_param.output_encoder.bias")
#         self.obias.signal.connect(self.obias_set)
#         self.oposition = NumberDisplay("output position (rad)", tooltip="status.joint_position")
#         self.odir = APIDir("odir", "output position dir", "main_loop_param.output_encoder.dir")
#         olayout = QHBoxLayout()
#         olayout.addWidget(self.obias)
#         olayout.addWidget(self.oposition)
#         olayout.addWidget(self.odir)
#         layout.addLayout(olayout)

#         self.mbias = APIEdit("startup_mbias", "startup motor bias (rad)", "also calls set_startup_bias\nstartup_param.motor_encoder_bias")
#         self.mbias.signal.connect(self.mbias_set)
#         self.mposition_raw = APIDisplay("motor_position_raw", "motor abs position (rad)")
#         self.mposition = NumberDisplay("motor position (rad)", tooltip="status.motor_position")
#         self.mdir = APIDir("mdir", "motor position dir", "fast_loop_param.motor_encoder.dir")

#         mlayout = QHBoxLayout()
#         mlayout.addWidget(self.mbias)
#         mlayout.addWidget(self.mposition_raw)
#         mlayout.addWidget(self.mposition)
#         mlayout.addWidget(self.mdir)
#         layout.addLayout(mlayout)

#         self.tbias = APIEdit("tbias", "torque bias (Nm)", "main_loop_param.torque_sensor.bias")
#         self.torque = NumberDisplay("torque (Nm)", tooltip="status.torque")
#         self.tdir = APIDir("tdir", "torque dir", "main_loop_param.torque_sensor.dir")
#         tlayout = QHBoxLayout()
#         tlayout.addWidget(self.tbias)
#         tlayout.addWidget(self.torque)
#         tlayout.addWidget(self.tdir)
#         layout.addLayout(tlayout)

#         self.setLayout(layout)

#     def update(self):
#         super(CalibrateTab, self).update()
#         self.index_offset.update()
#         self.current_d.update()
#         self.oposition.setNumber(self.status.joint_position)
#         self.mposition.setNumber(self.status.motor_position)
#         self.odir.update()
#         self.torque.setNumber(self.status.torque)
#         mposition_raw = float(current_motor()[self.mposition_raw.name].get()) % 2*np.pi
#         if mposition_raw > np.pi:
#             mposition_raw -= 2*np.pi
#         self.mposition_raw.setNumber(mposition_raw)
#         self.obias.update()
#         self.mbias.update()
#         self.mdir.update()
#         self.phase_mode.update()
#         self.position_limits_disable.update()
#         self.tbias.update()
#         self.tdir.update()

#     def phase_lock(self):
#         print("phase lock")
#         motor_manager.set_command_mode(motor.ModeDesired.PhaseLock)
#         motor_manager.set_command_current([self.phase_lock_current.getNumber()])
#         motor_manager.write_saved_commands()

#     def joint_position(self):
#         print("joint position")
#         motor_manager.set_commands([motor.Command()])
#         motor_manager.set_command_mode(motor.ModeDesired.JointPosition)
#         motor_manager.write_saved_commands()


#     def mbias_set(self):
#         print("setting mbias")
#         current_motor()["set_startup_bias"].get()

#     def obias_set(self):
#         pass

# class MainWindow(QMainWindow):

#     def __init__(self):
#         super(MainWindow, self).__init__()
#         global motor_manager
#         motor_manager = motor.MotorManager()
#         self.simulated = False
#         motors = None
#         if "-simulated" in QCoreApplication.arguments():
#             self.simulated = True
#             motors = motor_manager.get_motors_by_name(["sim1", "sim2"], connect=False, allow_simulated = True)
#         else:
#             motors = motor_manager.get_connected_motors(connect=False)
#         print(motors)
#         self.menu_bar = QMenuBar(self)
#         self.motor_menu = QMenu("&Motor")
#         self.menu_bar.addMenu(self.motor_menu)
#         self.setMenuBar(self.menu_bar)
#         actions = []
#         for m in motors:
#             actions.append(self.motor_menu.addAction(m.name()))
#             print(m.name())
#         self.motor_menu.triggered.connect(lambda action: self.connect_motor(action.text()))
#         self.connect_motor(motors[0].name())

#         self.tabs = QTabWidget()
#         self.tabs.setTabPosition(QTabWidget.TabPosition.West)

#         self.tuning_tab = QTabWidget()
#         self.tuning_tab.setTabPosition(QTabWidget.TabPosition.West)
#         self.tuning_tab.unpause = None


#         self.tabs.addTab(FaultTab(), "fault")
#         self.tabs.addTab(StatusTab(), "status")
#         self.tabs.addTab(PlotTab(), "plot")
#         self.tabs.addTab(PlotTab2(), "plot2")
#         self.tabs.addTab(VelocityTab(), "velocity")
#         self.tabs.addTab(LogTab(), "log")
#         #self.tabs.addTab(self.tuning_tab, "tuning")
#         self.tabs.addTab(CalibrateTab(), "calibrate")
#         self.tabs.addTab(CurrentTuningTab(), "current tuning")
#         self.tabs.addTab(PositionTuningTab(), "position tuning")

#         self.setCentralWidget(self.tabs)
#         self.last_tab = self.tabs.currentWidget()
#         self.last_tab.unpause()

#         self.last_tuning_tab = self.tuning_tab.currentWidget()

#         self.tabs.currentChanged.connect(self.new_tab)
#         self.tuning_tab.currentChanged.connect(self.new_tuning_tab)
#         if "-fullscreen" in QCoreApplication.arguments():
#             self.showFullScreen()

#     def connect_motor(self, name):
#          global cpu_frequency
#          print("Connecting motor " + name)
#          motor_manager.get_motors_by_name([name], allow_simulated = self.simulated)
#          motor_manager.set_auto_count()
#          self.setWindowTitle(name + " sn:" + current_motor().serial_number())
#          cpu_frequency = current_motor().get_cpu_frequency()

#     def new_tab(self, index):
#         #print("last tab " + str(index) + " " + self.last_tab.name)
#         self.last_tab.pause()
#         #print("new tab " + str(index) + " " + self.tabs.widget(index).name)
#         self.tabs.widget(index).unpause()
#         self.last_tab = self.tabs.widget(index)

#     def new_tuning_tab(self, index):
#         pass
#        # self.last_tuning_tab.pause()
#         #self.tuning_tab.widget(index).unpause()
#         #self.last_tuning_tab = self.tuning_tab.widget(index)


# class PositionTuningTab(MotorTab):
#     def __init__(self, *args, **kwargs):
#         super(PositionTuningTab, self).__init__(*args, **kwargs)

#         self.name = "position_tuning"
#         self.command = motor.Command()
#         self.command.mode_desired = motor.ModeDesired.PositionTuning
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignTop)

#         self.amplitude = NumberEditSlider("amplitude (rad)")
#         self.amplitude.slider.setMinimum(-100)
#         self.amplitude.slider.setMaximum(100)
#         self.amplitude.slider.setPageStep(5)
#         self.amplitude.signal.connect(self.amplitude_update)
#         layout.addWidget(self.amplitude)

#         self.bias = NumberEditSlider("bias (rad)")
#         self.bias.slider.setMinimum(-100)
#         self.bias.slider.setMaximum(100)
#         self.bias.slider.setPageStep(5)
#         self.bias.signal.connect(self.bias_update)
#         layout.addWidget(self.bias)

#         self.frequency = NumberEditSlider("frequency (Hz)")
#         self.frequency.slider.setMinimum(0)
#         self.frequency.slider.setMaximum(100)
#         self.frequency.slider.setPageStep(5)
#         self.frequency.signal.connect(self.frequency_update)
#         layout.addWidget(self.frequency)

#         self.mode = QComboBox()
#         self.mode.addItems(motor.TuningMode.__members__)
#         self.mode.currentTextChanged.connect(self.mode_update)
#         layout.addWidget(self.mode)

#         parameter_layout = QGridLayout()
#         self.kp = ParameterEdit("kp", "kp (A/rad)")
#         self.kd = ParameterEdit("kd", "kd (A*s/rad)")
#         #self.ki_limit = ParameterEdit("ki_limit")
#         self.command_max = ParameterEdit("max", "command max (A)")
#         parameter_layout.addWidget(self.kp,0,0)
#         parameter_layout.addWidget(self.kd,0,1)
#         #parameter_layout.addWidget(self.ki_limit,1,0)
#         parameter_layout.addWidget(self.command_max,1,0)
#         layout.addLayout(parameter_layout)

#         self.setLayout(layout)

#     def update(self):
#         super(PositionTuningTab, self).update()

#     def unpause(self):
#         self.kp.refresh_value()
#         self.kd.refresh_value()
#         self.command_max.refresh_value()
#         return super().unpause()

#     def command_update(self):
#         print(self.command)
#         motor_manager.write([self.command])

#     def amplitude_update(self):
#         self.command.position_tuning.amplitude = float(self.amplitude.number_widget.text())
#         print("amplitude: {}".format(self.command.current_tuning.amplitude))
#         self.command_update()

#     def bias_update(self):
#         self.command.position_tuning.bias = float(self.bias.number_widget.text())
#         self.command_update()

#     def frequency_update(self):
#         self.command.position_tuning.frequency = float(self.frequency.number_widget.text())
#         self.command_update()

#     def mode_update(self, selection):
#         self.command.position_tuning.mode = int(motor.TuningMode.__members__[selection])
#         self.command_update()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.api_connection = motor_widgets.ApiConnection()
        motors = self.api_connection.motor_manager.get_connected_motors(
            connect=False
        )
        self.menu_bar = QMenuBar(self)
        self.motor_menu = QMenu("&Motor")
        self.menu_bar.addMenu(self.motor_menu)
        self.setMenuBar(self.menu_bar)
        actions = [self.motor_menu.addAction(m.name()) for m in motors]
        self.motor_menu.triggered.connect(
            lambda action: self.connect_motor(action.text())
        )
        self.api_connection.connect_motor(motors[0].name())

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)

        self.tabs.addTab(motor_fault.FaultTab(self.api_connection), "fault")
        self.tabs.addTab(
            motor_current_tuning.CurrentTuningTab(self.api_connection), "current tuning"
        )
        # self.tabs.addTab(StatusTab(), 'status')
        # self.tabs.addTab(PlotTab(), 'plot')
        # self.tabs.addTab(PlotTab2(), 'plot2')
        # self.tabs.addTab(VelocityTab(), 'velocity')
        # self.tabs.addTab(LogTab(), 'log')
        # self.tabs.addTab(CalibrateTab(), 'calibrate')

        # self.tabs.addTab(PositionTuningTab(), 'position tuning')

        self.tabs.currentChanged.connect(self.new_tab)

        self.setCentralWidget(self.tabs)
        self.last_tab = self.tabs.currentWidget()
        self.last_tab.unpause()

        if "-fullscreen" in QCoreApplication.arguments():
            self.showFullScreen()

    def connect_motor(self, name):
        print(f"Connecting motor: {name}")
        self.last_tab.pause()
        self.api_connection.connect_motor(name)
        self.setWindowTitle(
            f"{name} sn: {self.api_connection.current_motor.serial_number()}"
        )
        self.last_tab.unpause()

    def new_tab(self, index):
        self.last_tab.pause()
        self.tabs.widget(index).unpause()
        self.last_tab = self.tabs.widget(index)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
