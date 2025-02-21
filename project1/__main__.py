from project1.parcer import main
from project1.logger.logger_config import setup_logger

logger = setup_logger("------START------")
logger.debug("------START------")


app = main()


if __name__ == '__main__':
	app