
import socket

import random

class Socket_function:
    def __init__(self):
        super().__init__()

        self.server_socket = None
        self.client_socket = None

    def socket_server_open(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()

    def socket_connect(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))
    def socket_close(self):
        self.client_socket.close()
    def socket_send_msg(self, send_msg):
        self.client_socket.send(send_msg.encode('utf-16'))
        print("TX_msg: /", send_msg, "/")
        # recv
        # recv_msg = self.client_socket.recv(1024)
        # d_recv_msg = recv_msg.decode()
        # print("recv: " + recv_msg.decode())
        # for i in range(len(recv_msg)):
        #     print("msg[i]: ", recv_msg[i])
        #
        # for i in range(len(recv_msg)):
        #     print("de_msg[i]: ", recv_msg[i])

    def socket_read(self):
        return self.client_socket.recv(3300000)

    # region msg response
    def send_FF_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0xFF)
        data = chr(0x06) # ack
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_FE_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0xFE)
        length = self.length_calc(1)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    # def send_01_res_msg(self, sender_ip, destination_ip):
    #     controller_kind = 'VD'
#     #     controller_number = '12345''
    #     length = '0002'
    #     point = chr(0x2D)
    #     opcode = chr(0xFE)
    #     data = chr(0x06) # ack
    #     send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
    #     self.socket_send_msg(send_msg)

    def send_04_res_msg(self, sender_ip, destination_ip, frame_number):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x04)
        frame_num = frame_number
        lane_err = '0000'
        lane_num = '2'
        lane_data = chr(0x0A) + chr(0x2B) + chr(0x09) + chr(0x2C)
        data = frame_num + lane_err + lane_num + lane_data
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_05_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x05)
        lane = '2' # 2차선
        lane_1 = [bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2),
                  bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2)]
        lane_2 = [bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2),
                  bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2)]
        for i in range(len(lane_1)):
            temp = lane_1[i]

            # num = random.randrange(0, 65535)
            num = random.randrange(0, 300)
            if num > 255:
                num_high = num >> 8
                num_low = num & 0xFF
                temp[0] = ord(chr(num_high))
                temp[1] = ord(chr(num_low))
            else:
                temp[1] = ord(chr(num))

        for i in range(len(lane_2)):
            temp = lane_2[i]

            # num = random.randrange(0, 65535)
            num = random.randrange(0, 300)
            if num > 255:
                num_high = num >> 8
                num_low = num & 0xFF
                temp[0] = ord(chr(num_high))
                temp[1] = ord(chr(num_low))
            else:
                temp[1] = ord(chr(num))

        data = lane
        for cg_data in lane_1:
            data = data + chr(cg_data[0])
            data = data + chr(cg_data[1])
        for cg_data in lane_2:
            data = data + chr(cg_data[0])
            data = data + chr(cg_data[1])

        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data

        self.socket_send_msg(send_msg)

        # for i in range(len(send_msg)):
        #     print(i, "   ", send_msg[i])

    def send_07_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x07)

        lane_1 = bytearray(2)
        lane_2 = bytearray(2)

        # num = random.randrange(0, 65535)
        num1 = random.randrange(0, 250)
        num1_high = num1 >> 8
        num1_low = num1 & 0xFF
        lane_1[0] = ord(chr(num1_high))
        lane_1[1] = ord(chr(num1_low))

        num2 = random.randrange(0, 300)
        num2_high = num2 >> 8
        num2_low = num2 & 0xFF
        lane_2[0] = ord(chr(num2_high))
        lane_2[1] = ord(chr(num2_low))

        data = chr(lane_1[0]) + chr(lane_1[1]) + chr(lane_2[0]) + chr(lane_2[1])
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0C_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x0C)
        data = chr(0x06) # ack
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0D_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '54321'
        point = chr(0x2D)
        opcode = chr(0x0D)
        data = chr(0x06) # ack
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0E_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x0E)
        data = chr(0x06) # ack
        length = self.length_calc(1 + len(data))
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0F_res_msg(self, sender_ip, destination_ip, index):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0x0F)
        print("index = ", index)
        data = ''
        if index == 1:
            # 차로 계산 (1 << 차로-1)
            byte_1 = chr(1 << (6 - 1))
            byte_2 = chr(0)
            data = byte_1 + byte_2
        elif index == 3:
            # 수집주기 기본 30, 변경값 60
            byte_1 = chr(30)
            data = byte_1
        elif index == 5:
            # 차량 속도 category 단위 기본 10
            byte_1 = chr(10)
            byte_2 = chr(10)
            byte_3 = chr(10)
            byte_4 = chr(10)
            byte_5 = chr(10)
            byte_6 = chr(10)
            byte_7 = chr(10)
            byte_8 = chr(10)
            byte_9 = chr(10)
            byte_10 = chr(10)
            byte_11 = chr(10)
            byte_12 = chr(10)
            data = byte_1 + byte_2 + byte_3 + byte_4 + byte_5 + byte_5 + byte_6 + \
                   byte_7 + byte_8 + byte_9 + byte_10 + byte_11 + byte_12
        elif index == 7:
            data = chr(index)
            # 속도별 누적치 계산 기본 1(사용)
            byte_1 = chr(1)
            data = data + byte_1
        elif index == 9:
            data = chr(index)
            # 속도 계산 가능 여부 기본 1(사용)
            byte_1 = chr(1)
            data = data + byte_1
        elif index == 21:
            data = chr(index)
            # 속도 계산 가능 여부 기본 0(사용안함)
            byte_1 = chr(0)
            data = data + byte_1

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_11_res_msg(self, sender_ip, destination_ip, connect_time, request_time):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x11)
        if connect_time != None and request_time != None:
            time_cha = int(request_time - connect_time)
            print("time_delay: ", str(time_cha))
            time_1 = time_cha & 0xFF
            time_2 = (time_cha >> 8) & 0xFF
            time_3 = (time_cha >> 16) & 0xFF
            time_4 = (time_cha >> 24) & 0xFF
            print(time_4, time_3, time_2, time_1)
            data = chr(time_3) + chr(time_3) + chr(time_2) + chr(time_1)
            length = self.length_calc(1 + len(data))

            send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
            self.socket_send_msg(send_msg)
        else:
            print("Please connect 0xFF")

    def send_13_res_msg(self, sender_ip, destination_ip, msg):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x13)
        data = msg[44:]
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_15_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x15)
        version = 1 << 4
        release = 1 & 0x0F
        version_num = chr(version + release)
        make_year = chr(random.randrange(0, 20))
        make_month = chr(random.randrange(1, 12))
        make_day = chr(random.randrange(1, 28))
        data = version_num + make_year + make_month + make_day
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    # 개별 차량 데이터 응답
    def send_16_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    # 정지 영상 응답
    def send_17_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    # RTC 변경 응답
    def send_18_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x18)
        data = chr(0x06)  # ack
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    # 돌발 상황 정보
    def send_19_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_1E_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    # endregion

    def send_FF_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = self.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0xFF)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_FE_msg(self, local_ip, sender_ip):
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)
        length = self.length_calc(1 + len(data))

        send_msg = local_ip + point + sender_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_01_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x01)
        data_frame = chr(120)
        length = self.length_calc(2)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data_frame
        self.socket_send_msg(send_msg)

    def send_04_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = self.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x04)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_05_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)

        length = self.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x05)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_07_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = self.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x07)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_0C_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = self.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x0C)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_0D_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x0D)
        length = self.length_calc(1)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_0E_msg(self):
        point = chr(0x2D)
        opcode = chr(0x0E)
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        # length = '0001'
        # index = 1 -> 차로지정
        # index = 3 -> 수집주기
        # index = 5 -> 차량 속도 구분
        # index = 7 -> 속도별 누적치 계산
        index_list = [1, 3, 5, 7, 9, 19]
        index = random.choice(index_list)

        index =1
        data = ''
        if index == 1:
            data = chr(index)
            # 차로 계산 (1 << 8-차로)
            byte_1 = chr(1 << (8-6))
            byte_2 = chr(0)
            # 차로 계산 (1 << 8-(차로-8))
            # byte_1 = chr(0)
            # byte_2 = chr(1 << (8 - (9-8)))
            data = data + byte_1 + byte_2
        elif index == 3:
            data = chr(index)
            # 수집주기 기본 30, 변경값 60
            byte_1 = chr(60)
            data = data + byte_1
        elif index == 5:
            data = chr(index)
            # 차량 속도 category 단위 기본 10
            byte_1 = chr(0)
            byte_2 = chr(11)
            byte_3 = chr(21)
            byte_4 = chr(31)
            byte_5 = chr(51)
            byte_6 = chr(61)
            byte_7 = chr(81)
            byte_8 = chr(91)
            byte_9 = chr(101)
            byte_10 = chr(121)
            byte_11 = chr(131)
            byte_12 = chr(141)
            data = data + byte_1 + byte_2 + byte_3 + byte_4 + byte_5 + byte_6 + \
                   byte_7 + byte_8 + byte_9 + byte_10 + byte_11 + byte_12
        elif index == 7:
            data = chr(index)
            # 속도별 누적치 계산 기본 1(사용)
            byte_1 = chr(0)
            data = data + byte_1
        elif index == 9:
            data = chr(index)
            # 속도 계산 가능 여부 기본 1(사용)
            byte_1 = chr(0)
            data = data + byte_1
        elif index == 19:
            data = chr(index)
            # 돌발 사용 여부  기본 0(사용안함)
            byte_1 = chr(1)
            data = data + byte_1

        length = self.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0F_msg(self):
        point = chr(0x2D)
        opcode = chr(0x0F)
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        index_list = [1, 3, 5, 7, 9, 21]
        index = chr(random.choice(index_list))
        length = self.length_calc(1 + len(index))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + index
        self.socket_send_msg(send_msg)

    def send_11_msg(self):
        point = chr(0x2D)
        opcode = chr(0x11)
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = self.length_calc(1)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_13_msg(self):
        point = chr(0x2D)
        opcode = chr(0x13)
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        echo_msg = 'qwelkjdasoiweoi2390weiodskl'
        length = self.length_calc(1 + len(echo_msg))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + echo_msg
        self.socket_send_msg(send_msg)

    def send_15_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = self.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x15)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_16_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = self.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x16)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_17_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        point = chr(0x2D)
        opcode = chr(0x17)
        # cam = chr(random.randrange(0, 3))
        cam = chr(0)
        length = self.length_calc(1)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_18_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = '0008'
        point = chr(0x2D)
        opcode = chr(0x18)
        # change_rtc_tune =

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_1E_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        # controller_number = '12345'
        controller_number = chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00)
        length = self.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x1E)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    # region other

    def length_calc(self, length):
        length_1 = length & 0xFF
        length_2 = (length >> 8) & 0xFF
        length_3 = (length >> 16) & 0xFF
        length_4 = (length >> 24) & 0xFF

        value = chr(length_4) + chr(length_3) + chr(length_2) + chr(length_1)

        return value

    # endregion
