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
