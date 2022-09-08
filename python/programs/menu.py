print("MENU")

    
import time, os, traceback, sys
from badge import battery, OLED, error
from badge import IOInterface as IO
#Text = 6X 7Y


def drawControls():
    #Controls
    OLED.driver.text("UP",0,0,255)
    OLED.driver.text("DWN",0,24,255)
    #List
    OLED.driver.line(18,0,18,32,1)
    
def drawList(scroll, programs):
    for i in range(4):
        name = program_list[(scroll+i)%(len(program_list)-1)]
        OLED.driver.text(name,18,i*7,255)
        

def up():
    if not IO.joystick_LU.value or not IO.joystick_RU.value:
        return True
    else:
        return False

def down():
    if not IO.joystick_LD.value or not IO.joystick_RD.value:
        return True
    else:
        return False
    
def pressed():
    if not IO.joystick_P.value:
        return True
    else:
        return False


#Load programs
program_list = os.listdir("programs")

#Init list
OLED.driver.fill(0)
drawControls()
drawList(0,program_list)
OLED.driver.show()

#Explorer loop
joystick_changed = False
joystick_down = False
test = 0
cursor = 0
scroll = 0
while True:
    
    if pressed():
        if joystick_down == False:
            joystick_down = True
            #When pressed run once
            
            #Find selected file
            print(" ")
            print((cursor+scroll)%len(program_list))
            selected = program_list[(cursor+scroll)%(len(program_list)-1)]
            
            #Run it
            time.sleep(1) 
            exec(open("programs/"+selected).read())
            
            #When program left, redraw everything
            OLED.driver.fill(0)
            drawControls()              
            drawList(scroll,program_list)  
            OLED.driver.show()
            
    else:
        joystick_down = False
    
    if down() or up():
        if joystick_changed == False:
            joystick_changed = True
            #Joystick has changed. Run once
            
            #Draw controls
            OLED.driver.fill(0)
            drawControls()  
  
            #Change cursor
            if down():
                if cursor < 3:
                    cursor = cursor + 1
                else:
                    scroll = scroll + 1
            else:
                if cursor > 0:
                    cursor = cursor - 1
                else:
                    scroll = scroll - 1
            
            #Arrow
            OLED.driver.line(128-10,(cursor*7)+4,128,cursor*7,255)
            OLED.driver.line(128-10,(cursor*7)+5,128,(cursor*7)+8,255)
            
            drawList(scroll,program_list)   
            
            OLED.driver.show()
            
    else:
        joystick_changed = False
        
    time.sleep(0.0001)
        

