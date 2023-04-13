import motor
import motor_widgets

import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtChart import QChart
from PyQt5.QtChart import QChartView
from PyQt5.QtChart import QLineSeries
from PyQt5.QtChart import QValueAxis


def _make_current_tuning_combobox() -> QComboBox:
    combobox = QComboBox()
    combobox.addItem("sine-wave", userData=motor.Sine)
    combobox.addItem("square-wave", userData=motor.Square)
    combobox.addItem("chirp", userData=motor.Chirp)
    combobox.setEditable(False)
    combobox.setToolTip("current tuning mode")
    return combobox


class CurrentTuningChartView(QChartView):
    def __init__(self, *args, **kwargs):
        chart = QChart()
        super(CurrentTuningChartView, self).__init__(chart, *args, **kwargs)
        self.setRubberBand(QChartView.VerticalRubberBand)
        self.axis_x = QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setTitleText("time [ms]")
        chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.axis_y = QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setRange(-100, 100)
        self.axis_y.setTitleText("current [A]")
        chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)

        self.series_iq_des = QLineSeries()
        self.series_iq_des.setName("desired")
        chart.addSeries(self.series_iq_des)
        self.series_iq_des.attachAxis(self.axis_x)
        self.series_iq_des.attachAxis(self.axis_y)

        self.series_iq_mes = QLineSeries()
        self.series_iq_mes.setName("measured (filt)")
        chart.addSeries(self.series_iq_mes)
        self.series_iq_mes.attachAxis(self.axis_x)
        self.series_iq_mes.attachAxis(self.axis_y)

    def update(
        self, time_ms: np.ndarray, iq_des: np.ndarray, iq_mes: np.ndarray
    ):
        xy_iq_des = [QPointF(x, y) for x, y in zip(time_ms, iq_des)]
        xy_iq_mes = [QPointF(x, y) for x, y in zip(time_ms, iq_mes)]

        self.series_iq_des.replace(xy_iq_des)
        self.series_iq_mes.replace(xy_iq_mes)
        min_y = np.min([iq_des.min(), iq_mes.min()])
        max_y = np.max([iq_des.max(), iq_mes.max()])

        self.axis_y.setMin(min_y)
        self.axis_y.setMax(max_y)
        self.axis_x.setMin(time_ms.min())
        self.axis_x.setMax(time_ms.max())


class CurrentTuningMeasurementFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super(CurrentTuningMeasurementFrame, self).__init__(*args, **kwargs)
        measure_layout = QGridLayout()
        self.statuses = {}
        specification = [
            ("frequency desired", "Hz", 1),
            ("frequency measured", "Hz", 1),
            ("magnitude desired", "A", 2),
            ("magnitude measured", "A", 2),
            ("gain", "", 2),
            ("phase", "deg", 2),
        ]
        for cnt, (name, units, decimals) in enumerate(specification):
            row = cnt % 2
            column = int(0.5 * cnt)
            self.statuses[name] = motor_widgets.DoubleLineStatus(
                name, units=units, decimals=decimals
            )
            measure_layout.addWidget(QLabel(name), row, 2 * column)
            measure_layout.addWidget(self.statuses[name], row, 2 * column + 1)
            column += 1
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLayout(measure_layout)

    def update(
        self,
        freq_des: float,
        freq_mes: float,
        mag_des: float,
        mag_mes: float,
        gain: float,
        phase: float,
    ):
        self.statuses["frequency desired"].setValue(freq_des)
        self.statuses["frequency measured"].setValue(freq_mes)
        self.statuses["magnitude desired"].setValue(mag_des)
        self.statuses["magnitude measured"].setValue(mag_mes)
        self.statuses["gain"].setValue(gain)
        self.statuses["phase"].setValue(phase)


