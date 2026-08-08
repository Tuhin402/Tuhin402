import requests

from scripts.github.auth import GitHubAuth

from scripts.utils.logger import logger


class GitHubFetcher:
    """
    Executes GraphQL requests
    against GitHub.
    """

    API_URL = "https://api.github.com/graphql"

    def __init__(self):

        self.auth = GitHubAuth()

    # --------------------------------------------------

    def execute(self, query, variables=None):

        logger.info("Sending GraphQL request...")

        payload = {

            "query": query,

            "variables": variables or {},

        }

        response = requests.post(

            self.API_URL,

            headers=self.auth.headers(),

            json=payload,

            timeout=30,

        )

        if response.status_code != 200:

            raise RuntimeError(

                f"GitHub API Error "
                f"{response.status_code}\n"
                f"{response.text}"
            )

        logger.info("GitHub response received.")

        return response.json()