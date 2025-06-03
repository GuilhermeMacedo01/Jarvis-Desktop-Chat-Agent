import requests
import logging
from .config import HUGGINGFACE_API_KEY, HUGGINGFACE_ENDPOINT

class ChatInterface:
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {HUGGINGFACE_API_KEY}',
            'Content-Type': 'application/json'
        }
        self.conversation_history = []
        self.logger = logging.getLogger(__name__)
    
    def send_message(self, message):
        """Envia uma mensagem para a API do HuggingFace e obtém uma resposta"""
        try:
            self.logger.info("Enviando mensagem para HuggingFace API...")
            
            # Prepara o histórico da conversa
            chat_history = " ".join([
                f"{'user' if msg['role'] == 'user' else 'assistant'}: {msg['content']}"
                for msg in self.conversation_history[-5:]
            ])
            
            # Prepara o prompt
            prompt = f"{chat_history} user: {message}"
            
            self.logger.info("Processando resposta...")
            response = requests.post(
                HUGGINGFACE_ENDPOINT,
                headers=self.headers,
                json={
                    'inputs': prompt,
                    'parameters': {
                        'max_length': 200,
                        'temperature': 0.7,
                        'top_p': 0.9,
                        'return_full_text': False,
                        'do_sample': True
                    }
                }
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            # Processa a resposta
            if isinstance(response_data, list) and len(response_data) > 0:
                assistant_message = response_data[0].get('generated_text', '')
                # Limpa a resposta para remover o prompt
                if "assistant:" in assistant_message.lower():
                    assistant_message = assistant_message.split("assistant:")[-1].strip()
            else:
                assistant_message = "Desculpe, não consegui processar sua mensagem corretamente."
            
            # Atualiza o histórico
            self.conversation_history.append({
                'role': 'user',
                'content': message
            })
            self.conversation_history.append({
                'role': 'assistant',
                'content': assistant_message
            })
            
            self.logger.info("Resposta recebida com sucesso")
            return assistant_message
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro ao enviar mensagem: {str(e)}")
            return f"Desculpe, tive um problema ao processar sua mensagem. Por favor, tente novamente."
        except Exception as e:
            self.logger.error(f"Erro inesperado: {str(e)}")
            return f"Desculpe, ocorreu um erro inesperado. Por favor, tente novamente."
    
    def clear_history(self):
        """Limpa o histórico de conversas"""
        self.conversation_history = [] 