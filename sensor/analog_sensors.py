import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import sensor.gpio_pinout as gpio_pinout
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

 
def get_uv_intensity():
    GPIO.output(gpio_pinout.ML_8511_UV_POWER_PIN, True)
    time.sleep(1)

    uv_intensity = [0]*5
    for i in range(5):
        uv_intensity_measured = mcp.read_adc(1)
        # 0-1023 = 0-3.3v
        # 310 = 1V --> min uv of 0 (mW/cm^2)
        # 885 = 2.85V --> max uv of 15 (mW/cm^2)
        # scaling real_value = measured_value - 310 which means offset is [0-575]
        uv_intensity[i] = (uv_intensity_measured - 310) / 575 * 15
        time.sleep(0.5)


    uv_intensity = round(sum(uv_intensity) / len(uv_intensity), 2)

    GPIO.output(gpio_pinout.ML_8511_UV_POWER_PIN, False)

    if uv_intensity < 0:
        uv_intensity = 0

    return uv_intensity
