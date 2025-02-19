from flask import Blueprint, render_template, request, session, redirect, url_for
import os
import tempfile
import logging
from werkzeug.utils import secure_filename
from app.services.chat_api import ChatAPI
from app.services.transcriber import Transcriber
from app.services.extractAudioVideo import AudioExtractor

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')

logging.basicConfig(level=logging.DEBUG)

# Instancia os serviços
chat_api = ChatAPI()
transcriber = Transcriber()
audio_extractor = AudioExtractor()


def handle_api_selection(api_selection, combined_input):
    if api_selection == "gemini":
        return chat_api.chat_with_gemini(combined_input)
    elif api_selection == "outra_api":
        return chat_api.chat_with_outra_api(combined_input)
    elif api_selection == "chatgpt":
        return chat_api.chat_with_chatgpt(combined_input)
    else:
        return "API não suportada."


@dashboard_bp.route('/', methods=['GET', 'POST'])
def dashboard():
    # Garante que o usuário esteja autenticado
    if 'user_email' not in session:
        return redirect(url_for('auth_bp.login'))

    user_email = session['user_email']
    bot_response = None
    user_message = None
    error = None

    if request.method == "POST":
        try:
            user_message = request.form.get("user_message", "")
            api_selection = request.form.get("api_selection")
            audio_file = request.files.get("audio_file")
            video_file = request.files.get("video_file")
            transcribed_text = ""

            if video_file:
                # Extrai o áudio do vídeo
                audio_buffer = audio_extractor.extract_audio(video_file)
                if isinstance(audio_buffer, str) and audio_buffer.startswith("Erro"):
                    error = audio_buffer
                    return render_template("dashboard.html", email=user_email, error=error)
                transcribed_text = transcriber.transcribe_audio(audio_buffer)
            elif audio_file:
                # Salva o arquivo de áudio temporariamente
                temp_audio_path = os.path.join(
                    tempfile.gettempdir(), secure_filename(audio_file.filename))
                audio_file.save(temp_audio_path)
                logging.debug(
                    f"Áudio salvo temporariamente em: {temp_audio_path}")
                with open(temp_audio_path, "rb") as af:
                    transcribed_text = transcriber.transcribe_audio(af)
                try:
                    os.remove(temp_audio_path)
                except Exception as e:
                    logging.error(
                        f"Erro ao remover arquivo de áudio temporário: {e}")

            combined_input = f"{user_message} {transcribed_text}".strip()

            if combined_input.lower() in ["sair", "exit", "quit"]:
                bot_response = "Chat encerrado."
            else:
                bot_response = handle_api_selection(
                    api_selection, combined_input)
        except Exception as e:
            logging.error(f"Erro ao processar a solicitação: {e}")
            error = f"Erro ao processar a solicitação: {e}"

    return render_template("dashboard.html", email=user_email, user_message=user_message, bot_response=bot_response, error=error)
