# Desktop Chat & Tech News App

A multiplatform desktop application that combines AI chat capabilities with personalized tech news.

## Features

- AI-powered chat interface using DeepSeek
- Personalized tech news based on user interests
- User profile management
- Modern PySide6-based UI

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your API keys:
     ```
     DEEPSEEK_API_KEY=your_deepseek_api_key_here
     NEWS_API_KEY=your_news_api_key_here
     ```

## Running the Application

```bash
python src/main.py
```

## Project Structure

```
DesktopChatTechNewsApp/
├── src/
│   ├── main.py             # App entry point
│   ├── ui/                 # UI definitions
│   │   ├── main_window.py  # PySide6 main window layout
│   ├── modules/            # Core functionality
│   │   ├── chat_interface.py  # DeepSeek API integration
│   │   ├── news_fetcher.py    # News API fetch & summarization
│   │   ├── user_profile.py    # Profile load/save
│   │   ├── config.py          # App configuration handling
├── resources/              # Icons, assets
├── data/                   # Local storage (JSON/SQLite)
├── requirements.txt        # Dependencies
└── README.md              # Project overview and setup
```

## Dependencies

- PySide6: UI framework
- requests: HTTP client
- python-dotenv: Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
