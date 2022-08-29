import time, os
from badge import BMP, IOInterface, OLED, battery


OLED.Power(True)

#Load
print("Loading images")
imageCount = 0
dirs = os.listdir("images")
for file in dirs:
    bmp = BMP.bitmap("images/" + file)
    image = bmp.generate1bit_array()
    OLED.store_frame(image, 0)
    imageCount = imageCount + 1
 
#Show
print("Showing")
while True:
    for n in range(imageCount):
        OLED.show_frame(n-1)
        time.sleep(1)