class CurrentTuningGainsFrame(QFrame):
    def __init__(self, api_connection, *args, **kwargs):
        super(CurrentTuningGainsFrame, self).__init__(*args, **kwargs)
        self.api_connection = api_connection
        frame_layout = QGridLayout()
        self.inputs = {}

        def _add_widget(description, name, row, col):
            frame_layout.addWidget(QLabel(description), row, 2 * col)
            frame_layout.addWidget(self.inputs[name], row, 2 * col + 1)

        def _link_widgets(leader_name: str, follower_name: str):
            leader = self.inputs[leader_name]
            follower = self.inputs[follower_name]
            leader.valueChanged.connect(follower.setValue)

        specification = [
            ("iq kp", "ikp", "V/A", 0.1, 0, 100, 2),
            ("iq ki", "iki", "V/(A*h)", 0.1, 0, 100, 2),
            ("iq ki-limit", "iki_limit", "V", 0.1, 0, 1000, 1),
            ("iq max", "imax", "V", 0.1, 0, 1000, 1),
            ("iq filter", "iq_filter", "Hz", 1000.0, 0, 1000000, 0),
            ("id kp", "idkp", "V/A", 0.1, 0, 100, 2),
            ("id ki", "idki", "V/(A*h)", 0.1, 0, 100, 2),
            ("id ki-limit", "idki_limit", "V", 0.1, 0, 1000, 1),
            ("id max", "idmax", "V", 0.1, 0, 1000, 1),
            ("id filter", "id_filter", "Hz", 1000.0, 0, 1000000, 0),
        ]
        for cnt, (
            description,
            name,
            units,
            increment,
            minimum,
            maximum,
            decimals,
        ) in enumerate(specification):
            self.inputs[name] = motor_widgets.DoubleParameterSpinBox(
                name,
                api_connection,
                increment=increment,
                minimum=minimum,
                maximum=maximum,
                units=units,
                decimals=decimals,
            )
            row = int(cnt / 5)
            col = cnt % 5
            _add_widget(description, name, row, col)
        _link_widgets("ikp", "idkp")
        _link_widgets("iki", "idki")
        _link_widgets("iki_limit", "idki_limit")
        _link_widgets("imax", "idmax")
        _link_widgets("iq_filter", "id_filter")
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLayout(frame_layout)

    def update(self):
        for name in self.inputs:
            self.inputs[name].update()


class CurrentTuningCommandFrame(QFrame):
    def __init__(self, api_connection, *args, **kwargs):
        super(CurrentTuningCommandFrame, self).__init__(*args, **kwargs)
        self.api_connection = api_connection
        self.running = False
        frame_layout = QGridLayout()

        def _add_widget(name, row):
            frame_layout.addWidget(QLabel(name), row, 0)
            frame_layout.addWidget(self.inputs[name], row, 1)

        self.inputs = {"mode": _make_current_tuning_combobox()}
        _add_widget("mode", 0)
        specification = [
            ("amplitude", "A", 0.0, 0.1, 0, 100),
            ("bias", "A", 0.0, 0.1, -100, 100),
            ("frequency", "Hz", 1000.0, 100.0, 0, 100000),
        ]
        for row, (
            name,
            units,
            default_value,
            increment,
            minimum,
            maximum,
        ) in enumerate(specification, start=1):
            spinbox = QDoubleSpinBox()
            spinbox.setSuffix(f" [{units}]")
            spinbox.setSingleStep(increment)
            spinbox.setRange(minimum, maximum)
            spinbox.setValue(default_value)
            spinbox.setToolTip(name)
            self.inputs[name] = spinbox
            _add_widget(name, row)

        button = QPushButton("Start")
        button.clicked.connect(self.start_clicked)
        frame_layout.addWidget(button)
        button = QPushButton("Stop")
        button.clicked.connect(self.stop_clicked)
        frame_layout.addWidget(button)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLayout(frame_layout)

    def start_clicked(self):
        command = motor.Command(
            host_timestamp=self.api_connection.pseudo_time(),
            mode=motor.CurrentTuning,
        )
        command.current_tuning.amplitude = self.inputs["amplitude"].value()
        command.current_tuning.frequency = self.inputs["frequency"].value()
        command.current_tuning.bias = self.inputs["bias"].value()
        command.current_tuning.mode = self.inputs["mode"].currentData()
        self.api_connection.motor_manager.write([command])
        self.running = True

    def stop_clicked(self):
        self.running = False
        self.api_connection.command_open()


