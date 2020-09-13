# Reprogram_Fan

This uses a 7-LED fan with a 24C08B EEPROM to store the animations.

The First byte is how many animations. Then an animation has the following format:<br/> 
byte 1: Number of Characters<br/>
byte 2: Animation Control<br/>
bytes N: 5 bytes per character<br/>
This pattern repeats for every animation.<br/>

The Animation Control byte has the following format:<br/>
bit 0 - Erases from the back<br/>
bit 1 - Erases from the front<br/>
bit 2 - Erases from the top<br/>
bit 3 - Stops all animations from appearing<br/>
bit 4 - Unknown<br/>
bit 5 - Write direction 0-L to R, 1-R to L<br/>
bit 6 - Writes from bottom to top<br/>
bit 7 - Write(0) or instantly appear(1)<br/>

Combining the bits will make combination animations (erase from middle if b0,1) but the LEDs get weaker on the fan.

EEPROM
http://ww1.microchip.com/downloads/en/devicedoc/21081g.pdf