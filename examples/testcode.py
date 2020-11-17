#Stack Light v1.0p test code

from machine import Pin
from pyb import CAN, ADC
import utime


print("starting stack light board test")
print("v1.0")
print("initializing")
can = CAN(1, CAN.NORMAL)
can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))


#Setup Pins
hbt_led = Pin("D5", Pin.OUT)
func_butt = Pin("E7", Pin.IN, Pin.PULL_UP)
can_wakeup = Pin("D6", Pin.OUT)
can_wakeup.value(0) 

BUZZER = Pin("D12", Pin.OUT)
WHITE = Pin("D11", Pin.OUT)
BLUE = Pin("E13", Pin.OUT)
GREEN = Pin("E12", Pin.OUT)
YELLOW = Pin("E11", Pin.OUT)
RED = Pin("E10", Pin.OUT)
    
    
#Setup hbt timer
hbt_state = 0
hbt_interval = 500
start = utime.ticks_ms()
next_hbt = utime.ticks_add(start, hbt_interval)
hbt_led.value(hbt_state)


print("starting")


def chk_hbt():
    global next_hbt
    global hbt_state
    now = utime.ticks_ms()
    if utime.ticks_diff(next_hbt, now) <= 0:
        if hbt_state == 1:
            hbt_state = 0
            hbt_led.value(hbt_state)
            #print("hbt")
        else:
            hbt_state = 1
            hbt_led.value(hbt_state)  
        
        next_hbt = utime.ticks_add(next_hbt, hbt_interval)

      

def send():
    can.send('message!', 123)   # send a message with id 123
    
def get():
    mess = can.recv(0)
    print(mess)
    cycle_stack()
        
def cycle_stack():
    RED.value(1)
    utime.sleep_ms(500)
    RED.value(0)
    YELLOW.value(1)
    utime.sleep_ms(500)
    YELLOW.value(0)
    GREEN.value(1)
    utime.sleep_ms(500)
    GREEN.value(0)
    BLUE.value(1)
    utime.sleep_ms(500)
    BLUE.value(0)
    WHITE.value(1)
    utime.sleep_ms(500)
    WHITE.value(0)
    BUZZER.value(1)
    utime.sleep_ms(75)
    BUZZER.value(0)
      
while True:
    chk_hbt()
    if not (func_butt.value()):
        print("function button")
        cycle_stack()
        send()
        utime.sleep_ms(200)

    if(can.any(0)):
        get()
        