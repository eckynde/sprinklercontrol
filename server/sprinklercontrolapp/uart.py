import bson
import logging
from serial import Serial
from django.conf import settings

logger = logging.getLogger(__name__)

def write_to_uart(content):
    with open_uart() as uart:
        uart.write(content)

def open_uart() -> Serial:
    uart = Serial(settings.UART.device, baudrate = settings.UART.baudrate)
    logger.info('Opened UART interface ' + uart.name)
    return uart    

def bson_from_model(model_instance):
    d = get_dict_except_state(model_instance)
    return bson.dumps(d)

def get_dict_except_state(obj):
    d = obj.__dict__
    return { k: d[k] for k in set(list(d.keys())) - set(['_state']) }
