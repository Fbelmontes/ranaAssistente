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
