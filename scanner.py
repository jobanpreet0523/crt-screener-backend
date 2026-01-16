from crt_logic import classify_crt

def run_crt_scan(tf="daily"):
    return {
        "timeframe": tf,
        "message": "Scanner running",
        "results": []
    }
