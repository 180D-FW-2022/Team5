import sys
sys.path.append('../')

from speech.StateArbitrator import StateArbitrator

stateArbitrator = StateArbitrator(None)
stateArbitrator.arbitrate_speech("1")