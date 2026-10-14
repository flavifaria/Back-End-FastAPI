# core/paths.py
import sys
from pathlib import Path

def get_bundle_dir() -> Path:
    """Retorna o diretório onde arquivos estáticos empacotados estão (ex: index.html, static/)."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent

def get_executable_dir() -> Path:
    """Retorna a pasta real no Linux onde o binário está rodando (ideal para o banco .db e .env)."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent

BUNDLE_DIR = get_bundle_dir()
EXEC_DIR = get_executable_dir()