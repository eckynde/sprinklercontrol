import logging
from serial import Serial, SerialException
from django.conf import settings

logger = logging.getLogger(__name__)

class UARTManager:
    def __init__(self, uart_port, uart_baudrate = None):
        uart = Serial()
        uart.port = uart_port

        if uart_baudrate == None:
            uart.baudrate = uart.BAUDRATES[:1]
        else:
            uart.baudrate = uart_baudrate

        self.uart = uart

    def write_to_uart(self, content):
        with self.open_uart() as uart:
            return uart.write(content)
    
    # Reads all BSON documents from the UART interface
    def read_from_uart(self) -> list:
        with self.open_uart() as uart:
            results = []

            while uart.in_waiting > 4: # 4 for document length + 1 terminating byte
                first_four_bytes = uart.read(4)
                byte_count = int.from_bytes(first_four_bytes, "little", signed=True)
                rest_of_bson = uart.read(byte_count - 4)
                results.insert(first_four_bytes + rest_of_bson)

            if uart.in_waiting > 0: 
                logger.warn("Less than 5 bytes in UART buffer. This might mean the data in the buffer is corrupted.")
            else:
                logger.debug("Empty UART buffer")

            return results

    def open_uart(self) -> Serial:
        try:
            self.uart.open()
        except SerialException as se:
            logger.error("Error on opening UART:" + se)
            return None
        except ValueError as ve:
            logger.error("Error on opening UART: Invalid configuration (" + ve + ")")
            return None
        else:
            return self.uart
