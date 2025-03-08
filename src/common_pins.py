class Pin:
    def __init__(self, id, name):
        self.id = id
        self.name = name

OLED_BUTTON_NEXT = Pin(15, "OLED_BUTTON_NEXT")
OLED_BUTTON_SELECT = Pin(17, "OLED_BUTTON_SELECT")

OLED_SPI_MOSI = Pin(11, "OLED_SPI_MOSI")
OLED_SPI_SCK = Pin(10, "OLED_SPI_SCK")
OLED_RST = Pin(12, "OLED_RST")
OLED_SPI_DC = Pin(8, "OLED_SPI_DC")
OLED_SPI_CS = Pin(9, "OLED_SPI_CS")
ONBOARD_LED = Pin("LED", "ONBOARD_LED")

ONEWIRE = Pin(22, "ONEWIRE")
HEATING = Pin(26, "HEATING")
COOLING = Pin(27, "COOLING")
