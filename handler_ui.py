from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5 import uic
from datetime import datetime

form_class = uic.loadUiType("SMCommandCenter.ui")[0]

class HandlerUI(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1340, 880)

        self.serial_handler = None
        self.plot_handler = None
        self.command_handler = None

        # 버튼 이벤트 연결
        self.PB_SER_REFRESH.clicked.connect(self.refresh_ports)
        self.PB_SER_CONN.clicked.connect(self.connect_serial)
        self.PB_SER_CONN.setCheckable(True)

        self.PB_TX_SV1.clicked.connect(self.send_sv1)
        self.PB_TX_SV1.setCheckable(True)

        self.PB_TX_SV2.clicked.connect(self.send_sv2)
        self.PB_TX_SV2.setCheckable(True)

        self.PB_TX_IG.clicked.connect(self.send_ig)
        self.PB_TX_IG.setCheckable(True)

        self.PB_TX_SEQSTART.clicked.connect(self.send_seqstart)
        self.PB_TX_SEQSTOP.clicked.connect(self.send_seqstop)

        self.PB_LOG.clicked.connect(self.start_log)
        self.PB_LOG.setCheckable(True)


    def set_serial_handler(self, serial_handler):
        self.serial_handler = serial_handler

    def set_plot_handler(self, plot_handler):
        self.plot_handler = plot_handler

    def set_command_handler(self, command_handler):
        self.command_handler = command_handler


    def refresh_ports(self):
        self.CB_SER_PORT.clear()
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            self.CB_SER_PORT.addItem(f"{port.portName()} - {port.description()}", port.portName())
        if not available_ports:
            self.CB_SER_PORT.addItem("No ports available")

    def connect_serial(self):
        if self.serial_handler:
            self.serial_handler.connect_serial()


    def send_sv1(self):
        if self.command_handler:
            if self.PB_TX_SV1.isChecked():
                command = "{\"sv1\":1}"
            else:
                command = "{\"sv1\":0}"
            self.command_handler.send_command(command)
            curr_datetime = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            command = curr_datetime + " : " + command
            self.TE_TX_JSON.append(f"{command}")

    def send_sv2(self):
        if self.command_handler:
            if self.PB_TX_SV2.isChecked():
                command = "{\"sv2\":1}"
            else:
                command = "{\"sv2\":0}"
            self.command_handler.send_command(command)
            curr_datetime = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            command = curr_datetime + " : " + command
            self.TE_TX_JSON.append(f"{command}")

    def send_ig(self):
        if self.command_handler:
            if self.PB_TX_IG.isChecked():
                command = "{\"ig\":1}"
            else:
                command = "{\"ig\":0}"
            self.command_handler.send_command(command)
            curr_datetime = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            command = curr_datetime + " : " + command
            self.TE_TX_JSON.append(f"{command}")

    def send_seqstart(self):
        if self.command_handler:
            command = "{\"seq\":1}"
            self.command_handler.send_command(command)
            curr_datetime = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            command = curr_datetime + " : " + command
            self.TE_TX_JSON.append(f"{command}")

    def send_seqstop(self):
        if self.command_handler:
            command = "{\"seq\":0}"
            self.command_handler.send_command(command)
            curr_datetime = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            command = curr_datetime + " : " + command
            self.TE_TX_JSON.append(f"{command}")

    def start_log(self):
        if self.PB_LOG.isChecked():
            print('log start')  # TODO : implement
        else:
            print('log stop')
