import sys
import threading
import time
sys.path.append('../')

from AudioSuggester import AudioSuggester

engine = AudioSuggester()
text = "testing testing testing"

suggest_thread = threading.Thread(target=engine.run)
suggest_thread.start()
print("suggest Thread started")

time.sleep(3)

engine.approach_stop()

time.sleep(3)

engine.enable_suggestions()
