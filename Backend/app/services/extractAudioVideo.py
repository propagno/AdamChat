from moviepy import *
import os
import tempfile
import logging
from werkzeug.utils import secure_filename

# Configuração de logs
logging.basicConfig(level=logging.DEBUG)


class AudioExtractor:
    def is_video_format_supported(self, video_file):
        """Verifica se o formato do vídeo é suportado."""
        supported_formats = [".mp4", ".avi", ".mkv",
                             ".mov"]  # Adicione os formatos suportados
        return any(video_file.filename.lower().endswith(ext) for ext in supported_formats)

    def extract_audio(self, video_file, target_sample_rate=48000):
        """
        Extrai o áudio de um arquivo de vídeo e salva em um arquivo temporário.
        :param video_file: Arquivo de vídeo.
        :param target_sample_rate: Taxa de amostragem desejada (16000 ou 48000 Hz).
        :return: Caminho do arquivo de áudio extraído ou mensagem de erro.
        """
        if target_sample_rate not in [16000, 48000]:
            return "Erro: A taxa de amostragem deve ser 16000 Hz ou 48000 Hz."

        # Salva o arquivo de vídeo temporariamente
        temp_video_path = os.path.join(
            tempfile.gettempdir(), secure_filename(video_file.filename))
        video_file.save(temp_video_path)
        logging.debug(f"Vídeo salvo temporariamente em: {temp_video_path}")

        try:
            # Tenta extrair o áudio do vídeo
            with VideoFileClip(temp_video_path) as video:
                audio = video.audio
                if audio is None:
                    logging.error("O arquivo de vídeo não contém áudio.")
                    return "Erro: O arquivo de vídeo não contém áudio."

                # Define o caminho do arquivo de áudio temporário
                temp_audio_path = os.path.join(
                    tempfile.gettempdir(), 'extracted_audio.wav')

                # Configurações para o áudio extraído
                audio_params = {
                    "codec": "pcm_s16le",  # Codec WAV de 16 bits
                    "fps": target_sample_rate,  # Taxa de amostragem desejada
                    "ffmpeg_params": ["-ac", "1"]  # Converte para mono
                }

                # Salva o áudio extraído
                audio.write_audiofile(temp_audio_path, **audio_params)
                logging.debug(f"Áudio extraído e salvo em: {temp_audio_path}")

                return temp_audio_path
        except Exception as e:
            logging.error(f"Erro ao extrair áudio do vídeo: {e}")
            return f"Erro ao extrair áudio do vídeo: {e}"
        finally:
            # Remove o arquivo de vídeo temporário
            try:
                os.remove(temp_video_path)
                logging.debug(
                    f"Arquivo de vídeo temporário removido: {temp_video_path}")
            except Exception as e:
                logging.error(
                    f"Erro ao remover arquivo de vídeo temporário: {e}")
