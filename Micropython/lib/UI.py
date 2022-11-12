import IOInterface as IO
import time 
import OLED  
import os 


class FilePicker:   
    LINE_HEIGHT = 8
    MAX_LINES = 4

    def __init__(self):
        self.path = ""
        self.cursor = 0
        self.scroll = 0

    def draw_list(self):
        OLED.driver.fill(0) #Make sure everything is empty
        
        entries = os.ilistdir()
        
        #Skip entries we dont want to see. Scroll past it
        for s in range(self.scroll):
            next(entries)
        
        #Draw entries
        print("PICKER")
        line = 0
        for entry in entries:
            
            print(entry)
            
            #When cursor is on the line. Invert it
            color = int(self.cursor!=line)
         
            #Draw selection bar
            OLED.driver.fill_rect(0,FilePicker.LINE_HEIGHT * line, 128, FilePicker.LINE_HEIGHT, 1-color)         
            #Draw name
            OLED.driver.text(entry[0],0,FilePicker.LINE_HEIGHT * line, color)
            #Draw size
            OLED.driver.text(str(int(entry[3]/1000))+"kB",93,FilePicker.LINE_HEIGHT * line, color)
                       
            line = line + 1
            #Stop drawing when max lines is reached
            if line >= self.MAX_LINES:
                print("---SCREEN_END---")
                print(self.cursor + self.scroll)
                OLED.driver.show()
                break
        else: #NO_BREAK. No more entries. 
            print("---DIRECTORY_END---")
            print(self.cursor + self.scroll)
            OLED.driver.show()
                

    def open(self, path, cancellable=False):
        
        #Change directory
        os.chdir(path)
        self.draw_list()
        
        #Logic
        DB = DButton(200)
        while True:
            time.sleep(1/10000)
            
            #Press up
            if DB.up():
                if self.cursor > 0:
                    self.cursor = self.cursor -1
                else:
                    self.scroll = self.scroll -1
                self.draw_list()
            
            #Press down
            if DB.down():
                if self.cursor < FilePicker.MAX_LINES-1:
                    self.cursor = self.cursor +1
                else:
                    if self.scroll < FilePicker.MAX_LINES:
                        self.scroll = self.scroll +1
                self.draw_list()
                
            if DB.press():
                print("PRESSED & Return")
                index = self.cursor + self.scroll
                newpath = os.listdir()[index]
                print(index)
                print(newpath)
                return newpath
            
    

class SmoothCursor:
    """This is a very smooth moving cursor.
    You can use update() to change it's position based on IO joystick and draw it on the screen.
    get_postion() to get it's current position
    """

    def __init__(self):
        self.X: float = 0
        self.Y: float = 0
        self.VX: float = 0
        self.VY: float = 0

    def update(self):
        OLED.driver.fill(0)

        NX,NY = IO.Joystick.getDirection()
        
        self.VX = self.VX + NX / 10
        self.VY = self.VY + NY / 10

        self.VX = self.VX - self.VX * 0.1
        self.VY = self.VY - self.VY * 0.1

        self.X = self.X + self.VX / 1
        self.Y = self.Y + self.VY / 1

        OLED.driver.line(int(self.X),int(self.Y),int(self.X-self.VX*5),int(self.Y-self.VY*5),1)
        OLED.driver.show()    

    def get_position(self):
        return self.X,self.Y

class DButton:
    debounce_delay: float

    up_last_pressed: float = 0
    down_last_pressed: float = 0
    left_last_pressed: float = 0
    right_last_pressed: float = 0
    press_last_pressed: float = 0

    def __init__(self, debounce_delay = 200):
        """Initialize the DBUtton class.
        Keyword arguments:
        debounce_delay -- the button debounce delay in milliseconds (default 200)
        """

        self.debounce_delay = debounce_delay 

    def up(self) -> bool:
        """Return whether the up button is pressed."""
        if self.up_last_pressed < time.ticks_ms() - self.debounce_delay:
            self.up_last_pressed = time.ticks_ms()
            return not IO.Joystick.LU.value() or not IO.Joystick.RU.value()

        return False

    def down(self) -> bool:
        """Return whether the down button is pressed."""
        if self.down_last_pressed < time.ticks_ms() - self.debounce_delay:
            self.down_last_pressed = time.ticks_ms()
            return not IO.Joystick.LD.value() or not IO.Joystick.RD.value()

        return False

    def left(self) -> bool:
        """Return whether the left button is pressed."""
        if self.left_last_pressed < time.ticks_ms() - self.debounce_delay:
            self.left_last_pressed = time.ticks_ms()
            return not IO.Joystick.LU.value() or not IO.Joystick.LD.value()

        return False

    def right(self) -> bool:
        """Return whether the right button is pressed."""
        if self.right_last_pressed < time.ticks_ms() - self.debounce_delay:
            self.right_last_pressed = time.ticks_ms()
            return not IO.Joystick.RU.value() or not IO.Joystick.RD.value()

        return False

    def press(self) -> bool:
        """Return whether the button is pressed."""
        if self.press_last_pressed < time.ticks_ms()- self.debounce_delay:
            self.press_last_pressed = time.ticks_ms()
            return not IO.Joystick.P.value()

        return False


