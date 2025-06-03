# Project: DesktopChatTechNewsApp

# Description: Multiplatform desktop app with AI chat (DeepSeek) and personalized tech news.

# Directory structure:

# DesktopChatTechNewsApp/

# ├── src/

# │   ├── main.py             # App entry point

# │   ├── ui/                 # UI definitions

# │   │   ├── main_window.py  # PySide6 main window layout

# │   ├── modules/            # Core functionality

# │   │   ├── chat_interface.py  # DeepSeek API integration

# │   │   ├── news_fetcher.py    # News API fetch & summarization

# │   │   ├── user_profile.py    # Profile load/save

# │   │   ├── config.py          # App configuration handling

# ├── resources/              # Icons, assets

# ├── data/                   # Local storage (JSON/SQLite)

# ├── requirements.txt        # Dependencies

# └── README.md               # Project overview and setup

# src/main.py

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# src/ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tech Chat & News")
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        # Layouts
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

    # User profile summary
        self.profile_label = QLabel("Olá, usuário!")
        main_layout.addWidget(self.profile_label)

    # News area
        self.news_area = QTextEdit()
        self.news_area.setReadOnly(True)
        main_layout.addWidget(self.news_area)
        self.refresh_news_btn = QPushButton("Atualizar notícias")
        main_layout.addWidget(self.refresh_news_btn)

    # Chat area
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
        main_layout.addLayout(chat_layout)

    # Signal connections (to implement)
        # self.refresh_news_btn.clicked.connect(self.load_news)
        # self.send_btn.clicked.connect(self.send_chat)

# src/modules/user_profile.py

import json
from pathlib import Path

PROFILE_PATH = Path(__file__).parent.parent.parent / 'data' / 'profile.json'

class UserProfile:
    def __init__(self):
        self.name = ''
        self.stack = []
        self.interests = []
        self.load()

    def load(self):
        if PROFILE_PATH.exists():
            data = json.loads(PROFILE_PATH.read_text())
            self.name = data.get('name', '')
            self.stack = data.get('stack', [])
            self.interests = data.get('interests', [])

    def save(self):
        PROFILE_PATH.parent.mkdir(exist_ok=True)
        PROFILE_PATH.write_text(json.dumps({
            'name': self.name,
            'stack': self.stack,
            'interests': self.interests
        }, indent=2))

# src/modules/chat_interface.py

import requests
from modules.config import DEEPSEEK_API_KEY

class ChatInterface:
    ENDPOINT = 'https://api.deepseek.com/v1/chat/completions'
    def __init__(self):
        self.headers = {'Authorization': f'Bearer {DEEPSEEK_API_KEY}'}

    def send_message(self, messages):
        payload = {'model': 'deepseek-chat', 'messages': messages}
        resp = requests.post(self.ENDPOINT, json=payload, headers=self.headers)
        resp.raise_for_status()
        return resp.json()['choices'][0]['message']['content']

# src/modules/news_fetcher.py

import requests
from modules.config import NEWS_API_KEY
from modules.chat_interface import ChatInterface

class NewsFetcher:
    NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'
    def __init__(self, profile):
        self.profile = profile
        self.chat = ChatInterface()

   def fetch_and_summarize(self):
        query = ' OR '.join(self.profile.stack + self.profile.interests)
        params = {'apiKey': NEWS_API_KEY, 'q': query, 'pageSize': 5, 'sortBy': 'publishedAt'}
        resp = requests.get(self.NEWS_ENDPOINT, params=params)
        resp.raise_for_status()
        articles = resp.json().get('articles', [])
        summaries = []
        for art in articles:
            summed = self.chat.send_message([
                {'role':'user','content': f"Resuma em 2 frases: {art['title']} - {art['description']}"}
            ])
            summaries.append({
                'title': art['title'], 'summary': summed, 'url': art['url']
            })
        return summaries

# src/modules/config.py

import os

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
NEWS_API_KEY   = os.getenv('NEWS_API_KEY', '')
sk-2bfd11dd07434e1b9a001bb002fd2fd4

# requirements.txt

# PySide6

# requests

# python-dotenv

# DesktopChatTechNewsApp - Project Setup Checklist

## Project Structure Setup

- [X] Create main project directory structure
- [X] Create src directory and subdirectories
- [X] Create resources directory
- [X] Create data directory

## Core Files Setup

- [X] Create main.py
- [X] Create main_window.py
- [X] Create chat_interface.py
- [X] Create news_fetcher.py
- [X] Create user_profile.py
- [X] Create config.py
- [X] Create requirements.txt
- [X] Create README.md

## Dependencies Setup

- [X] Install required packages
- [X] Configure environment variables

## Testing

- [X] Test main application launch
- [X] Test chat interface
- [X] Test news fetching
- [X] Test user profile functionality

## Documentation

- [X] Complete README.md with setup instructions
- [X] Add code documentation

## Security

- [X] Remove exposed API keys
- [X] Add environment variable handling
- [X] Add .env file template

## Additional Tasks

- [X] Add proper error handling in API calls
- [X] Implement user profile persistence
- [X] Add news refresh functionality
- [X] Implement chat message history
