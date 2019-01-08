# Starts the definition of the class 'Coordinate' using inheritance.
class Coordinate(tuple):

    def __new__(cls, *args):
        # Similar function to an __init__ function. Called when a new
        # 'Coordinate' object is created. Essentially just creates a new
        # tuple object.
        return tuple.__new__(cls, args)

    def __add__(self, other):
        # Called when a 'Coordinate' object is added to another 'Coordinate'
        # object. Returns a new 'Coordinate' object with new values in
        # the tuple.
        return Coordinate(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        # Called when a 'Coordinate' object is minused from another
        # 'Coordinate' object. Returns a new 'Coordinate' object with new*
        # values in the tuple.
        return Coordinate(self[0] - other[0], self[1] - other[1])
