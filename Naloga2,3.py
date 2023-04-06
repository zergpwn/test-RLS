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
        self.ser.write(str.encode('C16:00:20:0:0'))
        self.ser.timeout = 0.5
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

    def test_read_encoder_bank_select(self):
        self.ser.write(str.encode('40'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_EDS_bank(self):
        self.ser.write(str.encode('41'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_ProfileID(self):
        self.ser.write(str.encode('42:43'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_serial_number(self):
        self.ser.write(str.encode('44:47'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_key_register(self):
        self.ser.write(str.encode('48'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_command_register(self):
        self.ser.write(str.encode('49'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_detailed_status(self):
        self.ser.write(str.encode('4A:4D'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))

    def test_read_encoder_sensor_temperature(self):
        self.ser.write(str.encode('4E:4F'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_signal_level(self):
        self.ser.write(str.encode('50:53'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))

    def test_read_encoder_measured_velocity(self):
        self.ser.write(str.encode('54:57'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))

    def test_read_encoder_persistent_detailed_status(self):
        self.ser.write(str.encode('58:5B'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))

    def test_read_encoder_parameter_access_status(self):
        self.ser.write(str.encode('5C'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_reserved(self):
        self.ser.write(str.encode('5D:73'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_FW_version(self):
        self.ser.write(str.encode('74:77'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_deviceID(self):
        self.ser.write(str.encode('78:7D'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_encoder_manufacturer_ID(self):
        self.ser.write(str.encode('7E:7F'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))
        
    def test_read_BISS(self):
        self.ser.write(str.encode('>'))
        self.ser.read_until(self.CR)
        print(self.ser.read_until(self.CR))

if __name__ == "__main__":
    # Create a TestEncoderWithE2019B test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEncoderWithE2019B)
    
    # Run all tests
    test_to_run = unittest.TestSuite()
    test_to_run.addTest(TestEncoderWithE2019B('test_read_BISS'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_bank_select'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_EDS_bank'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_ProfileID'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_serial_number'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_key_register'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_command_register'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_detailed_status'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_sensor_temperature'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_signal_level'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_measured_velocity'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_persistent_detailed_status'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_parameter_access_status'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_reserved'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_FW_version'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_deviceID'))
    test_to_run.addTest(TestEncoderWithE2019B('test_read_encoder_manufacturer_ID'))
    result = unittest.TextTestRunner().run(test_to_run)

    # Print the result of the tests
    print(result)
