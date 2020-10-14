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
