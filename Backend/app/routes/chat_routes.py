from flask import Blueprint
from app.controllers.chat_controller import chat

chat_bp = Blueprint("chat_bp", __name__)

chat_bp.route("/api/chat", methods=["POST"])(chat)
