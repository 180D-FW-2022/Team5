#
# Copyright 2018-2021 Picovoice Inc.
#
# You may not use this file except in compliance with the license. A copy of the license is located in the "LICENSE"
# file accompanying this source.
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
import time

import argparse
import os
import struct
import wave
from datetime import datetime
from threading import Thread

import pvporcupine
from pvrecorder import PvRecorder

ACCESS_KEY = ""
PATH = "./Hey-Edward_en_mac_v2_1_0/Hey-Edward_en_mac_v2_1_0.ppn"
#PATH = "./Hey-Edward_en_raspberry-pi_v2_1_0/Hey-Edward_en_raspberry-pi_v2_1_0.ppn"

class PorcupineDemo(Thread):
    """
    Microphone Demo for Porcupine wake word engine. It creates an input audio stream from a microphone, monitors it, and
    upon detecting the specified wake word(s) prints the detection time and wake word on console. It optionally saves
    the recorded audio into a file for further debugging.
    """

    def __init__(
            self,
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

            recorder = PvRecorder(device_index=self._input_device_index, frame_length=porcupine.frame_length)
            recorder.start()

            '''
            if self._output_path is not None:
                wav_file = wave.open(self._output_path, "w")
                wav_file.setparams((1, 2, 16000, 512, "NONE", "NONE"))

            print('Using device: %s' % recorder.selected_device)

            print('Listening {')
            for keyword, sensitivity in zip(keywords, self._sensitivities):
                print('  %s (%.2f)' % (keyword, sensitivity))
            print('}')
            '''

            while True:
                pcm = recorder.read()

                if wav_file is not None:
                    wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

                result = porcupine.process(pcm)
                if result >= 0:
                    # TODO: CALLBACK RIGHT HERE
                    print('[%s] Detected %s' % (str(datetime.now()), keywords[result]))
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
    with open("./.env") as f:
        ACCESS_KEY = f.readline().strip()

    PorcupineDemo(
        access_key=ACCESS_KEY,
        library_path=pvporcupine.LIBRARY_PATH,
        model_path=pvporcupine.MODEL_PATH,
        keyword_paths=[PATH],
        sensitivities=[0.65],
        input_device_index=-1,
        output_path=None).start()

    while True:
        print("Running")
        time.sleep(1)

if __name__ == "__main__":
    main()
