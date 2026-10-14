# Nome do binário final
APP_NAME = sistema_backend
PYTHON = ./venv/bin/python
PIP = ./venv/bin/pip
PYINSTALLER = ./venv/bin/pyinstaller

.PHONY: all setup clean run build

all: setup clean build

# 1. Cria o venv e instala o requirements.txt
setup:
	@echo "🔧 Configurando ambiente virtual e dependências..."
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# 2. Limpa todos os __pycache__ e builds anteriores
clean:
	@echo "🧹 Limpando arquivos temporários e caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.spec

# 3. Roda em modo de desenvolvimento
run:
	./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 4. Compila para um executável único autônomo
build: clean
	@echo "🚀 Compilando binário..."
	$(PYINSTALLER) --noconfirm --onefile --clean \
		--name "$(APP_NAME)" \
		--add-data "static:static" \
		--add-data "index.html:." \
		--hidden-import="passlib.handlers.bcrypt" \
		--hidden-import="bcrypt" \
		--hidden-import="multipart" \
		--hidden-import="sqlalchemy.sql.default_comparator" \
		--hidden-import="uvicorn.logging" \
		--hidden-import="uvicorn.loops.auto" \
		--hidden-import="uvicorn.protocols.http.auto" \
		--hidden-import="uvicorn.protocols.websockets.auto" \
		--hidden-import="uvicorn.lifespan.on" \
		--collect-submodules="passlib" \
		--collect-submodules="modules" \
		--collect-submodules="core" \
		run_app.py
	@echo "✅ Binário gerado em: dist/$(APP_NAME)"