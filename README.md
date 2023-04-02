# Emulators
My attempt at figuring out how to write basic CPU emulators. Not particularly concerned with being super efficient or modeling every aspect of the hardware. Just trying to write functional, readable code.

So far, I've completed my Python implementation of the SAP (Simple As Possible) Computer from Malvino's "Digital Computer Electronics", which inspired Ben Eater's 8-bit Breadboard Computer. My version of the SAP-3 is essentially a full Intel 8080 emulator, minus a couple of instructions involving binary-coded decimal arithmetic and the input instruction, since all input is handled by my own simple UI script. The clock speed is only about 20kHz (on my old laptop at least), so it's not exactly up to snuff in that department. But, I didn't expect it to be with my completely un-optimized Python code.

Next step is probably trying to get more comfortable with C++ so that I can reimplement this emulator, hopefully with significantly better performance, and maybe even some simple graphics. I might start with a CHIP-8 emulator to try to figure out graphics and sound in C++ before coming back to the SAP/8080.
