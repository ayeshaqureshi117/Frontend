from TTS.api import TTS
import numpy as np

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
def emotional_TTS(text, emotion='Neutral', emotion_reference=''):
  audio_file = tts.tts(text=text,
                speaker_wav=emotion_reference,
                language="en",
                emotion = emotion)
  return audio_file