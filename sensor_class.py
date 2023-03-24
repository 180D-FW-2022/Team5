import time

class Sensor:

    def __init__(self, hist_length, min_delay=0, default=0) -> None:
        self.hist = []
        self.hist_length = hist_length
        self.min_delay = min_delay
        self.default=default
    
    def push(self, value):
        if not self.hist:
            self.hist.append((time.time(), value))
            return

        if self.hist and time.time() > self.hist[-1][0] + self.min_delay:
            self.hist.append((time.time(), value))
        while self.hist and time.time() > self.hist[0][0] + self.hist_length:
            self.hist.pop(0)
        
    def find_above(self, thresh):
        while self.hist and time.time() > self.hist[0][0] + self.hist_length:
            self.hist.pop(0)
        if not self.hist:
            return self.default > thresh
        return max(self.hist, key=lambda x : x[1])[1] > thresh

    def not_find_above(self, thresh):
        return not self.find_above(thresh)

    def find_below(self, thresh):
        while self.hist and time.time() > self.hist[0][0] + self.hist_length:
            self.hist.pop(0)
        if not self.hist:
            return self.default < thresh
        return min(self.hist, key=lambda x : x[1])[1] < thresh

    def not_find_below(self, thresh):
        return not self.find_below(thresh)

    def find_case(self, value):
        while self.hist and time.time() > self.hist[0][0] + self.hist_length:
            self.hist.pop(0)
        return value in [x[1] for x in self.hist]
    
    def find_case_older(self, passed):
        value, min_age = passed
        while self.hist and time.time() > self.hist[0][0] + self.hist_length:
            self.hist.pop(0)
        max_idx = 0
        while max_idx < len(self.history) and time.time() - self.hist[max_idx][1] >= min_age:
            max_idx += 1
        return value in [x[1] for x in self.hist[:max_idx]]

    def get_recent(self):
        return self.hist[-1][1] if self.hist else self.default