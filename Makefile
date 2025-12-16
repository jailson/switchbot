.PHONY: start install test help scan press stop

# Use the venv python from the current directory
VENV := .venv/bin/python
VENV_WIN := .venv\Scripts\python.exe

help:
	@echo "Available commands:"
	@echo "  make start     - Start the API server"
	@echo "  make test      - Test the API with curl"
	@echo "  make install   - Install dependencies"
	@echo "  make scan      - Run the BLE SwitchBot scanner"
	@echo "  make press     - Press a SwitchBot (BOT_MAC required)"
	@echo "  make stop      - Stop the running API server"

install:
	$(VENV) -m pip install -r requirements.txt

start:
	$(VENV) src/api.py

test:
ifndef BOT_MAC
	$(error BOT_MAC is required. Usage: make test BOT_MAC=XX:XX:XX:XX:XX:XX)
endif
	curl -X POST http://localhost:5000/devices/$(BOT_MAC)/press

stop:
	pkill -f "python src/api.py" 2>/dev/null || true
	sleep 1
	@echo "API stopped"

scan:
	$(VENV) src/scan.py

press:
ifndef BOT_MAC
	$(error BOT_MAC is required. Usage: make press BOT_MAC=XX:XX:XX:XX:XX:XX)
endif
	$(VENV) src/press.py $(BOT_MAC)

.DEFAULT_GOAL := help
