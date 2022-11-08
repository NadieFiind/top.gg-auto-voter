def _vote() -> None:
    run_job()
    scheduler.enter(60 * 60 * 12 + 60, 1, _vote)
    Logger("vote").info(
        "Voting will start again in 12 hours. Please don't exit the application."
    )


if __name__ == "__main__":
    import time
    import sched
    from app.utils import Logger
    from job import main as run_job

    scheduler = sched.scheduler(time.time, time.sleep)

    try:
        _vote()
        scheduler.run()
    except KeyboardInterrupt:
        pass
