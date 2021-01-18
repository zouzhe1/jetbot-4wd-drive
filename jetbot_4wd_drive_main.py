#use DC motor by PCA9685 and A4950
#chip A4950 only need two pin,is in1 and in2
#jetbot offical use the pcb is adafruit DC Motor
#first ,install python lib https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library

import time
from Adafruit_MotorHAT.Adafruit_PWM_Servo_Driver import PWM
class LB_Motor:
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3
    RELEASE = 4
    def __init__(self,num,speed=0.0,addr = 0x60, freq = 1600, i2c=None, i2c_bus=1):
        self._frequency = freq
        self._pwm = PWM(addr, debug=False, i2c=i2c, i2c_bus=i2c_bus)
        self._pwm.setPWMFreq(self._frequency)

        self.motornum = num
        self.speed = speed
        in1 = in2 = 0
        #my jetson实际引脚已确定
        if (num == 0):
                 in1 = 0
                 in2 = 1
        elif (num == 1):
                 in1 = 2
                 in2 = 3
        elif (num == 2):
                 in1 = 4
                 in2 = 5
        elif (num == 3):
                 in1 = 6
                 in2 = 7
        else:
            raise NameError('MotorHAT Motor must be between 1 and 4 inclusive')
        self.IN1pin = in1
        self.IN2pin = in2

    def setPin(self, pin, value):
        if (pin < 0) or (pin > 15):
            raise NameError('PWM pin must be between 0 and 15 inclusive')
        if (value != 0) and (value != 1):
            raise NameError('Pin value must be 0 or 1!')
        if (value == 0):
            self._pwm.setPWM(pin, 0, 4096)
        if (value == 1):
            self._pwm.setPWM(pin, 4096, 0)

    def run(self, command):
        if (command == LB_Motor.FORWARD):
            self.setPin(self.IN1pin, 1)
            self._pwm.setPWM(self.IN2pin, 0, self.speed)
        if (command == LB_Motor.BACKWARD):
            self.setPin(self.IN2pin, 1)
            self._pwm.setPWM(self.IN1pin, self.speed, 0)
        if (command == LB_Motor.RELEASE):
            self.setPin(self.IN1pin, 0)
            self.setPin(self.IN2pin, 0)
    def setSpeed(self, speed256):
        if (speed256 < 0):
            self.speed = 0
        if (speed256 > 255):
            self.speed = 255
        self.speed=speed256
        
class play:
    def __init__(self, arg=None):
        self.arg = arg
        self.motor=[ LB_Motor(m,i2c_bus=1) for m in range(4) ]
    def forward(self,speed):
        for i in range(4):
            self.motor[i].setSpeed(speed)
        for i in range(4):
            self.motor[i].run(self.motor[i].FORWARD)
    def backward(self,speed):
        for i in range(4):
            self.motor[i].setSpeed(speed)
        for i in range(4):
            self.motor[i].run(self.motor[i].BACKWARD)
    def stop(self):
        for i in range(4):
            self.motor[i].setSpeed(0)
        for i in range(4):
            self.motor[i].run(self.motor[i].RELEASE)
