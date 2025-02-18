# main.py: Game selection menu by Vincent Mistler (YouMakeTech)
from machine import Pin, PWM, I2C, Timer
from ssd1306 import SSD1306_I2C
import time
import random

if __name__ == "__main__":
    # size of the screen
    SCREEN_WIDTH=128                       
    SCREEN_HEIGHT=64
    
    # list of games
    GAMELIST=["Pong","Snake","Space Invaders"]

    # Buttons connected to GP2 to GP7
    up = Pin(2, Pin.IN, Pin.PULL_UP)
    down = Pin(3, Pin.IN, Pin.PULL_UP)
    left = Pin(4, Pin.IN, Pin.PULL_UP)
    right = Pin(5, Pin.IN, Pin.PULL_UP)
    button1 = Pin(6, Pin.IN, Pin.PULL_UP)
    button2 = Pin(7, Pin.IN, Pin.PULL_UP)
    button_start = Pin(9, Pin.IN, Pin.PULL_UP)
    button_select = Pin(8, Pin.IN, Pin.PULL_UP)
    
    # Buzzer connected to GP10
    buzzer = PWM(Pin(10))
    
    # OLED Screen connected to GP0 (SDA) and GP1 (SCL)
    i2c = machine.I2C(0, sda = Pin(0), scl = Pin(1), freq = 400000)
    oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

    current = 0
    game_selected = -1

    while True:
        oled.fill(0)
        for row in range(0, len(GAMELIST)):
            if row == current:
                oled.fill_rect(0, row*8, SCREEN_WIDTH, 7, 1)
                color = 0
            else:
                color = 1
            
            oled.text(GAMELIST[row], int(SCREEN_WIDTH/2)-int(len(GAMELIST[row])/2 * 8), row*8,color)
        
        oled.show()
        
        time.sleep(0.2)
        
        buttonPressed = False
        
        while not buttonPressed:
            if (down.value() == 0 or right.value() == 0) and current < len(GAMELIST) - 1:
                current += 1
                buttonPressed = True
            elif (up.value() == 0 or left.value() == 0) and current > 0:
                current -= 1
                buttonPressed = True
            elif button1.value()==0 or button2.value()==0 or button_start.value()==0:
                buttonPressed = True
                game_selected = current

        # Make a sound
        buzzer.freq(1000)
        buzzer.duty_u16(2000)
        time.sleep(0.100)
        buzzer.duty_u16(0)
        
        # Start the selected game
        if game_selected >= 0:
            oled.fill(0)
            oled.show()
            
            if game_selected==0:
                from PicoPong import *
                pico_pong_main()
            elif game_selected==1:
                from PicoSnake import *
                pico_snake_main()
            elif game_selected==2:
                from PicoInvaders import *
                pico_invaders_main()
                
        game_selected=-1
