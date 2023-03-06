class MockThreadRunner:
    def __init__(self):
        print("starting")
        
    def start(self):
        while(True):
            print("running")