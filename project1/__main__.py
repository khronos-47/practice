from .parcer import main

from logging import getLogger
from uvicorn import run

logger = getLogger(__name__)


app = main()


if __name__ == '__main__':
	run(
        ".__main__:app",
        reload=True,
        reload_dirs=["project1"],
        log_level="debug"
    )