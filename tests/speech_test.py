import sys
sys.path.append('../')

from speech.SpeechArbitrator import SpeechArbitrator

speechArbitrator = SpeechArbitrator(None)
speechArbitrator.arbitrate_speech("1")