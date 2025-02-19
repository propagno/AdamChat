from flask import Blueprint, request, jsonify
from app.services.transcriber import Transcriber

# Cria o blueprint para as rotas de transcrição
transcriber_bp = Blueprint("transcriber_bp", __name__)

# Instancia o serviço de transcrição
transcriber = Transcriber()


@transcriber_bp.route("/api/transcribe", methods=["POST"])
def transcribe():
    # Aqui, vamos supor que o áudio seja enviado via multipart/form-data
    if "audio_file" not in request.files:
        return jsonify({"error": "Nenhum arquivo de áudio enviado"}), 400
    audio_file = request.files["audio_file"]
    result = transcriber.transcribe_audio(audio_file)
    return jsonify({"transcription": result})
