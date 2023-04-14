import math
import random
from color import Color

# define 10 colors for the gradient
colors = [
    (115, 30, 45),      # 1. Red (hottest)
    (115, 60, 30),      # 2. Orange-red
    (115, 90, 20),      # 3. Orange
    (115, 115, 20),     # 4. Yellow
    (90, 115, 30),      # 5. Green-yellow
    (60, 115, 30),      # 6. Green
    (30, 115, 90),      # 7. Cyan
    (30, 90, 115),      # 8. Deep sky blue
    (30, 60, 115),      # 9. Dodger blue
    (45, 30, 115)       # 10. Blue (coldest)
]

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_colors(a, b, t):
    return(lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t))

def entropic_color(entropy, max_entropy):
    t = entropy / max_entropy
    
    if t < 0.075:
        t = t / 0.075
        return lerp_colors(colors[0], colors[1], t)
    elif t < 0.125:
        t = (t - 0.075) / 0.05
        return lerp_colors(colors[1], colors[2], t)
    elif t < 0.25:
        t = (t - 0.125) / 0.125
        return lerp_colors(colors[2], colors[3], t)
    elif t < 0.33:
        t = (t - 0.25) / 0.08
        return lerp_colors(colors[3], colors[4], t)
    elif t < 0.4:
        t = (t - 0.33) / 0.07
        return lerp_colors(colors[4], colors[5], t)
    elif t < 0.55:
        t = (t - 0.4) / 0.15
        return lerp_colors(colors[5], colors[6], t)
    elif t < 0.625:
        t = (t - 0.55) / 0.075
        return lerp_colors(colors[6], colors[7], t)
    elif t < 0.75:
        t = (t - 0.625) / 0.125
        return lerp_colors(colors[7], colors[8], t)
    else:
        t = (t - 0.75) / 0.5
        return lerp_colors(colors[8], colors[9], t)
    

