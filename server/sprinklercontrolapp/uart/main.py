import uart.bson_helper
import bson
from server.settings import UART as UART_CONFIG
from uart.manager import UARTManager
from sprinklercontrolapp.models import Sprinkler

manager = UARTManager(UART_CONFIG.device, UART_CONFIG.baudrate)

# Directly control the sprinkler (on/off)
def direct_sprinkler_control(sprinkler_uuid, active):
    to_send = {
        "type": "direct_control",
        "direct_control": {
            "sprinkler": sprinkler_uuid,
            "active": active,
        },
    }

    manager.write_to_uart(bson.dumps(to_send))

def send_irrigation_plan(plan):
    intervals = []
    
    for interval in plan.timers.all():
        intervals.append(transform_interval(interval))

    to_send = {
        "type": "irrigation_plan",
        "irrigation_plan": intervals,
    }

    manager.write_to_uart(bson.dumps(to_send))

# Send irrigation plan that tells the microcontroller when to turn sprinklers on and off
def transform_interval(interval):
    # Transform list of weekdays to binary string (bitfield)
    weekdays_bitfield = 0        
    
    for day in interval.weekdays.all():
        if day.label == "Montag":
            weekdays_bitfield &= 0b0000_0001
        elif day.label == "Dienstag":
            weekdays_bitfield &= 0b0000_0010
        elif day.label == "Mittwoch":
            weekdays_bitfield &= 0b0000_0100
        elif day.label == "Donnerstag":
            weekdays_bitfield &= 0b0000_1000
        elif day.label == "Freitag":
            weekdays_bitfield &= 0b0001_0000
        elif day.label == "Samstag":
            weekdays_bitfield &= 0b0010_0000
        elif day.label == "Sonntag":
            weekdays_bitfield &= 0b0100_0000

    sprinkler_uuids = []
    for sprinkler in interval.sprinklers.all():
        sprinkler_uuids.append(sprinkler.uuid)

    return {
        "timestart": interval.timestart,
        "timestop": interval.timestop,
        "weekdays": weekdays_bitfield,
        "sprinklers": sprinkler_uuids,
    }

def set_sprinkler_label(sprinkler):
    to_send = {
        "type": "uuid",
        "uuid": sprinkler.uuid,
        "label": sprinkler.label
    }

    manager.write_to_uart(bson.dumps(to_send))

def get_sprinklers():
    to_send = {
        "type": "req_sprinklers"
    }

    manager.write_to_uart(bson.dumps(to_send))
    handle_read()

def handle_read():
    docs = manager.read_from_uart()
    for doc in docs:
        d = bson.loads(doc)

        d_type = None
        try:
            d_type = d['type']
            if d_type == 'res_sprinklers':
                # this key exists (specification)
                sprinklers = d['res_sprinklers']
                for spr in sprinklers:
                    Sprinkler.objects.filter(uuid=spr['uuid'])
                    if Sprinkler.objects.count() == 0:
                        Sprinkler.objects.create(uuid=spr['uuid'], label=spr['label'])
        except KeyError:
            continue
