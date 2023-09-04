# -*- coding:utf-8 -*-
#!/usr/bin/python
#Author: Dharmendra Kumar Yadav
#######################################################


import math
import RPi.GPIO as GPIO
import spidev
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)
 
# Define sensor channels (3 to 7 are unused)
mcp3008_switch_channel = 0
mcp3008_x_voltage_channel = 1
mcp3008_y_voltage_channel = 2
 
# Define RGB channels
red_led = 36
green_led = 31
blue_led = 37
 
 
def read_spi_data_channel(channel):
    """
    Read in SPI data from the channel and return a coordinate position
    :param channel: integer, between 0-7
    :return: integer, between 0-1023 indicating joystick position
    """
 
    adc = spi.xfer2([1, (8+channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]
 
 
def convert_coordinates_to_angle(x, y, center_x_pos, center_y_pos):
    """
    Convert an x,y coordinate pair representing joystick position,
    and convert it to an angle relative to the joystick center (resting) position
    :param x: integer, between 0-1023 indicating position on x-axis
    :param y: integer, between 0-1023 indicating position on y-axis
    :param center_x_pos: integer, indicating resting position of joystick along x-axis
    :param center_y_pos: integer, indicating resting position of joystick along y-axis
    :return: integer, between 0-359 indicating angle in degrees
    """
 
    dx = x - center_x_pos
    dy = y - center_y_pos
    rads = math.atan2(-dy, dx)
    rads %= 2 * math.pi
    return math.degrees(rads)
 
 
def adjust_angle_for_perspective_of_current_led(angle, led):
    """
    Take the current LED into account, and rotate the coordinate plane 360 deg to make PWM calculations easier
    :param angle: integer, between 0-359 indicating current angle of joystick position
    :param led: 'R', 'G', 'B', indicating the LED we're interested in
    :return: integer, between 0-359 indicating new angle relative to the current LED under consideration
    """
 
    led_peak_angle = 90 if led == 'R' else (210 if led == 'B' else 330)
    return ((angle - led_peak_angle) + 360) % 360
 
 
def calculate_next_pwm_duty_cycle_for_led(angle, led):
    """
    Calculate the next PWM duty cycle value for the current LED and joystick position (angle)
    :param angle: integer, between 0-359 indicating current angle of joystick position
    :param led: 'R', 'G', 'B', indicating the LED we're interested in
    :return: integer, between 0-100 indicating the next PWM duty cycle value for the LED
    """
 
    angle = adjust_angle_for_perspective_of_current_led(angle, led)
    if 120 < angle < 240:
        return 0
    elif angle <= 120:
        return 100 - (angle * (100 / 120.0))
    else:
        return 100 - ((360 - angle) * (100 / 120.0))
 
 
def is_joystick_near_center(x, y, center_x_pos, center_y_pos):
    """
    Compare the current joystick position to resting position and decide if it's close enough to be considered "center"
    :param x: integer, between 0-1023 indicating position on x-axis
    :param y: integer, between 0-1023 indicating position on y-axis
    :param center_x_pos: integer, indicating resting position of joystick along x-axis
    :param center_y_pos: integer, indicating resting position of joystick along y-axis
    :return: boolean, indicating whether or not the joystick is near the center (resting) position
    """
 
    dx = math.fabs(x - center_x_pos)
    dy = math.fabs(y - center_y_pos)
    return dx < 20 and dy < 20
 
 
def main():
    """
    Initializes GPIO and PWM, then sets up a loop to continually read the joystick position and calculate the next set
    of PWM value for the RGB LED. When user hits ctrl^c, everything is cleaned up (see 'finally' block)
    :return: None
    """
 
    # Center positions when joystick is at rest
    center_x_pos = 530
    center_y_pos = 504
 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([red_led, green_led, blue_led], GPIO.OUT, initial=GPIO.LOW)
 
    pwm_r = GPIO.PWM(red_led, 300)
    pwm_g = GPIO.PWM(green_led, 300)
    pwm_b = GPIO.PWM(blue_led, 300)
 
    pwm_instances = [pwm_r, pwm_g, pwm_b]
 
    for p in pwm_instances:
        p.start(0)
 
    try:
        while True:
            # If joystick switch is pressed down, turn off LEDs
            switch = read_spi_data_channel(mcp3008_switch_channel)
            if switch == 0:
                for p in pwm_instances:
                    p.ChangeDutyCycle(0)
                continue
 
            # Read the joystick position data
            x_pos = read_spi_data_channel(mcp3008_x_voltage_channel)
            y_pos = read_spi_data_channel(mcp3008_y_voltage_channel)
 
            # If joystick is at rest in center, turn on all LEDs at max
            if is_joystick_near_center(x_pos, y_pos, center_x_pos, center_y_pos):
                for p in pwm_instances:
                    p.ChangeDutyCycle(100)
                continue
 
            # Adjust duty cycle of LEDs based on joystick position
            angle = convert_coordinates_to_angle(x_pos, y_pos, center_x_pos, center_y_pos)
            pwm_r.ChangeDutyCycle(calculate_next_pwm_duty_cycle_for_led(angle, 'R'))
            pwm_g.ChangeDutyCycle(calculate_next_pwm_duty_cycle_for_led(angle, 'G'))
            pwm_b.ChangeDutyCycle(calculate_next_pwm_duty_cycle_for_led(angle, 'B'))
 
            # print("Position : ({},{})  --  Angle : {}".format(x_pos, y_pos, round(angle, 2)))
 
    except KeyboardInterrupt:
        pass
 
    finally:
        for p in pwm_instances:
            p.stop()
        spi.close()
        GPIO.cleanup()
 
 
if __name__ == '__main__':
    main()
