# quick workaround to import grandparent-directory
import sys
sys.path.append("...")
import global_vars
import config as cfg
#import gpiozero as gpio

def alert(event):
    #buzzer = gpio.DigitalOutputDevice(7, active_high=False) #GPIO4
    while True:
        event.wait()
        for i in range(0,4):
            #buzzer.on()
            print("buzzing...")
            sleep(0.5)#sleep(cfg.alert_interval)
            #buzzer.off()
        event.clear()
