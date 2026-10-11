import os
import azure.cognitiveservices.speech as speechsdk
from cecilia.core.settings import settings

class TTS:
    def __init__(self):
        print("Starting TTS Azure")

        self.speech_config = speechsdk.SpeechConfig(
            subscription=settings.azure.speech_key,
            region=settings.azure.speech_region
        )

        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Webm24Khz16Bit24KbpsMonoOpus
        )

        # The neural multilingual voice can speak different languages based on the input text.
        self.speech_config.speech_synthesis_voice_name= settings.azure.speech_synthesis_voice_name

        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=None    
        )

    def synthesize(self, text: str):
        speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()

        return speech_synthesis_result.audio_data