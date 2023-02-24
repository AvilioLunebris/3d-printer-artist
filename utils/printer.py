import serial
import time
import numpy as np

from models.line import Line


class Printer:

    def __init__(self):
        try:
            self.serial = serial.Serial("COM3", 115200, timeout=1)
            self.x_offset = 63
            self.y_offset = 63
            self.z_offset = 36
            self.z_max = 0.4

            if not self.serial.isOpen():
                self.serial.open()

            self.write(["G28"])
            time.sleep(5)
            self.write(["G0 Z45"])        
            time.sleep(5)
        except Exception as e:
            print(e)
        
    def convert_numpy_array_to_gcode(self, img):
        img += self.z_offset

        gcode_instructions = []
        width = len(img[0]) 
        height = len(img) 

        for y in range(height):
            line = Line()
            line.y_cord = y + self.y_offset

            for x in range(width):
                z_cord = img[y][x]

                # Brand new line
                if line.start_x is None:
                    line.start_x = x + self.x_offset
                    line.z_cord = z_cord

                # Different color detected. End the current line and start a new one
                elif (line.z_cord != z_cord):
                    # Don't save if the line was just white pixels
                    if line.z_cord != (self.z_offset + self.z_max):
                        line.end_x = x + self.x_offset
                        gcode_instructions.append(line.get_gcode()) 

                    # Start a new line
                    line.start_x = x + self.x_offset
                    line.end_x = None
                    line.z_cord = z_cord
            
            # If the line hasn't ended and it's not a white line, end it and save
            if (line.end_x is None) and (line.z_cord != (self.z_offset + self.z_max)):
                line.end_x = width + self.x_offset
                gcode_instructions.append(line.get_gcode()) 
        
        return gcode_instructions
        
    def write(self, gcode_instructions: list):
        num_instructions = len(gcode_instructions)

        for  i in range(num_instructions):
            g_code = gcode_instructions[i]

            print(f"Sending command:\n{g_code}")
            self.serial.write(str.encode(g_code + '\r\n'))
            self.serial.flush()

            # Wait for command to finish
            while True:
                response = self.serial.readline()
                
                if response == b'ok\n':
                    print(f"Response: {self.serial.readline()}")
                    break
            time.sleep(2.5)

            print(f"{i+1}/{num_instructions} Instructions Completed...")
            print("-------------------------")

    def close(self):
        print("Closing Serial Port...")
        self.serial.close()