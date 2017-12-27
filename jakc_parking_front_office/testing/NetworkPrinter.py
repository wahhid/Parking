from escpos import *

Epson = printer.Network('172.16.0.112')
Epson.text("Hello World")
Epson.barcode
Epson.barcode('1324354657687','EAN13',64,2,'','')
Epson.cut()