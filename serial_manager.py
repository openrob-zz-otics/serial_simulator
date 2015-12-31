import threads
import serial
import serial.tools.list_ports
import sys

class SerialManager(object):

	user_input = None
	user_port = None
	user_baud = None
	serial_io = None
	watchdog = None
	auto_timer = None
	serial_printer = None
	ports = None

	def __init__(self):
		print "Initializing serial manager..."

	def open_port(self, user_input, baud):

		try:
			self.user_port = self.ports[int(user_input)][0]
			print "Attempting to connect to port " + self.user_port + "..."
			self.serial_io = serial.Serial(
				port 		= self.user_port,
				baudrate 	= baud,
				parity 		= serial.PARITY_NONE,
				stopbits 	= serial.STOPBITS_ONE,
				bytesize	= serial.EIGHTBITS,
				timeout 	= 0.01,
				writeTimeout = 0.01
			)
			print "Connected"
			return True

		except serial.serialutil.SerialException:
			print "Connection failed"	
			return False	

		except Exception as e:
			sys.exc_clear()
			return False

	def write(self):
		if self.serial_io is not None:
			self.serial_io.write("@RGBabc")

	def toggle_watchdog(self):
		if self.watchdog is None:
			print "Starting watchdog..."
			self.watchdog = threads.Watchdog()
		else:
			print "Stopping watchdog..."
			self.watchdog.stop()
			self.watchdog = None

	def start_serial_printer(self):
		print "Starting serial printer on " + self.user_port
		self.serial_printer = threads.Serial_printer(self.serial_io)

	def start_auto_timer(self):
		print "Starting auto timed function"
		def thing_to_do():
			print "AT THING TO DO"
		self.auto_timer = threads.Auto_timer(thing_to_do, 0.1)

	def list_ports(self):
		self.ports = list(serial.tools.list_ports.comports())
		for i in xrange(len(self.ports)):
			print "[" + str(i) + "] " + self.ports[i][0]

	def close(self):
		if self.watchdog is not None:
			self.watchdog.stop()
		if self.serial_printer is not None:
			self.serial_printer.stop()
		if self.auto_timer is not None:
			self.auto_timer.stop()

	def add_menu_functions(self, dict):
		if self.serial_io is not None:
			dict['p'] = self.start_serial_printer
			dict['w'] = self.toggle_watchdog
			dict['s'] = self.write
			dict['a'] = self.start_auto_timer