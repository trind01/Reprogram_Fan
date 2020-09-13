# Reprogram_Fan

This uses a 7-LED fan with a 24C08B EEPROM to store the animations.

The First byte is how many animations. Then an animation has the following format:\n
byte 1: Number of Characters\n
byte 2: Animation Control\n
bytes N: 5 bytes per character\n
This pattern repeats for every animation.\n

The Animation Control byte has the following format:\n
bit 0 - Erases from the back\n
bit 1 - Erases from the front\n
bit 2 - Erases from the top\n
bit 3 - Stops all animations from appearing\n
bit 4 - Unknown\n
bit 5 - Write direction 0-L to R, 1-R to L\n
bit 6 - Writes from bottom to top\n
bit 7 - Write(0) or instantly appear(1)\n

Combining the bits will make combination animations (erase from middle if b0,1) but the LEDs get weaker on the fan.

EEPROM
http://ww1.microchip.com/downloads/en/devicedoc/21081g.pdf