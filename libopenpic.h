#define GPIO0 0x01
#define GPIO1 0x02
#define GPIO2 0x04
#define GPIO3 0x08
#define GPIO4 0x10
#define GPIO5 0x20
#define GPIO6 0x40
#define GPIO7 0x80

#define GPIO_CLEAR(PORT, PINS) (PORT &= ~(PINS))
#define GPIO_SET(PORT, PINS) (PORT |= (PINS))
#define GPIO_GET(PORT, PINS) (PORT & (PINS))

#define CLRWDT  __asm clrwdt __endasm;

void i2c_start();
void i2c_write(char b);
char i2c_read(bool ack);
void i2c_stop();
