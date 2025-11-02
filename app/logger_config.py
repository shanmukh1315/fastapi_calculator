import logging
from pathlib import Path


def configure_logger():
    # ensure a logs dir exists (optional)
    Path("logs").mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ],
    )
    return logging.getLogger("fastapi_calculator")
