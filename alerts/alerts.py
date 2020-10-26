# quick workaround to import grandparent-directory
import sys
sys.path.append("...")
import global_vars
import config as cfg
import gpiozero as gpio
from time import sleep

def alert(event):
    buzzer = gpio.DigitalOutputDevice("GPIO4", active_high=False)
    while True:
        event.wait()
        for i in range(0,4):
            buzzer.on()
            #print("buzzing...")#debug
            sleep(0.2)#sleep(cfg.alert_interval)
            buzzer.off()
            sleep(0.2)

        event.clear()
