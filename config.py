import os

# Tema padrão
TEMA_PADRAO_ESCURO = False

# API do OpenRouter
OPENROUTER_API_KEY = "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"
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"

# Google Sheets
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1YnX5Lg7eW6AXwSdo73SIwvlxc4fITwUw5mTPHlspSqA/edit?gid=0"
CREDENTIALS_PATH = "credentials.json"

# ffmpeg
os.environ["PATH"] += os.pathsep + os.path.abspath("C:\\ffmpeg\\bin")
