
import serial

class BServo(object):

    def __init__(self, port, board_id, servo_nr, lowvalue=45, highvalue=135, range=90, us_step=0.1, us_mid=1.5):
        self.board_id   = board_id  # id of the servo board
        self.servo_nr   = servo_nr  # servo channel on board
        self.lowvalue   = lowvalue  # low value of movement
        self.highvalue  = highvalue # high value of movement
        self.range      = range     # degree range of movement
        #self.inverted   = inverted  # if true, movenent is inverted
        self.us_step    = us_step   # microseconds for 1 degree
        self.us_mid     = us_mid    # microseconds for 90 degree

        self.servo_id = self.board_id << 4 | self.servo_nr

        self.serial = serial.Serial(port)

        if board_id < 0 or board_id > 15: raise ValueError("wrong board id")

    def angle(self, value):
        """
        calculates the servo angle according to the blender scene value.
        :param value:
        :return:
        """
        valuerange = self.highvalue - self.lowvalue
        lowangle = 90 - 1.*self.range/2.
        highangle = 90 + 1.*self.range/2.
        m = 1.*(highangle-lowangle)/valuerange
        q = highangle - m*self.highvalue
        return m * value + q

    def turnValue(self, value):
        self.turnAngle(self.angle(value=value))

    def turnAngle(self, angle):
        min_angle = 90. - 1.*self.range/2.
        max_angle = 90. + 1.*self.range/2.
        if angle < min_angle:
            angle = min_angle
        elif angle > max_angle:
            angle = max_angle
        self.serial.write(('S' + chr(self.servo_id) + chr(int(angle))).encode('latin_1'))

    def toDefaultPosition(self):
        self.turnAngle(90)