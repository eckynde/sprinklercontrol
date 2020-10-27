import logging
from serial import Serial, SerialException
from django.conf import settings

logger = logging.getLogger(__name__)

class UARTManager:
    def __init__(self, uart_port, uart_baudrate = None):
        # Create and configure a Serial instance that represents the UART interface
        uart = Serial()
        uart.port = uart_port

        if uart_baudrate == None:
            # If not specified, use highest available baudrate
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

            while uart.in_waiting > 4: # Minimal BSON document is 5 bytes long
                first_four_bytes = uart.read(4)
                doc_length = int.from_bytes(first_four_bytes, "little", signed=True)
                rest_of_bson = uart.read(doc_length - 4)
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
            logger.error("Error on opening UART:" + str(se))
            return None
        except ValueError as ve:
            logger.error("Error on opening UART: Invalid configuration (" + str(ve) + ")")
            return None
        else:
            logger.info("UART port has been opened")
            return self.uart
