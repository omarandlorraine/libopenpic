#!/usr/bin/python3
import sys

class pic16():
	def registers(self):
		self.regs = {
			'pir1': 0x0c,
			'pir2': 0x0d
		}
	
	def port(self, name, offset):
		self.regs['port' + name] = offset
		self.regs['tris' + name] = 0x80 + offset

	def __init__(self):
		self.registers()
		self.port('a', 0x05)
		self.port('b', 0x06)
		self.port('c', 0x07)
		self.port('e', 0x09) # TODO: Not all bits on port E are available on all pic16s.


class pic16f886(pic16):
	def __init__(self):
		super().__init__()

class pic16f887(pic16):
	def __init__(self):
		super().__init__()
		self.port('d', 0x08)

model = eval(sys.argv[1] + "()")
for name in model.regs:
	print("#define %s %s" % (name.upper(), hex(model.regs[name])))
