import time
import utime
import machine
import onewire
import ds18x20
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
#from numpy import mean

sensor_ds_pin = machine.Pin(22)

LCD_I2C_ADDR     = 39
LCD_I2C_NUM_ROWS = 4
LCD_I2C_NUM_COLS = 20

lcdi2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(lcdi2c, LCD_I2C_ADDR, LCD_I2C_NUM_ROWS, LCD_I2C_NUM_COLS)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(sensor_ds_pin))
roms = ds_sensor.scan()

def startscreen():    
    lcd.clear()
    lcd.move_to(0,1)
    lcd.putstr("KF Soil Temperature")
    lcd.move_to(0,2)
    lcd.putstr("Probe")
    utime.sleep(2)
    lcd.clear()

def measure_temp(ds_sensor, rom):
  ds_sensor.convert_temp()
  #time.sleep_ms(750)
  return ds_sensor.read_temp(rom)

def show_temp():
    temp = []
    clearcount = 0
    while True:
      for rom in roms:
        if clearcount==5:
            lcd.clear()
            clearcount=0
        lcd.move_to(0,0)
        temp.append(measure_temp(ds_sensor, rom))
        #lcd.putstr(f"{measure_temp(ds_sensor, rom):.1f} C")
        lcd.putstr(f"{temp[-1]:.1f} C")
        if len(temp)==11:
            temp = temp[1:]
            tsum = 0
            for t in temp:
                tsum = tsum + t
            lcd.move_to(0,2)
            lcd.putstr(f"10s avg: {tsum/10:.1f} C")
        clearcount = clearcount + 1
        print(clearcount)
        time.sleep(1)

startscreen()
show_temp()