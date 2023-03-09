''' 
Suppress error messages from portAudio and pyAudio that slow
down the program and spam the print output space
'''
from ctypes import *

# Define our error handler type
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)

''' 
Now continue with the rest of the program
'''
import time
import speech_recognition as sr
import SpeechDetector as sd

import argparse
import os
import struct
import wave
from datetime import datetime
from threading import Thread

import pvporcupine
from pvrecorder import PvRecorder


class PorcupineDemo(Thread):
    """
    Microphone Demo for Porcupine wake word engine. It creates an input audio stream from a microphone, monitors it, and
    upon detecting the specified wake word(s) prints the detection time and wake word on console. It optionally saves
    the recorded audio into a file for further debugging.
    """

    def __init__(
            self, 
            speech_detector, 
            access_key,
            library_path,
            model_path,
            keyword_paths,
            sensitivities,
            input_device_index=None,
            output_path=None):

        """
        Constructor.

        :param library_path: Absolute path to Porcupine's dynamic library.
        :param model_path: Absolute path to the file containing model parameters.
        :param keyword_paths: Absolute paths to keyword model files.
        :param sensitivities: Sensitivities for detecting keywords. Each value should be a number within [0, 1]. A
        higher sensitivity results in fewer misses at the cost of increasing the false alarm rate. If not set 0.5 will
        be used.
        :param input_device_index: Optional argument. If provided, audio is recorded from this input device. Otherwise,
        the default audio input device is used.
        :param output_path: If provided recorded audio will be stored in this location at the end of the run.
        """

        super(PorcupineDemo, self).__init__()

        self.speech_detector = speech_detector
        self.r = sr.Recognizer()

        self._access_key = access_key
        self._library_path = library_path
        self._model_path = model_path
        self._keyword_paths = keyword_paths
        self._sensitivities = sensitivities
        self._input_device_index = input_device_index

        self._output_path = output_path

    def run(self):
        """
         Creates an input audio stream, instantiates an instance of Porcupine object, and monitors the audio stream for
         occurrences of the wake word(s). It prints the time of detection for each occurrence and the wake word.
         """

        keywords = list()
        for x in self._keyword_paths:
            keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
            if len(keyword_phrase_part) > 6:
                keywords.append(' '.join(keyword_phrase_part[0:-6]))
            else:
                keywords.append(keyword_phrase_part[0])

        porcupine = None
        recorder = None
        wav_file = None
        try:
            porcupine = pvporcupine.create(
                access_key=self._access_key,
                library_path=self._library_path,
                model_path=self._model_path,
                keyword_paths=self._keyword_paths,
                sensitivities=self._sensitivities)

            #sample_rate = porcupine.sample_rate
            #frame_length = porcupine.frame_length
            #byte_depth = 2 # 16 bit audio is 2-byte audio

            recorder = PvRecorder(device_index=self._input_device_index, frame_length=porcupine.frame_length)
            recorder.start()

            while True:
                pcm = recorder.read()

                result = porcupine.process(pcm)
                if result >= 0:
                    recorder.stop()
                    print('[%s] Detected %s' % (str(datetime.now()), keywords[result]))
                    #self.speech_detector.detect_speech(source)
                    self.speech_detector.detect_speech()
                    recorder.start()
        except pvporcupine.PorcupineInvalidArgumentError as e:
            args = (
                self._access_key,
                self._library_path,
                self._model_path,
                self._keyword_paths,
                self._sensitivities,
            )
            print("One or more arguments provided to Porcupine is invalid: ", args)
            print("If all other arguments seem valid, ensure that '%s' is a valid AccessKey" % self._access_key)
            raise e
        except pvporcupine.PorcupineActivationError as e:
            print("AccessKey activation error")
            raise e
        except pvporcupine.PorcupineActivationLimitError as e:
            print("AccessKey '%s' has reached it's temporary device limit" % self._access_key)
            raise e
        except pvporcupine.PorcupineActivationRefusedError as e:
            print("AccessKey '%s' refused" % self._access_key)
            raise e
        except pvporcupine.PorcupineActivationThrottledError as e:
            print("AccessKey '%s' has been throttled" % self._access_key)
            raise e
        except pvporcupine.PorcupineError as e:
            print("Failed to initialize Porcupine")
            raise e
        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            if porcupine is not None:
                porcupine.delete()

            if recorder is not None:
                recorder.delete()

            if wav_file is not None:
                wav_file.close()

    @classmethod
    def show_audio_devices(cls):
        devices = PvRecorder.get_audio_devices()

        for i in range(len(devices)):
            print('index: %d, device name: %s' % (i, devices[i]))


def main():
    ACCESS_KEY = ""
    # Running as main paths
    #PATH = "./Hey-Edward_en_mac_v2_1_0/Hey-Edward_en_mac_v2_1_0.ppn"
    PATH = "./Hey-Edward_en_raspberry-pi_v2_1_0/Hey-Edward_en_raspberry-pi_v2_1_0.ppn"

    with open("./.env") as f:
        ACCESS_KEY = f.readline().strip()

    speech_detector = sd.SpeechDetector()

    PorcupineDemo(
        speech_detector=speech_detector,
        access_key=ACCESS_KEY,
        library_path=pvporcupine.LIBRARY_PATH,
        model_path=pvporcupine.MODEL_PATH,
        keyword_paths=[PATH],
        sensitivities=[0.65],
        input_device_index=-1,
        output_path=None).start()

    while True:
        print("Running (main thread)")
        time.sleep(1)

if __name__ == "__main__":
    main()
