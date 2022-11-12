# main.py -- put your code here!

from lib.OLED import driver
import time

while True:
    start = time.ticks_us()

    driver.fill(0)
    driver.text("owo", (128 - 5) // 2 , 12)
    driver.show()

    time_passed = time.ticks_us() - start

    print(f"{1000000 / time_passed:.2f} fps")

    time.sleep(0.5)
