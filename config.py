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
