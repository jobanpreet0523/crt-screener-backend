# cron_scan.py
from batch_scan import run_nse200_scan

if __name__ == "__main__":
    run_nse200_scan()
    print("✅ NSE 200 nightly scan completed")
