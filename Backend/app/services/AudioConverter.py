from pydub import AudioSegment
import io


class AudioConverter:
    def convert_sample_rate(self, audio_file, new_rate):
        """
        Converte a taxa de amostragem de um arquivo de áudio.
        :param audio_file: Arquivo de áudio.
        :param new_rate: Nova taxa de amostragem.
        :return: Arquivo de áudio convertido e nova taxa de amostragem, ou mensagem de erro.
        """
        try:
            # Carrega o arquivo de áudio
            audio = AudioSegment.from_file(audio_file)
            print(
                f"Arquivo carregado com sucesso. Taxa de amostragem original: {audio.frame_rate} Hz")

            # Converte o áudio para 16-bit (pcm_s16le) se necessário
            if audio.sample_width != 2:  # 2 bytes = 16-bit
                print("Convertendo áudio para 16-bit...")
                audio = audio.set_sample_width(2)

            # Converte a taxa de amostragem
            print(f"Convertendo taxa de amostragem para {new_rate} Hz...")
            audio = audio.set_frame_rate(new_rate)

            # Salva o arquivo convertido em um buffer temporário
            temp_file = io.BytesIO()
            audio.export(temp_file, format="wav")
            temp_file.seek(0)

            # Verifica a taxa de amostragem do arquivo convertido
            converted_audio = AudioSegment.from_file(temp_file)
            print(
                f"Taxa de amostragem após conversão: {converted_audio.frame_rate} Hz")

            return temp_file, new_rate
        except Exception as e:
            return f"Erro ao converter a taxa de amostragem: {e}"

    def convert_ogg_to_wav(self, ogg_file):
        """
        Converte um arquivo .ogg para .wav.
        :param ogg_file: Arquivo de áudio no formato .ogg.
        :return: Arquivo de áudio convertido para .wav ou mensagem de erro.
        """
        try:
            # Carrega o arquivo .ogg
            audio = AudioSegment.from_file(ogg_file, format="ogg")
            print(
                f"Arquivo .ogg carregado com sucesso. Taxa de amostragem: {audio.frame_rate} Hz")

            # Converte o áudio para 16-bit (pcm_s16le) se necessário
            if audio.sample_width != 2:  # 2 bytes = 16-bit
                print("Convertendo áudio para 16-bit...")
                audio = audio.set_sample_width(2)

            # Salva o arquivo convertido em um buffer temporário
            wav_file = io.BytesIO()
            audio.export(wav_file, format="wav")
            wav_file.seek(0)

            print("Arquivo .ogg convertido para .wav com sucesso.")
            return wav_file
        except Exception as e:
            return f"Erro ao converter .ogg para .wav: {e}"
