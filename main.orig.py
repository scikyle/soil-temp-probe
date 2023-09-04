import time
import utime
import machine
import onewire
import ds18x20
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

sensor_ds_pin = machine.Pin(22)

LCD_I2C_ADDR     = 39
LCD_I2C_NUM_ROWS = 4
LCD_I2C_NUM_COLS = 20

lcdi2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(lcdi2c, LCD_I2C_ADDR, LCD_I2C_NUM_ROWS, LCD_I2C_NUM_COLS)

def startscreen():    
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("KF Soil Temperature")
    lcd.move_to(0,1)
    lcd.putstr("Probe")
    utime.sleep(2)
    lcd.clear()

ds_sensor = ds18x20.DS18X20(onewire.OneWire(sensor_ds_pin))
roms = ds_sensor.scan()

def show_temp():
    while True:
      ds_sensor.convert_temp()
      time.sleep_ms(750)
      for rom in roms:
        #print(rom)
        #print(ds_sensor.read_temp(rom))
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr(f"{ds_sensor.read_temp(rom):.1f} C")
      time.sleep(1)

startscreen()
show_temp()