class MockThreadRunner:
    def __init__(self, mode:int):
        self.mode = mode
        print("starting")

    def start(self):
        while(True):
            print("running " + str(self.mode))