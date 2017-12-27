from escpos import *

#Epson = printer.Usb(0x04b8,0x0202)
#Epson = printer.Serial("/dev/ttyUSB0")
Epson = printer.Network("172.16.0.112")  
# Print text
Epson.set("center", "A", "", 1, 2)
Epson.text("Jakc Labs\n")
Epson.set("center", "A", "", 1, 1)
Epson.text("Jakarta")
Epson.text("\n")
Epson.text("\n")
 
# Print image
#Epson.image("logo.gif") 
# Print QR Code
#Epson.qr("You can readme from your smartphone")
# Print barcode
Epson.barcode('1324354657689','EAN13',64,2,'','')
# Cut paper
Epson.cut()
                