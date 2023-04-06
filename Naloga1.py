"""
COPYRIGHT(c) 2020 RLS d.o.o, Pod vrbami 2, 1218 Komenda, Slovenia

"""
import time
import unittest
import serial.tools.list_ports
import serial


class TestEncoderWithE2019B(unittest.TestCase):
    CR = b'\r'

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.ser: serial.serialwin32.Serial = self._connect_on_first_E2019B_device(com_port='COM12', baudrate=9600)
        self._encoder_power_on()
        time.sleep(0.5)

    def tearDown(self):
        self._encoder_power_off()
        self.ser.close()

    @staticmethod
    def _detect_serial_devices():
        ports = list(serial.tools.list_ports.comports())
        print("Ports:")
        for i, port in enumerate(ports):
            print(f" \ni:{i} \n\tName: {port.name}, \n\tDevice:{port.device}, \n\tDescription:{port.description}, "
                  f"\n\tPid:{port.pid}, \n\tVid:{port.vid}, \n\tManufacturer:{port.manufacturer}, "
                  f"\n\tProduct:{port.product}, \n\tHwid:{port.hwid}, \n\tInterface:{port.interface}, "
                  f"\n\tSerial number:{port.serial_number}")
            print(f"\tPort info: {port.usb_info()}")
        return ports

    def _connect_on_first_E2019B_device(self, com_port, baudrate):
        return serial.Serial(com_port, baudrate)

    def _E2019B_version(self):
        self.ser.write(b'v')
        self.ser.flush()
        self.ser.timeout = 0.5
        data_read_byte = self.ser.read_until(self.CR)
        return str(data_read_byte, 'utf-8')

    def _read_encoder_position(self):
        self.ser.write(b'4')
        self.ser.flush()
        return self.ser.read_until(self.CR)
    

    def _set_encoder_parser(self):
        self.ser.write(str.encode('C22:00:20:1:1'))
        self.ser.read_until(self.CR)

    def _read_encoder_parsed_position(self):
        self.ser.write(b'>')
        self.ser.flush()
        self.ser.timeout = 2
        data_read_byte = self.ser.read_until(self.CR)
        return data_read_byte

    def _encoder_power_on(self):
        self.ser.write(b'N')

    def _encoder_power_off(self):
        self.ser.write(b'F')

    def test_version_read(self):
        version = self._E2019B_version()
        print(f"Version: {version}")

    def test_encoder_power_on(self):
        self._encoder_power_on()

    def test_encoder_power_off(self):
        self._encoder_power_off()

    def test_read_encoder_position(self):
        position = self._read_encoder_position()
        print(position)

    def test_read_encoder_serial_number(self):
        self.ser.write(str.encode('R04:068'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))

    def test_read_encoder_current_position(self):
        self.ser.write(str.encode('4'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))



if __name__ == "__main__":
    # Create a TestEncoderWithE2019B test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEncoderWithE2019B)
    
    # Run only the test_read_encoder_current_position() test method
    test_to_run = unittest.TestSuite()
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_current_position'))
    result = unittest.TextTestRunner().run(test_to_run)

    # Print the result of the test
    print(result)

