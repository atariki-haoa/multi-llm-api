import os

def gemini_model_selector():
    return os.environ.get('GEMINI_MODEL') or 'gemini-2.5-flash'

def ngrok_model_selector():
    return os.environ.get('NGROK_MODEL') or 'gemini-2.5-flash'