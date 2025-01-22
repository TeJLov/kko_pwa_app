import sys
import os
import signal
import uvicorn

# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def signal_handler(_, __):
    """
    Обработчик сигнала завершения работы
    """
    print("\nЗавершение работы сервера...")
    sys.exit(0)

if __name__ == "__main__":
    # Регистрируем обработчик сигнала SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    uvicorn.run("backend.main:app",
                host="127.0.0.1",
                port=8000,
                reload=True)