class Path:
    def __init__(self, map_width, map_height, start, end, screen, center_x, center_y, sq_size, squares):
        self.screen = screen
        self.center_x = center_x
        self.center_y = center_y
        self.sq_size = sq_size
        self.n_map_x = map_width
        self.n_map_y = map_height
        self.start_index = start
        self.end_index = end
        self.squares = squares
        self.start_pos = self.index_to_pos(start)
        self.end_pos = self.index_to_pos(end)
        self.end_points = []
        self.exit_path = []
        self.walking = None
        self.searching = False
        self.mapped = False
        # find max manhatton distance to top left corner and top right corner
        self.max_entropy = max(self.man_distance(self.end_pos, (0,0)), self.man_distance(self.end_pos, (self.n_map_x, 0)))
        
    ## Manhattan distance - Number of steps to get from one point to another
    def man_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    ## Euclidian distance - Straight line distance between two points
    def euc_distance(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
    def index(self, x, y):
        return y * self.n_map_x + x
    
    def is_path(self, x, y):
        return self.squares[self.index(x, y)].path
    
    def is_checked(self, x, y):
        return self.squares[self.index(x, y)].checked
    
    def is_in_map(self, x, y):
        return 0 <= x < self.n_map_x and 0 <= y < self.n_map_y
    
    def check_endpoint(self, x, y):
        if self.is_in_map(x, y):
            if self.is_path(x, y) and not self.is_checked(x, y):
                return True
        return False
    
    def find_next_endpoint(self, location):
        res = []
        x = location[0]
        y = location[1]
        p1, p2, p3, p4 = (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)
        
        if self.check_endpoint(p1[0], p1[1]):
            res.append(p1)
        if self.check_endpoint(p2[0], p2[1]):
            res.append(p2)
        if self.check_endpoint(p3[0], p3[1]):
            res.append(p3)
        if self.check_endpoint(p4[0], p4[1]):
            res.append(p4)
            
        return res
    
    def index_to_pos(self, index):
        return (index % self.n_map_x, index // self.n_map_x)
    
    @staticmethod
    def find_path(squares, start, end):
        import random
        index = random.randint(start, end)
        
        while not squares[index].path:
            index = random.randint(start, end)
        
        return index
    
    def create_wall(self, index):
        self.squares[index].path = False
        self.squares[index].color = Color.Brown
        self.squares[index].fill = 0
        self.squares[index].entropy = 0

    def create_water(self,index):
        self.squares[index].path = False
        self.squares[index].color = Color.LightBlue
        self.squares[index].fill = 0
        self.squares[index].entropy = 0

    def find_new_start(self):
        self.start_index = self.find_path(self.squares, 0, self.n_map_y // 3 * self.n_map_x)
        self.start_pos = self.index_to_pos(self.start_index)
        
        self.squares[self.start_index].path = False
        self.squares[self.start_index].color = Color.LightRed
        self.squares[self.start_index].fill = 0
        self.squares[self.start_index].entropy = 0
        self.squares[self.start_index].x = self.start_pos[0]
        self.squares[self.start_index].y = self.start_pos[1]
        
    def find_new_end(self):
        self.end_index = self.find_path(self.squares, self.n_map_y // 3 * self.n_map_x, self.n_map_x * self.n_map_y)
        self.end_pos = self.index_to_pos(self.end_index)
        
        self.squares[self.end_index].path = False
        self.squares[self.end_index].color = Color.LightGreen
        self.squares[self.end_index].fill = 0
        self.squares[self.end_index].entropy = 0
        self.squares[self.end_index].x = self.end_pos[0]
        self.squares[self.end_index].y = self.end_pos[1]
    
    def finish_mapping(self):
        
        # check for any unreached paths
        for square in self.squares:
            if square.path and not square.checked:
                if random.randint(0, 1) == 0:
                    self.create_wall(square.index)
                else:
                    self.create_water(square.index)
                continue

        # check that start is not surrounded by walls
        self.walking = self.index_to_pos(self.start_index)
        if self.find_next_step() == None:
            # turn the current square into a wall
            self.create_wall(self.start_index)

            # and spawn new start
            self.find_new_start()
                
            
        # check that end is not surrounded by walls
        self.walking = self.index_to_pos(self.end_index)
        if self.find_next_step() == None:
            # turn self into wall, and spawn new end
            self.create_wall(self.end_index)
            
            # and spawn new end
            self.find_new_end()
        
        self.walking = None
        self.mapped = True
        
    
    def clean_up_end_points(self):
        if len(self.end_points) > 0:
            for end_point in self.end_points:
                entropy = self.squares[self.index(end_point[0], end_point[1])].entropy
                self.squares[self.index(end_point[0], end_point[1])].color = entropic_color(entropy, self.max_entropy)
            
        self.end_points = []
    
    def map_entropic_values(self):
        curr_end_points = self.end_points
        self.clean_up_end_points()
        
        for point in curr_end_points:
            entropy = self.squares[self.index(point[0], point[1])].entropy + 1
        
            next_points = self.find_next_endpoint(point)
            if len(next_points) > 0:
                for next_point in next_points:
                    self.squares[self.index(next_point[0], next_point[1])].color = Color.Green
                    self.squares[self.index(next_point[0], next_point[1])].checked = True
                    self.squares[self.index(next_point[0], next_point[1])].fill = 1
                    self.squares[self.index(next_point[0], next_point[1])].entropy = entropy
                    self.end_points.append(next_point)
                    
        # determine if we have mapped all the squares that are part of the path
        if len(self.end_points) == 0:
            self.finish_mapping()
    
    def is_at_target(self, x, y):
        return self.end_pos == (x, y)
    
    def find_next_step(self):
        lowest_entropy = None
        points = [
            (self.walking[0] - 1, self.walking[1]),         # left
            (self.walking[0] - 1, self.walking[1] - 1),     # left up
            (self.walking[0], self.walking[1] - 1),         # up
            (self.walking[0] + 1, self.walking[1] - 1),     # right up
            (self.walking[0] + 1, self.walking[1]),         # right
            (self.walking[0] + 1, self.walking[1] + 1),     # right down
            (self.walking[0], self.walking[1] + 1),         # down
            (self.walking[0] - 1, self.walking[1] + 1)      # left down
            ]
        best_point = None

        for point in points:
            if not self.is_at_target(point[0], point[1]):
                if self.is_in_map(point[0], point[1]):
                    if self.is_path(point[0], point[1]):
                        if lowest_entropy is None or self.squares[self.index(point[0], point[1])].entropy < lowest_entropy:
                            lowest_entropy = self.squares[self.index(point[0], point[1])].entropy
                            best_point = point
            else: 
                self.searching = False
                return point
        
        return best_point
    
    def find_exit(self):
        if self.walking is None:
            self.walking = self.start_pos
        
        step = self.find_next_step()
        
        self.squares[self.index(step[0], step[1])].color = Color.White
        self.exit_path.append(step)
        self.walking = step
        
    
    def find_entropic_path(self):
        if len(self.end_points) == 0:
            self.searching = True
            self.end_points = [self.end_pos]
            return
    
        if self.searching:
            if not self.mapped:
                self.map_entropic_values()
            else:
                self.find_exit()
        

        
            
    def find_linear_path(self):
        print("manhatton distance: ", self.get_man_distance(self.start_pos, self.end_pos))