import time

class Incident:
    
    def __init__(self, name, refract_time, conditions, complain_fn=None) -> None:
        self.name = name
        self.refract_time = refract_time
        self.conditions = conditions
        self.past_time = time.time() - refract_time
        self.complain_fn = complain_fn
        pass


    def check_incident(self):
        if time.time() < self.past_time + self.refract_time:
            return False
        for f, v in self.conditions:
            # if self.name == "Tired While Driving":
            #     print("incident check", f(v))
            if not f(v):
                return False
        print("INCIDENT", self.name)
        if self.complain_fn != None:
            self.complain_fn()
        self.past_time = time.time()
        return True

    def upload_incident(self):
        #upload to firebase
        pass