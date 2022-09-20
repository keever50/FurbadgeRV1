#OPTIONS
dev = True
#dev=False when you want to load files safely and partially report crashes.
#dev=True when you want everything to halt and have a fully detailed traceback crash report to serial.

PROGRAMS_DIRECTORY = "/programs"

SCREEN_HEIGHT = 32
TEXT_HEIGHT = 7
LINE_HEIGHT = TEXT_HEIGHT + 1
LINE_COUNT = SCREEN_HEIGHT // LINE_HEIGHT

import time, os
from badge import battery, OLED
from badge import IOInterface as IO
from badge.tools import run

class DButton:
    # Button debounce delay in seconds
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

        self.debounce_delay = debounce_delay / 1000

    def up(self) -> bool:
        """Return whether the up button is pressed."""
        if self.up_last_pressed < time.monotonic() - self.debounce_delay:
            self.up_last_pressed = time.monotonic()
            return not IO.joystick_LU.value or not IO.joystick_RU.value

        return False

    def down(self) -> bool:
        """Return whether the down button is pressed."""
        if self.down_last_pressed < time.monotonic() - self.debounce_delay:
            self.down_last_pressed = time.monotonic()
            return not IO.joystick_LD.value or not IO.joystick_RD.value

        return False

    def left(self) -> bool:
        """Return whether the left button is pressed."""
        if self.left_last_pressed < time.monotonic() - self.debounce_delay:
            self.left_last_pressed = time.monotonic()
            return not IO.joystick_LU.value or not IO.joystick_LD.value

        return False

    def right(self) -> bool:
        """Return whether the right button is pressed."""
        if self.right_last_pressed < time.monotonic() - self.debounce_delay:
            self.right_last_pressed = time.monotonic()
            return not IO.joystick_RU.value or not IO.joystick_RD.value

        return False

    def press(self) -> bool:
        """Return whether the button is pressed."""
        if self.press_last_pressed < time.monotonic() - self.debounce_delay:
            self.press_last_pressed = time.monotonic()
            return not IO.joystick_P.value

        return False

class Menu:
    items: list[str]
    scroll: int
    cursor: int

    def __init__(self, items):
        self.set_items(items)

    def set_items(self, items):
        self.items = items
        self.scroll = 0
        self.cursor = 0

    def draw(self):
        OLED.driver.fill(0)
        self.draw_cursor()
        self.draw_items()
        OLED.driver.show()

    def draw_cursor(self):
        OLED.driver.text(">", 1, self.cursor * LINE_HEIGHT, True)

    def draw_items(self):
        item_count = len(self.items)
        scroll = self.scroll % item_count

        items_to_draw = self.items[scroll:scroll + LINE_COUNT]
        if len(items_to_draw) < LINE_COUNT and len(items_to_draw) != item_count:
            items_to_draw += self.items[0:LINE_COUNT - len(items_to_draw)]

        for i, item in enumerate(items_to_draw):
            OLED.driver.text(item, 10, i * LINE_HEIGHT, True)

    def move_cursor_up(self):
        if self.cursor > 0:
            self.cursor -= 1
        elif len(self.items) > LINE_COUNT:
            self.scroll -= 1

    def move_cursor_down(self):
        if self.cursor < len(self.items) - 1:
            if self.cursor < 3:
                self.cursor += 1
            else:
                self.scroll += 1

    def get_selected(self):
        return self.items[(self.cursor + self.scroll) % len(self.items)]

class FileMenu(Menu):
    root_directory: str
    current_directory: str
    directory_history: list[str]

    def __init__(self, root_directory=PROGRAMS_DIRECTORY):
        self.root_directory = root_directory
        self.current_directory = root_directory
        self.directory_history = []

        super().__init__(self.get_files())

    def get_files(self):
        files = os.listdir(self.current_directory)
        if (self.current_directory != self.root_directory):
            files.insert(0, "..")

        return files

    def chdir(self, directory):
        full_path = self.current_directory + "/" + directory

        if directory == "..":
            # Move up one directory
            self.current_directory = self.directory_history.pop()
            self.set_items(self.get_files())
        elif os.stat(full_path)[0] == 16384:
            # Go into a directory and save the directory history
            self.directory_history.append(self.current_directory)
            self.current_directory = full_path
            self.set_items(self.get_files())

menu = FileMenu()
button = DButton()

menu.draw()

while True:
    battery.check()

    if button.press():
        selected = menu.get_selected()
        file_path = menu.current_directory + "/" + selected

        if selected == ".." or os.stat(file_path)[0] == 16384:
            menu.chdir(selected)
        else:
            # Run the selected file
            time.sleep(1)
            run.runfile(file_path, not dev)

        menu.draw()

    if button.up():
        menu.move_cursor_up()
        menu.draw()

    if button.down():
        menu.move_cursor_down()
        menu.draw()

    time.sleep(0.0001)
