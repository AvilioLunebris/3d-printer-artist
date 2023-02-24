from utils import opencv
from utils.printer import Printer
from utils import math

printer = Printer()

img = opencv.load_image("images/esfand.jpg") 
img = opencv.resize_image(img, 172, 172)
img = math.normalize(img, printer.z_max) # Convert colors from 0-255 to 0 to z-max to represent the brightness of the pixel

gcode_instructions = printer.convert_numpy_array_to_gcode(img)
printer.write(gcode_instructions)
printer.close()