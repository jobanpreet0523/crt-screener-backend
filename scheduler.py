from apscheduler.schedulers.background import BackgroundScheduler
from batch_scan import scan_nse_200

def start_scheduler():
    scheduler = BackgroundScheduler()

    # Runs every night at 2 AM IST
    scheduler.add_job(
        scan_nse_200,
        trigger="cron",
        hour=2,
        minute=0
    )

    scheduler.start()
