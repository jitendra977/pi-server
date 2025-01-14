# signals.py
import signal
import sys

def signal_handler(sig, frame):
    print("Gracefully exiting...")
    sys.exit(0)

def setup_signal_handlers():
    signal.signal(signal.SIGINT, signal_handler)