from my_project import config

config.setup()

logger = config.get_logger(__name__)


def main() -> None:
    logger.info("Starting...")


if __name__ == "__main__":
    main()
