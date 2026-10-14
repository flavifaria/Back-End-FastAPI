# run_app.py
import uvicorn
import main  # Garante que o PyInstaller rastreie o main.py

if __name__ == "__main__":
    uvicorn.run(main.app, host="0.0.0.0", port=8000)