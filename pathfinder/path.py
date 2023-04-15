# TODO: if an end point is in an unreachable area:
# remove the point, collapse the area, and find a new endpoint

class PathFinder:
    def __init__(self, map_sq):
        self.n_map_sq_x = map_sq[0]
        self.n_map_sq_y = map_sq[1]
        self.start_location = 0
        self.end_location = 0
        self.squares = []
    
    def hello_nested(self):
        print("Hello nested")