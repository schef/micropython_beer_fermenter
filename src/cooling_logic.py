import asyncio
import common_pins
import leds
from common import get_millis, millis_passed

in_progress_status = False
start_timestamp = 0
cooling_on_timeout_s = 60
cooling_off_timeout_s = 0
timeout = 0

def init():
    print("[CL]: init")
    stop()

def start():
    print("[CL]: start")
    global in_progress_status
    in_progress_status = True

def stop():
    print("[CL]: stop")
    global in_progress_status, start_timestamp
    in_progress_status = False
    leds.set_state_by_name(common_pins.COOLING.name, 0)
    start_timestamp = 0

def in_progress():
    return in_progress_status

def set_cooling_on_timeout_s(timeout):
    global cooling_on_timeout_s
    cooling_on_timeout_s = timeout

def set_cooling_off_timeout_s(timeout):
    global cooling_off_timeout_s
    cooling_off_timeout_s = timeout

def get_cooling_on_timout():
    return cooling_on_timeout_s

def get_cooling_off_timout():
    return cooling_off_timeout_s

async def loop():
    print("[CL]: loop")
    global start_timestamp
    cooling = leds.get_led_by_name(common_pins.COOLING.name)
    while True:
        if in_progress_status:
            if start_timestamp == 0:
                start_timestamp = get_millis()
                cooling.set_state(1)
            else:
                if cooling.get_state() == 1:
                    if millis_passed(start_timestamp) >= cooling_on_timeout_s * 1000 and cooling_off_timeout_s != 0:
                        start_timestamp = get_millis()
                        cooling.set_state(0)
                else:
                    if millis_passed(start_timestamp) >= cooling_off_timeout_s * 1000:
                        start_timestamp = get_millis()
                        cooling.set_state(1)
        await asyncio.sleep(1)
