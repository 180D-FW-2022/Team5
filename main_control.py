import json

class Main_Control:
    def __init__(self):
        with open('config.txt') as f:
            data = f.read()

        settings = json.loads(data)

        self.should_suggest = settings["enable_suggest"]
        self.user = settings["user_id"]

    def run(self):
        while(1):
            print(self.should_suggest)


controller = Main_Control()
controller.run()