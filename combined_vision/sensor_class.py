import time

class Sensor:

    def __init__(self, hist_length, min_delay=0) -> None:
        self.hist = []
        self.hist_length = hist_length
        self.min_delay = min_delay
    
    def push(self, value):
        if time.time() > self.hist[-1][0] + self.min_delay:
            self.hist.push((time.time(), value))
        while time.time() > self.hist[0][0] + self.hist_length:
            self.hist.pop(0)
        
    def find_above(self, thresh):
        return max(self.hist, key=lambda x : x[1] if x[0] + self.hist_length > time.time() else None) > thresh

    def not_find_above(self, thresh):
        return not self.find_above(thresh)

    def find_below(self, thresh):
        return min(self.hist, key=lambda x : x[1] if x[0] + self.hist_length > time.time() else None) < thresh

    def not_find_below(self, thresh):
        return not self.find_below(thresh)

    def find_case(self, value):
        return value in [x[1] for x in self.hist]

    def get_recent(self):
        return self.hist[-1][1]