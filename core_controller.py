from handler_ui import HandlerUI
from handler_serial import HandlerSerial
from handler_plot import HandlerPlot
from handler_command import HandlerCommand

class CoreController:
    def __init__(self):
        # UI 초기화
        self.ui = HandlerUI()
        
        # 핸들러 초기화
        self.serial_handler     = HandlerSerial(self)

        # self.plot_handler_cur_r = HandlerPlot(self.ui.plot_cur_r, "Roll",  "deg") // ref from JNG
        self.plot_handler_tc1 = HandlerPlot(self.ui.plot_tc1, "tc_1", None, 1000)
        self.plot_handler_tc2 = HandlerPlot(self.ui.plot_tc2, "tc_2", None, 1000)
        self.plot_handler_tc3 = HandlerPlot(self.ui.plot_tc3, "tc_3", None, 1000)
        self.plot_handler_pt1 = HandlerPlot(self.ui.plot_pt1, "pt_1", None, 1000)
        self.plot_handler_pt2 = HandlerPlot(self.ui.plot_pt2, "pt_2", None, 1000)
        # self.plot_handler_pt3 = HandlerPlot(self.ui.plot_pt3, "pt_3", None, 200)
        self.plot_handler_lc1 = HandlerPlot(self.ui.plot_lc1, "lc_1", None, 1000)
        
        self.command_handler    = HandlerCommand(self.serial_handler)

        # UI에 핸들러 연결
        self.ui.set_serial_handler(self.serial_handler)
        self.ui.set_plot_handler(self.plot_handler_tc1)
        self.ui.set_plot_handler(self.plot_handler_tc2)
        self.ui.set_plot_handler(self.plot_handler_tc3)
        self.ui.set_plot_handler(self.plot_handler_pt1)
        self.ui.set_plot_handler(self.plot_handler_pt2)
        # self.ui.set_plot_handler(self.plot_handler_pt3)
        self.ui.set_plot_handler(self.plot_handler_lc1)
        self.ui.set_command_handler(self.command_handler)

    def start(self):
        # UI 실행
        self.ui.show()
