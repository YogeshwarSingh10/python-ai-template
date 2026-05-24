import asyncio

from my_project.config import get_logger, setup_logging

setup_logging()

logger = get_logger(__name__)


async def main() -> None:
    logger.info("Starting...")


if __name__ == "__main__":
    asyncio.run(main())
