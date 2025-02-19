from flask import request, jsonify
from app.services.chat_api import ChatAPI

chat_service = ChatAPI()


def chat():
    data = request.json
    response = chat_service.chat_with_gemini(data["message"])
    return jsonify({"response": response})
