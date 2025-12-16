import asyncio
import subprocess
import sys
import os
from flask import Flask, jsonify, request
import logging
from scan import scan_switchbots

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Build cross-platform paths for the press.py script
if sys.platform == "win32":
    VENV_PYTHON = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "python.exe")
else:
    VENV_PYTHON = os.path.join(PROJECT_ROOT, ".venv", "bin", "python")

PRESS_SCRIPT = os.path.join(SCRIPT_DIR, "press.py")

@app.route('/devices', methods=['GET'])
def list_devices():
    """List nearby SwitchBot devices"""
    try:
        logger.info("SwitchBot scan request received")
        devices = asyncio.run(scan_switchbots(timeout=5.0))
        
        logger.info(f"SwitchBot scan complete: found {len(devices)} devices")
        return jsonify({
            'status': 'success',
            'devices': devices,
            'count': len(devices)
        }), 200
    except Exception as e:
        logger.error(f"SwitchBot scan failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Scan failed',
            'error': str(e)
        }), 500

@app.route('/devices/<mac>/press', methods=['POST'])
def press_bot(mac):
    """Trigger the SwitchBot press via HTTP POST with MAC address in path"""
    try:
        logger.info(f"Press request received for MAC: {mac}")
        # Run the press command with the MAC as an argument
        result = subprocess.run(
            [VENV_PYTHON, PRESS_SCRIPT, mac],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            logger.info(f"Press successful for {mac}")
            return jsonify({
                'status': 'success',
                'message': f'SwitchBot ({mac}) pressed successfully'
            }), 200
        else:
            logger.error(f"Press failed for {mac}: {result.stderr}")
            return jsonify({
                'status': 'error',
                'message': f'Failed to press SwitchBot ({mac})',
                'error': result.stderr
            }), 500
    except subprocess.TimeoutExpired:
        logger.error(f"Press command timed out for {mac}")
        return jsonify({
            'status': 'error',
            'message': 'Request timed out'
        }), 408
    except Exception as e:
        logger.error(f"Unexpected error for {mac}: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Unexpected error',
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SwitchBot API'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
