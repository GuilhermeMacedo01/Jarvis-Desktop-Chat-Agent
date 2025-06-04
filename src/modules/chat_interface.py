import logging
from transformers import pipeline
from .config import MODEL_NAME

class ChatInterface:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.conversation_history = []
        
        self.logger.info("Carregando modelo BlenderBot...")
        self.pipe = pipeline("text2text-generation", model=MODEL_NAME)
        self.logger.info("Modelo carregado com sucesso!")
    
    def send_message(self, message):
        """Envia uma mensagem para o modelo e obtém uma resposta"""
        try:
            self.logger.info("Processando mensagem...")
            
            if self.conversation_history:
                last_message = self.conversation_history[-1]["content"]
                prompt = f"{last_message} {message}"
            else:
                prompt = message
            
            outputs = self.pipe(
                [prompt],
                max_length=128,
                min_length=10,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                truncation=True 
            )
            
            if isinstance(outputs, list) and len(outputs) > 0:
                assistant_message = outputs[0].get("generated_text", "")
                if prompt in assistant_message:
                    assistant_message = assistant_message.replace(prompt, "").strip()
            else:
                assistant_message = "Desculpe, não consegui processar sua mensagem corretamente."
            
            self.conversation_history.append({
                'role': 'user',
                'content': message
            })
            self.conversation_history.append({
                'role': 'assistant',
                'content': assistant_message
            })
            
            if len(self.conversation_history) > 4:
                self.conversation_history = self.conversation_history[-4:]
            
            self.logger.info("Resposta gerada com sucesso")
            return assistant_message
            
        except Exception as e:
            self.logger.error(f"Erro ao processar mensagem: {str(e)}")
            return f"Desculpe, tive um problema ao processar sua mensagem. Por favor, tente novamente."
    
    def clear_history(self):
        """Limpa o histórico de conversas"""
        self.conversation_history = [] 