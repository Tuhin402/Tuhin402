import os

from dotenv import load_dotenv

from scripts.utils.logger import logger


class GitHubAuth:
    """
    Responsible for loading and validating
    GitHub authentication credentials.
    """

    def __init__(self):

        load_dotenv()

        self.token = os.getenv("GITHUB_TOKEN")

    # --------------------------------------------------

    def validate(self):

        if not self.token:

            raise RuntimeError(

                "Missing GITHUB_TOKEN inside .env"

            )

        logger.info(

            "GitHub token loaded successfully."

        )

        return True

    # --------------------------------------------------

    def headers(self):

        self.validate()

        return {

            "Authorization": f"Bearer {self.token}",

            "Content-Type": "application/json",

            "Accept": "application/vnd.github+json",

        }