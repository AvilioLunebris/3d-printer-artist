class Line:

    def __init__(self):
        self.start_x = None
        self.end_x = None
        self.y_cord = None
        self.z_cord = None

    def get_gcode(self):
        gcode = f"G0 X{self.start_x} Y{self.y_cord}\n" # Move to starting position
        gcode += f"G0 Z{self.z_cord}\n" # Move pen down to touch paper
        gcode += f"G0 X{self.end_x} Y{self.y_cord} Z{self.z_cord}\n" # Move to ending position while pen is still touching paper
        gcode += f"G0 Z{self.z_cord+5}" # Move pen back up to move to the next position without drawing
        return gcode