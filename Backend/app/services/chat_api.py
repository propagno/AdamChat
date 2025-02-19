import requests
import os
from dotenv import load_dotenv

# Garante que as variáveis de ambiente estejam carregadas
load_dotenv()


class ChatAPI:
    def __init__(self):
        self.api_keys = {
            "gemini": os.getenv("GEMINI_API_KEY"),
            "chatgpt": os.getenv("CHATGPT_API_KEY"),
            "outra_api": os.getenv("OUTRA_API_KEY")
        }

    def chat_with_gemini(self, user_input):
        api_key = self.api_keys["gemini"]
        base_url = "https://generativelanguage.googleapis.com"
        endpoint = f"{base_url}/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{
                    "text": user_input
                }]
            }]
        }
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            if "candidates" in response_data:
                return response_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "Erro: Resposta inválida da API."
        except requests.exceptions.RequestException as e:
            return f"Erro ao conectar com a API: {e}"
        except ValueError as e:
            return f"Erro ao processar a resposta da API: {e}"

    def chat_with_outra_api(self, user_input):
        # Placeholder para outra API
        return "Resposta da outra API"

    def chat_with_chatgpt(self, user_input):
        api_key = self.api_keys["chatgpt"]
        base_url = "https://api.openai.com/v1/chat/completions"  # Endpoint para ChatGPT
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-3.5-turbo",  # Modelo ChatGPT
            "messages": [
                {"role": "user", "content": user_input}
            ],
            "max_tokens": 150
        }
        try:
            response = requests.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            if "choices" in response_data:
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                return "Erro: Resposta inválida da API."
        except requests.exceptions.RequestException as e:
            return f"Erro ao conectar com a API: {e}"
        except ValueError as e:
            return f"Erro ao processar a resposta da API: {e}"
