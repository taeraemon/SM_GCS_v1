import os
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QMessageBox
import json
from datetime import datetime

class HandlerSerial:
    f_rx = None
    log_flag = False
    
    def __init__(self, controller):
        self.controller = controller
        self.serial_port = QSerialPort()
        self.serial_connected = False

    def log_start(self):
        self.log_flag = True

        # Get the directory of the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the log file path relative to the script directory
        log_dir = os.path.join(base_dir, 'log')
        os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists

        log_file = os.path.join(log_dir, datetime.now().strftime('%Y%m%d_%H%M%S') + '_rx.csv')
        self.f_rx = open(log_file, "w")

    def log_stop(self):
        self.log_flag = False
        self.f_rx.close()

    def connect_serial(self):
        selected_port = self.controller.ui.CB_SER_PORT.currentData()
        if not self.serial_connected:
            self.serial_port.setPortName(selected_port)
            self.serial_port.setBaudRate(int(self.controller.ui.LE_SER_BAUD.text()))
            self.serial_port.setDataBits(QSerialPort.Data8)
            self.serial_port.setParity(QSerialPort.NoParity)
            self.serial_port.setStopBits(QSerialPort.OneStop)
            self.serial_port.setFlowControl(QSerialPort.NoFlowControl)

            if self.serial_port.open(QIODevice.ReadWrite):
                self.serial_connected = True
                self.controller.ui.PB_SER_CONN.setText("Connected!")
                self.serial_port.readyRead.connect(self.handle_ready_read)
            else:
                QMessageBox.critical(self.controller.ui, "Error", "Failed to open serial port.")
        else:
            self.serial_connected = False
            self.serial_port.close()
            self.controller.ui.PB_SER_CONN.setText("Connect\nSerial")

    def handle_ready_read(self):
        while self.serial_port.canReadLine():
            line = self.serial_port.readLine().data().decode("utf-8").strip()
            if line[0] == '{':
                try:
                    data = json.loads(line)

                    curr_datetime = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    print(curr_datetime, ' | Packet Size : ', len(line))

                    recv_tc1_raw = data.get("tc1_raw", -1.0)
                    recv_tc2_raw = data.get("tc2_raw", -1.0)
                    recv_tc3_raw = data.get("tc3_raw", -1.0)
                    recv_pt1_raw = data.get("pt1_raw", -1.0)
                    recv_pt2_raw = data.get("pt2_raw", -1.0)
                    # recv_pt3_raw = data.get("pt3_raw", -1.0)
                    recv_lc1_raw = data.get("lc1_raw", -1.0)

                    self.controller.plot_handler_tc1.update_plot(recv_tc1_raw)
                    self.controller.plot_handler_tc2.update_plot(recv_tc2_raw)
                    self.controller.plot_handler_tc3.update_plot(recv_tc3_raw)
                    self.controller.plot_handler_pt1.update_plot(recv_pt1_raw)
                    self.controller.plot_handler_pt2.update_plot(recv_pt2_raw)
                    # self.controller.plot_handler_pt3.update_plot(recv_pt3_raw)
                    self.controller.plot_handler_lc1.update_plot(recv_lc1_raw)

                    # self.controller.ui.TE_RX_JSON.setText(line)
                    pretty_data = json.dumps(data, indent=4, ensure_ascii=False)  # 보기 좋게 포매팅
                    self.controller.ui.TE_RX_JSON.setText(pretty_data)

                    if self.log_flag:
                        self.f_rx.write(str(data)+'\n')
                except ValueError:
                    print(f"Invalid data: {line}")
            else:
                print("Debug Msg : ", line)

                # 기존 텍스트 가져오기
                text_edit = self.controller.ui.TE_RX_DEBUG
                existing_text = text_edit.toPlainText()

                # 줄 단위로 분리
                lines = existing_text.split('\n')

                # 100줄 초과 시 가장 오래된 줄 제거
                if len(lines) >= 100:
                    lines = lines[-99:]  # 최근 99줄만 유지

                # 새로운 줄 추가
                curr_datetime = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                lines.append(curr_datetime + " : " + line)

                # 텍스트 업데이트
                text_edit.setPlainText('\n'.join(lines).strip())
                text_edit.verticalScrollBar().setValue(text_edit.verticalScrollBar().maximum())  # 스크롤 아래로 이동
