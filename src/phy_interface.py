import asyncio
import heating_logic

advertise_state_callback = None

class Mode:
    HEATING_LOGIC = "heating_logic"

def _set_heating(state):
    if state:
        heating_logic.start()
        advertise_state(Mode.HEATING_LOGIC.upper(), 1)
    else:
        heating_logic.stop()
        advertise_state(Mode.HEATING_LOGIC.upper(), 0)

def set_heating(state):
    if state == 1:
        if heating_logic.in_progress():
            print("ERROR: heating already in progress")
        else:
            _set_heating(1)
    else:
        if heating_logic.in_progress():
            _set_heating(0)

def register_advertise_state_callback(callback):
    global advertise_state_callback
    advertise_state_callback = callback

def advertise_state(mode, state):
    if advertise_state_callback is not None:
        advertise_state_callback(mode, str(state))

def handle_request(thing):
    if thing.data == "request":
        state = None
        if state is not None:
            thing.data = state
            thing.dirty_out = True

def on_data_received(thing):
    handle_request(thing)

    if thing.path == Mode.HEATING_LOGIC:
        if thing.data == "1":
            set_heating(1)
        elif thing.data == "0":
            set_heating(0)
    elif thing.path == "heating_on_timeout":
        heating_logic.set_heating_on_timeout_s(int(thing.data))
        if advertise_state_callback is not None:
            advertise_state_callback(thing.path, thing.data)
    elif thing.path == "heating_off_timeout":
        heating_logic.set_heating_off_timeout_s(int(thing.data))
        if advertise_state_callback is not None:
            advertise_state_callback(thing.path, thing.data)

def init():
    print("[PHY]: init")

async def action():
    while True:
        await asyncio.sleep(0.1)
