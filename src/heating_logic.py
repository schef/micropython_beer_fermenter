import asyncio
import common_pins
import leds
from common import get_millis, millis_passed

in_progress_status = False
start_timestamp = 0
heating_on_timeout_s = 3
heating_off_timeout_s = 57
timeout = 0

def init():
    print("[HL]: init")
    stop()

def start():
    print("[HL]: start")
    global in_progress_status
    in_progress_status = True

def stop():
    print("[HL]: stop")
    global in_progress_status, start_timestamp
    in_progress_status = False
    leds.set_state_by_name(common_pins.HEATING.name, 0)
    start_timestamp = 0

def in_progress():
    return in_progress_status

def set_heating_on_timeout_s(timeout):
    global heating_on_timeout_s
    heating_on_timeout_s = timeout

def set_heating_off_timeout_s(timeout):
    global heating_off_timeout_s
    heating_off_timeout_s = timeout

def get_heating_on_timout():
    return heating_on_timeout_s

def get_heating_off_timout():
    return heating_off_timeout_s

async def loop():
    print("[HL]: loop")
    global start_timestamp
    heating = leds.get_led_by_name(common_pins.HEATING.name)
    while True:
        if in_progress_status:
            if start_timestamp == 0:
                start_timestamp = get_millis()
                heating.set_state(1)
            else:
                if heating.get_state() == 1:
                    if millis_passed(start_timestamp) >= heating_on_timeout_s * 1000:
                        start_timestamp = get_millis()
                        heating.set_state(0)
                else:
                    if millis_passed(start_timestamp) >= heating_off_timeout_s * 1000:
                        start_timestamp = get_millis()
                        heating.set_state(1)
        await asyncio.sleep(1)
