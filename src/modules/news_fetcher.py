import requests
import logging
from .config import NEWS_API_KEY, NEWS_ENDPOINT
from .chat_interface import ChatInterface

class NewsFetcher:
    def __init__(self, profile):
        self.profile = profile
        self.chat = ChatInterface()
        self.logger = logging.getLogger(__name__)
    
    def fetch_and_summarize(self):
        """Busca notícias de tecnologia baseadas no perfil do usuário e resume usando DeepSeek"""
        try:
            self.logger.info("Iniciando busca de notícias...")
            
            tech_terms = ['tecnologia', 'inovação', 'startup', 'programação', 'desenvolvimento']
            query_terms = self.profile.stack + self.profile.interests + tech_terms
            query = ' OR '.join(query_terms)
            
            self.logger.info(f"Termos de busca: {query}")
            
            params = {
                'apiKey': NEWS_API_KEY,
                'q': query,
                'pageSize': 5,
                'sortBy': 'publishedAt',
                'language': 'pt',  
                'domains': 'tecmundo.com.br,canaltech.com.br,olhardigital.com.br,techtudo.com.br',
            }
            
            self.logger.info("Fazendo requisição para News API...")
            response = requests.get(NEWS_ENDPOINT, params=params)
            response.raise_for_status()
            
            articles = response.json().get('articles', [])
            self.logger.info(f"Encontradas {len(articles)} notícias")
            
            summaries = []
            for i, article in enumerate(articles, 1):
                self.logger.info(f"Processando notícia {i}/{len(articles)}")
                prompt = f"Resuma esta notícia de tecnologia em 2-3 frases em português: {article['title']} - {article['description']}"
                summary = self.chat.send_message(prompt)
                
                summaries.append({
                    'title': article['title'],
                    'summary': summary,
                    'url': article['url'],
                    'published_at': article['publishedAt']
                })
            
            self.logger.info("Processamento de notícias concluído")
            return summaries
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro ao buscar notícias: {str(e)}")
            return [{
                'title': 'Erro',
                'summary': f"Falha ao buscar notícias: {str(e)}",
                'url': '',
                'published_at': ''
            }]
        except Exception as e:
            self.logger.error(f"Erro inesperado ao processar notícias: {str(e)}")
            return [{
                'title': 'Erro',
                'summary': f"Falha ao buscar notícias: {str(e)}",
                'url': '',
                'published_at': ''
            }] 