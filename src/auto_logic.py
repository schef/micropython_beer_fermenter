import asyncio
import sensors
import heating_logic
import cooling_logic

in_progress_status = False
target_temperature = 16.0

def init():
    print("[AL]: init")
    stop()

def start():
    print("[AL]: start")
    global in_progress_status
    in_progress_status = True

def stop():
    print("[AL]: stop")
    global in_progress_status
    in_progress_status = False
    heating_logic.stop()
    cooling_logic.stop()

def in_progress():
    return in_progress_status

def get_target_temperature():
    return target_temperature

def set_target_temperature(temperature):
    global target_temperature
    target_temperature = temperature

def get_liquid_temperature():
    temperatures = sensors.environment_sensors[0].get_temperature()
    temperature = temperatures.get("liquid")
    if temperature is not None:
        if temperature >= 50.0:
            return None
        elif temperature <= -5.0:
            return None
        else:
            return temperature

def get_air_temperature():
    temperatures = sensors.environment_sensors[0].get_temperature()
    temperature = temperatures.get("air")
    if temperature is not None:
        if temperature >= 50.0:
            return None
        elif temperature <= -5.0:
            return None
        else:
            return temperature

async def loop():
    print("[AL]: loop")
    while True:
        if in_progress():
            await asyncio.sleep(1)
            liquid_temperature = get_liquid_temperature()
            if liquid_temperature is None:
                print("[AL]: temp is None, turning off")
                if heating_logic.in_progress():
                    heating_logic.stop()
                if cooling_logic.in_progress():
                    cooling_logic.stop()
                continue
            ##### logic start #####
            if liquid_temperature >= target_temperature + 0.2:
                print("[AL]: to warm")
                if heating_logic.in_progress():
                    print("[AL]: heating_logic off")
                    heating_logic.stop()
                if not cooling_logic.in_progress():
                    print("[AL]: cooling_logic on")
                    cooling_logic.start()
            elif liquid_temperature <= target_temperature - 0.2:
                print("to cold")
                if cooling_logic.in_progress():
                    print("[AL]: cooling_logic off")
                    cooling_logic.stop()
                if not heating_logic.in_progress():
                    print("[AL]: heating_logic on")
                    heating_logic.start()
            else:
                print("[AL]: good")
                if cooling_logic.in_progress():
                    print("[AL]: cooling_logic off")
                    cooling_logic.stop()
                if heating_logic.in_progress():
                    print("[AL]: heating_logic off")
                    heating_logic.stop()
            await asyncio.sleep(1*60)
        else:
            await asyncio.sleep(1)