class CurrentTuningTab(motor_widgets.ApiTab):
    def __init__(
        self,
        api_connection: motor_widgets.ApiConnection,
        **kwargs,
    ):
        super(CurrentTuningTab, self).__init__(
            "current_tuning", api_connection, **kwargs
        )
        self.freq = np.linspace(0, 10000, 10000 // 5 + 1)

        # Create the main layout-box.
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create the chart.
        self.chart_view = CurrentTuningChartView()

        # Create the measurements panel.
        self.measurements_frame = CurrentTuningMeasurementFrame()

        # Create the gains frame.
        self.gains_frame = CurrentTuningGainsFrame(api_connection)

        # Create the tuning command frame.
        self.command_frame = CurrentTuningCommandFrame(api_connection)

        layout.addWidget(self.chart_view)
        layout.addWidget(self.measurements_frame)
        layout.addWidget(self.gains_frame)
        layout.addWidget(self.command_frame)
        self.setLayout(layout)

    def update(self):
        if not self.command_frame.running:
            return

        super(CurrentTuningTab, self).update()

        def _check(key):
            if key in data:
                return np.array(data[key])
            else:
                raise ValueError(f"Unable to find {key}")

        try:
            data = self.api_connection.current_motor.get_fast_log()
            time_s = _check("timestamp") / self.api_connection.cpu_frequency
            iq_des = _check("iq_des")
            iq_mes = _check("iq_meas_filt")
        except ValueError as e:
            print(f"Bad update, error={e}")
            return
        # Shift time (doesn't handle roll-over).
        time_s -= time_s[0]
        time_ms = 1000.0 * time_s
        # Check the line below ... shouldn't this len(self.freq)?
        filter_halfwidth_size = 0.5 * len(iq_des)

        # DFT decomposition gives the k, xf (DFT coefficients)
        # for a discrete signal 's' of length N.
        # k = 0..N-1
        # xf[k] = sum_{n=0..N-1} s[n] * exp(-2*pi*j*(k * n/N))
        # And it has an inverse:
        # s[n] = 1/N * sum_{k=0..N-1} xf[k] * exp(2*pi*j*(k * n/N))

        # In matrix form this could be:
        # xf = M @ s
        # Where M is len(xf) x len(s) and M is:
        # M[r][c] = exp(-j*2*pi*r*c/N)

        # Given that the signal is T long with N-samples, the largest
        # frequency is 0.5 * N / T
        sample_frequency = 1.0 / np.mean(np.diff(time_s))
        num_samples = len(time_s)
        num_halfwidth = int(0.5 * num_samples)
        fft_freq = np.fft.fftfreq(num_samples) * sample_frequency

        fft_iq_des = np.fft.fft(iq_des)
        idx_max_fft_iq_des = np.argmax(np.abs(fft_iq_des[1:num_halfwidth])) + 1
        max_fft_iq_des = fft_iq_des[idx_max_fft_iq_des]
        mag_max_iq_des = np.abs(max_fft_iq_des) / num_halfwidth
        ang_max_iq_des = np.angle(max_fft_iq_des)

        fft_iq_mes = np.fft.fft(iq_mes)
        idx_max_fft_iq_mes = np.argmax(np.abs(fft_iq_mes[1:num_halfwidth])) + 1
        max_fft_iq_mes = fft_iq_mes[idx_max_fft_iq_mes]
        mag_max_iq_mes = np.abs(max_fft_iq_mes) / num_halfwidth
        ang_max_iq_mes = np.angle(max_fft_iq_mes)

        gain = mag_max_iq_mes / mag_max_iq_des
        phase_deg = np.rad2deg(ang_max_iq_mes - ang_max_iq_des)
        self.measurements_frame.update(
            fft_freq[idx_max_fft_iq_des],
            fft_freq[idx_max_fft_iq_mes],
            mag_max_iq_des,
            mag_max_iq_mes,
            gain,
            phase_deg,
        )

        # jomega = np.exp(2j * np.pi * np.outer(self.freq, time_s))
        # fft_iq_des = jomega @ iq_des
        # idx_max_freq_iq_des = np.argmax(np.abs(fft_iq_des))
        # max_freq_iq_des = fft_iq_des[idx_max_freq_iq_des]
        # mag_max_freq_iq_des = np.abs(max_freq_iq_des) / filter_halfwidth_size
        # ang_max_freq_iq_des = np.angle(max_freq_iq_des)

        # fft_iq_mes = jomega @ iq_mes
        # idx_max_freq_iq_mes = np.argmax(np.abs(fft_iq_mes))
        # max_freq_iq_mes = fft_iq_mes[idx_max_freq_iq_mes]
        # mag_max_freq_iq_mes = np.abs(max_freq_iq_mes) / filter_halfwidth_size
        # ang_max_freq_iq_mes = np.angle(max_freq_iq_mes)

        # gain = mag_max_freq_iq_mes / mag_max_freq_iq_des
        # phase_deg = -(ang_max_freq_iq_mes - ang_max_freq_iq_des) * 180 / np.pi
        # self.measurements_frame.update(
        #     self.freq[idx_max_freq_iq_des],
        #     self.freq[idx_max_freq_iq_mes],
        #     mag_max_freq_iq_des,
        #     mag_max_freq_iq_mes,
        #     gain,
        #     phase_deg,
        # )

        self.chart_view.update(time_ms, iq_des, iq_mes)

    def unpause(self):
        super(CurrentTuningTab, self).unpause()
        self.gains_frame.update()
