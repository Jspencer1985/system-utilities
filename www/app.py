#!/usr/local/bin/python3.11
from flask import Flask, render_template, jsonify
import subprocess
import psutil
from datetime import datetime

app = Flask(__name__)

def get_wg_stats():
    """Get WireGuard Statistics"""
    try:
        result = subprocess.run(['wg', 'show', 'wg0'],
                              capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e.stderr}"
    except Exception as e:
        return f"Error getting WireGuard stats: {str(e)}"

def get_pf_stats():
    """Get Packet Filter Statistics"""
    try:
        result = subprocess.run(['pfctl', '-si'],
                              capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e.stderr}"
    except Exception as e:
        return f"Error getting PF stats: {str(e)}"

def get_system_stats():
    """Get System Statistics"""
    try:
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory()._asdict(),
            'disk': psutil.disk_usage('/')._asdict(),
            'network': psutil.net_io_counters()._asdict(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        return {
            'cpu_percent': 0,
            'memory': {'percent': 0},
            'disk': {'percent': 0},
            'network': {},
            'timestamp': f'Error: {str(e)}'
        }

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'wg': get_wg_stats(),
        'pf': get_pf_stats(),
        'system': get_system_stats()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

