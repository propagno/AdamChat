from google.cloud import speech
from pydub import AudioSegment
import io
import os
from app.services.AudioConverter import AudioConverter


class Transcriber:
    def __init__(self):
        self.client = speech.SpeechClient()
        self.converter = AudioConverter()

    def transcribe_audio(self, audio_file):
        """
        Transcreve um arquivo de áudio, convertendo-o para .wav se necessário.
        :param audio_file: Arquivo de áudio.
        :return: Texto transcrito ou mensagem de erro.
        """
        try:
            # Converte o áudio para mono e verifica o formato
            audio_file = self._convert_to_mono(audio_file)
            if isinstance(audio_file, str):  # Se houver erro
                return audio_file

            sample_rate = self._check_sample_rate(audio_file)
            if isinstance(sample_rate, str):  # Se houver erro
                return sample_rate

            # Converte para uma taxa de amostragem compatível, se necessário
            if sample_rate not in [16000, 48000]:
                print(
                    f"Convertendo a taxa de amostragem de {sample_rate} Hz para 48000 Hz...")
                result = self.converter.convert_sample_rate(audio_file, 48000)
                if isinstance(result, str):  # Se houver erro
                    return result
                audio_file, new_sample_rate = result  # Desempacota o resultado
                print(
                    f"Taxa de amostragem após conversão: {new_sample_rate} Hz")
                sample_rate = new_sample_rate  # Atualiza a taxa de amostragem

            # Garante que o ponteiro do arquivo está no início
            audio_file.seek(0)
            content = audio_file.read()
            if not content:
                return "Erro: O conteúdo do áudio está vazio."

            # Configura o áudio para reconhecimento
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate,  # Usa a taxa de amostragem detectada ou convertida
                language_code="pt-BR"
            )

            # Faz a requisição para a API
            try:
                response = self.client.recognize(config=config, audio=audio)
                return self._extract_transcription(response)
            except Exception as e:
                return f"Erro ao transcrever o áudio: {e}"
        except Exception as e:
            return f"Erro ao processar o áudio: {e}"

    def _convert_to_mono(self, audio_file):
        """
        Converte o áudio para mono e, se necessário, converte .ogg para .wav.
        :param audio_file: Arquivo de áudio.
        :return: Arquivo de áudio em mono ou mensagem de erro.
        """
        try:
            # Verifica se o arquivo é .ogg
            if audio_file.name.lower().endswith(".ogg"):
                print("Arquivo .ogg detectado. Convertendo para .wav...")
                audio_file = self.converter.convert_ogg_to_wav(audio_file)
                if isinstance(audio_file, str):  # Se houver erro
                    return audio_file

            # Carrega o arquivo de áudio
            audio = AudioSegment.from_file(audio_file)
            print(
                f"Arquivo carregado com sucesso. Canais: {audio.channels}, Taxa de amostragem: {audio.frame_rate} Hz")

            # Converte para mono
            audio = audio.set_channels(1)
            temp_file = io.BytesIO()
            audio.export(temp_file, format="wav")
            temp_file.seek(0)

            return temp_file
        except Exception as e:
            return f"Erro ao converter o áudio para mono: {e}"

    def _check_sample_rate(self, audio_file):
        """
        Verifica a taxa de amostragem do áudio.
        :param audio_file: Arquivo de áudio.
        :return: Taxa de amostragem ou mensagem de erro.
        """
        try:
            audio = AudioSegment.from_file(audio_file)
            sample_rate = audio.frame_rate
            print(f"Taxa de amostragem detectada: {sample_rate} Hz")
            return sample_rate
        except Exception as e:
            return f"Erro ao verificar a taxa de amostragem: {e}"

    def _extract_transcription(self, response):
        """
        Extrai a transcrição da resposta da API.
        :param response: Resposta da API do Google Speech-to-Text.
        :return: Texto transcrito.
        """
        for result in response.results:
            return result.alternatives[0].transcript
        return "Não foi possível transcrever o áudio."

    def print_sample_rate(self, audio_file):
        """
        Imprime a taxa de amostragem do arquivo de áudio.
        :param audio_file: Arquivo de áudio.
        :return: Taxa de amostragem ou mensagem de erro.
        """
        try:
            audio = AudioSegment.from_file(audio_file)
            sample_rate = audio.frame_rate
            print(f"Taxa de amostragem do áudio: {sample_rate} Hz")
            return sample_rate
        except Exception as e:
            print(f"Erro ao verificar a taxa de amostragem: {e}")
            return None
