# Reprogram_Fan

This uses a 7-LED fan with a 24C08B EEPROM to store the animations.

The First byte is how many animations. Then an animation has the following format:
byte 1: Number of Characters
byte 2: Animation Control
bytes N: 5 bytes per character
This pattern repeats for every animation.

The Animation Control byte has the following format:
bit 0 - Erases from the back
bit 1 - Erases from the front
bit 2 - Erases from the top
bit 3 - Stops all animations from appearing
bit 4 - Unknown
bit 5 - Write direction 0-L to R, 1-R to L
bit 6 - Writes from bottom to top
bit 7 - Write(0) or instantly appear(1)

Combining the bits will make combination animations (erase from middle if b0,1) but the LEDs get weaker on the fan.

EEPROM
http://ww1.microchip.com/downloads/en/devicedoc/21081g.pdf