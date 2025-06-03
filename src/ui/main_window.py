from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QSplitter,
    QMessageBox
)
from PySide6.QtCore import Qt
import logging
from modules.chat_interface import ChatInterface
from modules.news_fetcher import NewsFetcher
from modules.user_profile import UserProfile
from modules.config import validate_api_keys

class QTextEditLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)
        self.widget.verticalScrollBar().setValue(
            self.widget.verticalScrollBar().maximum()
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tech Chat & News")
        self.setMinimumSize(800, 600)
        
        self.profile = UserProfile()
        self.chat = ChatInterface()
        self.news_fetcher = NewsFetcher(self.profile)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)
        
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)

        main_content = QWidget()
        main_content_layout = QVBoxLayout()
        main_content.setLayout(main_content_layout)
        splitter.addWidget(main_content)

        self.profile_label = QLabel(f"Olá, {self.profile.name or 'usuário'}!")
        main_content_layout.addWidget(self.profile_label)

        self.news_area = QTextEdit()
        self.news_area.setReadOnly(True)
        main_content_layout.addWidget(self.news_area)
        self.refresh_news_btn = QPushButton("Atualizar notícias")
        main_content_layout.addWidget(self.refresh_news_btn)

        chat_layout = QVBoxLayout()
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        chat_layout.addWidget(self.chat_history)
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.send_btn = QPushButton("Enviar")
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(self.send_btn)
        chat_layout.addLayout(input_layout)
        main_content_layout.addLayout(chat_layout)

        log_widget = QWidget()
        log_layout = QVBoxLayout()
        log_widget.setLayout(log_layout)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(150)
        log_layout.addWidget(QLabel("Logs:"))
        log_layout.addWidget(self.log_area)
        splitter.addWidget(log_widget)

        splitter.setSizes([700, 150])

        self.setup_logging()

        self.refresh_news_btn.clicked.connect(self.load_news)
        self.send_btn.clicked.connect(self.send_chat)
        self.chat_input.returnPressed.connect(self.send_chat)

        self.log("Aplicação iniciada com sucesso!")
        
        # Check API keys
        if not validate_api_keys():
            self.show_api_key_error()
        else:
            # Load initial news
            self.load_news()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.log_handler = QTextEditLogger(self.log_area)
        logging.getLogger().addHandler(self.log_handler)

    def show_api_key_error(self):
        """Show error message for missing API keys"""
        error_msg = """
        Chaves de API não configuradas!
        
        Por favor, crie um arquivo .env na raiz do projeto com as seguintes chaves:
        
        HUGGINGFACE_API_KEY=sua_chave_aqui
        NEWS_API_KEY=sua_chave_aqui
        
        Você pode obter as chaves em:
        - News API: https://newsapi.org/ (gratuito, 100 requisições/dia)
        - HuggingFace: https://huggingface.co/settings/tokens (gratuito, crie uma conta e gere um token)
        """
        QMessageBox.critical(self, "Erro de Configuração", error_msg)
        self.log("Erro: Chaves de API não configuradas!")

    def log(self, message):
        """Add a message to the log area"""
        self.log_area.append(f"{message}")
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )

    def load_news(self):
        """Load and display news"""
        if not validate_api_keys():
            self.show_api_key_error()
            return

        self.log("Carregando notícias...")
        try:
            news = self.news_fetcher.fetch_and_summarize()
            self.news_area.clear()
            for item in news:
                self.news_area.append(f"<h3>{item['title']}</h3>")
                self.news_area.append(f"<p>{item['summary']}</p>")
                self.news_area.append(f"<a href='{item['url']}'>Leia mais</a>")
                self.news_area.append("<hr>")
            self.log("Notícias carregadas com sucesso!")
        except Exception as e:
            self.log(f"Erro ao carregar notícias: {str(e)}")

    def send_chat(self):
        """Send chat message"""
        if not validate_api_keys():
            self.show_api_key_error()
            return

        message = self.chat_input.text().strip()
        if message:
            self.log(f"Enviando mensagem: {message}")
            self.chat_history.append(f"Você: {message}")
            self.chat_input.clear()
            
            try:
                response = self.chat.send_message([{'role': 'user', 'content': message}])
                self.chat_history.append(f"Assistente: {response}")
                self.log("Resposta recebida com sucesso!")
            except Exception as e:
                error_msg = f"Erro ao processar mensagem: {str(e)}"
                self.chat_history.append(f"Erro: {error_msg}")
                self.log(error_msg) 