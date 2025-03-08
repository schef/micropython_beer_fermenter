import asyncio

advertise_state_callback = None

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

def init():
    print("[PHY]: init")

async def action():
    while True:
        await asyncio.sleep(0.1)
