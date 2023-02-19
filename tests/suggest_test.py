import sys
sys.path.append('../')

from AudioSuggester import AudioSuggester

engine = AudioSuggester()
text = "testing testing testing"
engine.say(text)