#!/usr/bin/python3
import sys

class pic16():
    def registers(self):
        self.regs = {
        'pir1': 0x0c,
        'pir2': 0x0d,
        'txsta': 0x98,
        'sspcon': 0x14
        }

    def interrupt(self, name, reg, bit):
        self.interrupts[name] = (reg, bit)

    def port(self, name, offset):
        self.regs['port' + name] = offset
        self.regs['tris' + name] = 0x80 + offset

    def bitdecl(self, regname, bitlist):
        for i, bname in enumerate(bitlist):
            self.bits.append((bname, regname, 1 << i))

    def timer1(self):
        self.regs['tmr1l'] = 0x0e
        self.regs['tmr1h'] = 0x0f
        self.regs['tmr1con'] = 0x10
        self.bitdecl('t1con', ['t1ginv', 'tmr1ge', 't1ckps1', 't1ckps0', 't1oscen', 't1sync', 'tmr1cs', 'tmr1on'])
        self.uint16s.append('tmr1')

    def __init__(self):
        self.interrupts = {}
        self.bits = []
        self.uint16s = []
        self.registers()
        self.timer1()
        self.interrupt('tmr1', '1', 0)
        self.interrupt('tmr2', '1', 1)
        self.interrupt('ccp1', '1', 2)
        self.bitdecl('txsta', ['csrc', 'tx9', 'txen', 'sync', 'sendb', 'brgh', 'trmt', 'tx9d']) 
        self.bitdecl('sspcon', ['wcol', 'sspov', 'sspen', 'ckp', 'sspm3', 'sspm2', 'sspm1', 'sspm0'])
        self.port('a', 0x05)
        self.port('b', 0x06)
        self.port('c', 0x07)
        self.port('e', 0x09) # TODO: Not all bits on port E are available on all pic16s.

    def print_regs(self):
        print("#ifdef __SDCC")
        for name in self.regs:
            print("volatile __data __at (%s) uint8_t %s;" % (hex(model.regs[name]), name.upper()))
        print("#else")
        for name in self.regs:
            print("#define %s (*(uint8_t*)%s)" % (name.upper(), hex(model.regs[name])))
        print("#endif")

    def print_bits(self):
        for bi in self.bits:
            bitinfo = (bi[0], bi[1].upper(), bi[2])
            print("#define READ_%s (%s & %d)" % bitinfo)
            print("#define SET_%s (%s |= %d)" % bitinfo)
            print("#define CLEAR_%s (%s &= ~(%d))" % bitinfo)

    def print_ports(self):
        for p in ports:
            print("#define GPIO%s %s" % (p, p))

    def print_uint16s(self):
        for u16 in self.uint16s:
            print("#define %s_U16 ((%sH << 8) | %sL)" % tuple([u16.upper()] * 3))

    def print_interrupts(self):
        for name in self.interrupts:
            deets = self.interrupts[name]
            de = "#define enable_%s_interrupt()" % name
            dr = "#define clear_%s_interrupt()" % name
            dc = "#define check_%s_interrupt()" % name
            ie = "(PIE%s &= ~(1ULL << %d))" % deets
            ir = "(PIR%s &= ~(1ULL << %d))" % deets
            ic = "(PIR%s & (1ULL << %d))" % deets
            print("%s %s" % (de, ie))
            print("%s %s" % (dr, ir))
            print("%s %s" % (dc, ic))

    def print(self):
        self.print_regs()
        self.print_bits()
        self.print_uint16s()
        self.print_interrupts()


class pic16f886(pic16):
	def __init__(self):
		super().__init__()

class pic16f887(pic16):
	def __init__(self):
		super().__init__()
		self.port('d', 0x08)

model = eval(sys.argv[1] + "()")

print("#include <stdint.h>")
model.print()
