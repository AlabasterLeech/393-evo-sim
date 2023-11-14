class Object:
    def __init__(self, x, y, object_type, density):
        self.x = x
        self.y = y
        self.object_type = object_type  # Type of object: 'food' or 'obstacle'
        self.density = density  # Density of the object

    def get_state(self):
        # Returns the current state of the object
        return {
            "x": self.x,
            "y": self.y,
            "object_type": self.object_type,
            "density": self.density
        }

    def set_state(self, state):
        # Sets the state of the object
        self.x = state["x"]
        self.y = state["y"]
        self.object_type = state["object_type"]
        self.density = state["density"]

    def get_location(self):
        # Returns the location of the object
        return (self.x, self.y)

