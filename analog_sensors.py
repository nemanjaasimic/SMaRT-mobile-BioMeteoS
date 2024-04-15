import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Software SPI configuration:
# CLK  = 31
# MISO = 29
# MOSI = 18
# CS   = 16
# mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

 
def get_wind_speed():
    adc_0 = mcp.read_adc(0)
    # wind_speed = measured_value / MAX_MEASURED_VALUE * MAX_WIND_SPEED_MEASURED
    wind_speed = adc_0 / 1023 * 60
    wind_speed = round(wind_speed, 3)

    return wind_speed