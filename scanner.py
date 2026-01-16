from crt_logic import classify_crt

def run_crt_scan(tf="weekly"):
    return {
        "timeframe": tf,
        "status": "Scanner working",
        "data": []
    }
