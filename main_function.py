from PyQt5.QtCore   import QTimer
from PyQt5.QtWidgets import *

import time
from multiprocessing import Process
import threading
import cv2
import numpy as np
import base64

from db import DB_function
from Socket import Socket_function

class main_function(QWidget):
    def __init__(self, ui):
        super().__init__()

        self.ui = ui

        self.db = DB_function()
        self.sock = Socket_function()

        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.time_bar_timeout)

        self.set_ui()
        self.btn_event()

        # value setting
        self.local_ip = None
        self.server_ip = None
        self.frame_number_set = None
        self.connect_time = None
        self.lane_num = None
        self.collect_cycle = None
        self.category_num = None
        self.value_setting()

    def value_setting(self):
        self.local_ip = '123.456.789.123'
        # self.server_ip = '127.000.000.001'
        self.server_ip = '192.168.0.7'
        self.lane_num = 2
        self.collect_cycle = 30
        self.category_num = 10

    def time_bar_timeout(self):
        now = time.localtime()
        self.ui.time_bar.setText(str("%04d/%02d/%02d %02d:%02d:%02d" %
                                     (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)))

    def set_ui(self):
        # socket
        self.ui.sock_ip_input.setText("127.0.0.1")
        self.ui.sock_port_input.setText("30100")

        self.ui.op_FF_btn.setEnabled(False)
        self.ui.op_FE_btn.setEnabled(False)
        self.ui.op_01_btn.setEnabled(False)
        self.ui.op_04_btn.setEnabled(False)
        self.ui.op_05_btn.setEnabled(False)
        self.ui.op_07_btn.setEnabled(False)
        self.ui.op_0C_btn.setEnabled(False)
        self.ui.op_0D_btn.setEnabled(False)
        self.ui.op_0D_btn.setEnabled(False)
        self.ui.op_0E_btn.setEnabled(False)
        self.ui.op_0F_btn.setEnabled(False)
        self.ui.op_11_btn.setEnabled(False)
        self.ui.op_12_btn.setEnabled(False)
        self.ui.op_13_btn.setEnabled(False)
        self.ui.op_15_btn.setEnabled(False)
        self.ui.op_16_btn.setEnabled(False)
        self.ui.op_17_btn.setEnabled(False)
        self.ui.op_18_btn.setEnabled(False)
        self.ui.op_19_btn.setEnabled(False)
        self.ui.op_1E_btn.setEnabled(False)

    def btn_event(self):
        self.ui.socket_connect_btn.clicked.connect(self.socket_connect_btn_click)
        self.ui.db_connect_btn.clicked.connect(self.db_connect_btn_click)

        # region request btn event
        self.ui.op_FF_btn.clicked.connect(self.op_FF_btn_click)
        self.ui.op_FE_btn.clicked.connect(self.op_FE_btn_click)
        self.ui.op_01_btn.clicked.connect(self.op_01_btn_click)
        self.ui.op_04_btn.clicked.connect(self.op_04_btn_click)
        self.ui.op_05_btn.clicked.connect(self.op_05_btn_click)
        self.ui.op_07_btn.clicked.connect(self.op_07_btn_click)
        self.ui.op_0C_btn.clicked.connect(self.op_0C_btn_click)
        self.ui.op_0D_btn.clicked.connect(self.op_0D_btn_click)
        self.ui.op_0E_btn.clicked.connect(self.op_0E_btn_click)
        self.ui.op_0F_btn.clicked.connect(self.op_0F_btn_click)
        self.ui.op_11_btn.clicked.connect(self.op_11_btn_click)
        self.ui.op_12_btn.clicked.connect(self.op_12_btn_click)
        self.ui.op_13_btn.clicked.connect(self.op_13_btn_click)
        self.ui.op_15_btn.clicked.connect(self.op_15_btn_click)
        self.ui.op_16_btn.clicked.connect(self.op_16_btn_click)
        self.ui.op_17_btn.clicked.connect(self.op_17_btn_click)
        self.ui.op_18_btn.clicked.connect(self.op_18_btn_click)
        self.ui.op_19_btn.clicked.connect(self.op_19_btn_click)
        self.ui.op_1E_btn.clicked.connect(self.op_1E_btn_click)
        # test
        self.ui.test_btn.clicked.connect(self.test_btn_click)
        # endregion


    def test_btn_click(self):
        self.sock.socket_close()

    # region btn click function
    def socket_connect_btn_click(self):
        sock_ip = self.ui.sock_ip_input.text()
        sock_port = int(self.ui.sock_port_input.text())

        if sock_ip == '' or sock_port == '':
            self.ui.status_bar.setText("Socket IP, PORT를 입력해주세요!")
        else:
            self.ui.status_bar.setText("Socket server 연결중...")
            try:
                self.sock.socket_connect(sock_ip, sock_port)
            except Exception as e:
                self.ui.status_bar.setText("err socket connect: ", e)
            self.ui.status_bar.setText("Socket server '" + sock_ip + "', '" + str(sock_port) + "' connect !")

            # region test btn true
            self.ui.op_FF_btn.setEnabled(True)
            self.ui.op_FE_btn.setEnabled(False)
            self.ui.op_01_btn.setEnabled(True)
            self.ui.op_04_btn.setEnabled(True)
            self.ui.op_05_btn.setEnabled(True)
            self.ui.op_07_btn.setEnabled(True)
            self.ui.op_0C_btn.setEnabled(True)
            self.ui.op_0D_btn.setEnabled(True)
            self.ui.op_0D_btn.setEnabled(True)
            self.ui.op_0E_btn.setEnabled(True)
            self.ui.op_0F_btn.setEnabled(True)
            self.ui.op_11_btn.setEnabled(True)
            self.ui.op_12_btn.setEnabled(True)
            self.ui.op_13_btn.setEnabled(True)
            self.ui.op_15_btn.setEnabled(True)
            self.ui.op_16_btn.setEnabled(True)
            self.ui.op_17_btn.setEnabled(True)
            self.ui.op_18_btn.setEnabled(True)
            self.ui.op_19_btn.setEnabled(False)
            self.ui.op_1E_btn.setEnabled(True)
            # endregion

            # read 스레드 시작 while
            t = threading.Thread(target=self.read_socket_msg, args=(), daemon=True)
            t.start()
            # read_socket = Process(target=self.read_socket_msg, args=())
            # read_socket.start()

    def db_connect_btn_click(self):
        print("db..")
        self.db.test()

    # endregion

    # region socket_msg

    def read_socket_msg(self):
        while 1:
            recv_msg = self.sock.socket_read()
            if recv_msg == '':
                break
            else:
                self.parsing_msg(recv_msg)

    def parsing_msg(self, recv_msg):
        d_recv_msg = recv_msg.decode('utf-16')

        # for i in range(len(d_recv_msg)):
        #     print(i, "   ", d_recv_msg[i])
        # print(msg_op)
        if len(d_recv_msg) > 40:
            print("[msg len] : " + str(len(d_recv_msg)))
            # print("recv_msg: ", end=' ')
            # for data in d_recv_msg:
            #     print(hex(ord(data)), end='/')
            # print('')
            msg_op = d_recv_msg[43]
            sender_ip = d_recv_msg[0:15]
            destination_ip = d_recv_msg[16:31]
            self.server_ip = sender_ip

            # 수신메시지의 목적지IP == local IP
            if destination_ip == self.local_ip:
                # print("RX_msg: /", recv_msg.decode('utf-16'), "/")
                if msg_op == chr(0xFF):
                    # self.sock.send_FF_res_msg(self.local_ip, sender_ip)
                    # self.connect_time = time.time()
                    print('0xFF response')
                elif msg_op == chr(0xFE):
                    print("FE")
                    self.sock.send_FE_msg(self.local_ip, sender_ip)
                elif msg_op == chr(0x01):
                    # self.device_sync(msg_op, d_recv_msg)
                    # self.sock.send_01_res_msg(self.local_ip, sender_ip)
                    print("0x01 ")
                elif msg_op == chr(0x04):
                    # self.sock.send_04_res_msg(self.local_ip, sender_ip, self.frame_number_set)
                    print('0x04 response')
                elif msg_op == chr(0x05):
                    # self.sock.send_05_res_msg(self.local_ip, sender_ip)
                    print('0x05 response')
                elif msg_op == chr(0x07):
                    # self.sock.send_07_res_msg(self.local_ip, sender_ip)
                    print('0x07 response')
                elif msg_op == chr(0x0C):
                    # self.device_sync(msg_op, d_recv_msg)
                    # self.sock.send_0C_res_msg(self.local_ip, sender_ip)
                    print('0x0C response')
                elif msg_op == chr(0x0D):
                    # self.sock.send_0D_res_msg(self.local_ip, sender_ip)
                    print('0x0D response')
                elif msg_op == chr(0x0E):
                    # self.sock.send_0E_res_msg(self.local_ip, sender_ip)
                    print('0x0E response')
                elif msg_op == chr(0x0F):
                    # index = int(ord(d_recv_msg[44]))
                    # self.sock.send_0F_res_msg(self.local_ip, sender_ip, index)
                    print('0x0F response')
                elif msg_op == chr(0x11):
                    # request_time = time.time()
                    # self.sock.send_11_res_msg(self.local_ip, sender_ip, self.connect_time, request_time)
                    print('0x11 response')
                elif msg_op == chr(0x13):
                    # self.sock.send_13_res_msg(self.local_ip, sender_ip, d_recv_msg)
                    print('0x13 response')
                elif msg_op == chr(0x15):
                    # self.sock.send_15_res_msg(self.local_ip, sender_ip)
                    print('0x15 response')
                elif msg_op == chr(0x16):
                    # self.sock.send_16_res_msg(self.local_ip, sender_ip)
                    print('0x16 response')
                elif msg_op == chr(0x17):
                    # self.sock.send_17_res_msg(self.local_ip, sender_ip)
                    sender_ip = d_recv_msg[0:15]
                    destination_ip = d_recv_msg[16:31]
                    controller = d_recv_msg[32:39]
                    total_length = (ord(d_recv_msg[39]) << 24) + (ord(d_recv_msg[40]) << 16) + (ord(d_recv_msg[41]) << 8) + ord(
                        d_recv_msg[42])
                    opcode = d_recv_msg[43]
                    if opcode == chr(0x17):
                        ack = d_recv_msg[44]
                        data_field = d_recv_msg[45:]
                        img_size = (ord(data_field[0]) << 24) + (ord(data_field[1]) << 16) + (ord(data_field[2]) << 8) + ord(data_field[3])
                        img_temp = data_field[4:]
                        img_data = img_temp + "=" * (4-len(img_temp) % 4)


                        data = np.frombuffer(base64.b64decode(img_data), np.uint8)
                        img = cv2.imdecode(data, 1)

                        self.server_ip = sender_ip

                        # print('sender', sender_ip, 'destination', destination_ip, 'controller', controller)
                        print('[total length] : ', total_length)
                        # print('opcode', opcode)
                        print('[img_size] : ', img_size)

                        cv2.imshow("image", img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                    print('0x17 response')
                elif msg_op == chr(0x18):
                    # self.sock.send_18_res_msg(self.local_ip, sender_ip)
                    print('0x18 response')
                elif msg_op == chr(0x19):
                    # self.sock.send_19_res_msg(self.local_ip, sender_ip)
                    print('0x19 response')
                elif msg_op == chr(0x1E):
                    # self.sock.send_1E_res_msg(self.local_ip, sender_ip)
                    print('0x1E response')
            else:
                print("TX_msg: /", recv_msg.decode('utf-16'), "/")
    # endregion

    def device_sync(self, op, msg):
        if op == chr(0x01):
            self.frame_number_set = msg[44]
        elif op == chr(0x0C):
            self.lane_num = 2
            self.collect_cycle = 30
            self.category_num = 10
            # 이외의 설정값 등 리셋



    # region test send msg
    def op_FF_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("FF btn_click")
        self.sock.send_FF_msg()

    def op_FE_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("FE btn_click")
        self.sock.send_FE_res_msg()

    def op_01_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("01 btn_click")
        self.sock.send_01_msg()

    def op_04_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("04 btn_click")
        self.sock.send_04_msg()

    def op_05_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("05 btn_click")
        self.sock.send_05_msg()

    def op_07_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("07 btn_click")
        self.sock.send_07_msg()

    def op_0C_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("0C btn_click")
        self.sock.send_0C_msg()

    def op_0D_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("0D btn_click")
        self.sock.send_0D_msg()

    def op_0E_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("0E btn_click")
        self.sock.send_0E_msg()

    def op_0F_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("0F btn_click")
        self.sock.send_0F_msg()

    def op_11_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("11 btn_click")
        self.sock.send_11_msg()

    def op_12_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("12 btn_click")
        # self.sock.send_12_msg()

    def op_13_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("13 btn_click")
        self.sock.send_13_msg()

    def op_15_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("15 btn_click")
        self.sock.send_15_msg()

    def op_16_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("16 btn_click")
        self.sock.send_16_msg()

    def op_17_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("17 btn_click")
        self.sock.send_17_msg()

    def op_18_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("18 btn_click")
        self.sock.send_18_msg()

    def op_19_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("19 btn_click")

    def op_1E_btn_click(self):
        print("---------------------------------------------------------------------------")
        print("1E btn_click")
        self.sock.send_1E_msg()

    # endregion