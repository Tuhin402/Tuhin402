from abc import ABC
from abc import abstractmethod

from scripts.cache.manager import CacheManager

from scripts.github.fetcher import GitHubFetcher
from scripts.github.graphql import GitHubQueries
from scripts.github.parser import GitHubParser

from scripts.utils.logger import logger


class BaseGenerator(ABC):
    """
    Base class for every generator.

    Provides common GitHub loading helpers so
    individual generators only focus on rendering.
    """

    def __init__(self):

        self.fetcher = GitHubFetcher()
        self.cache = CacheManager()
        self.parser = GitHubParser()

    # --------------------------------------------------

    @abstractmethod
    def generate(self):

        raise NotImplementedError

    # --------------------------------------------------

    def load_profile(self, repositories=False, contributions=False,):

        """
        Loads the authenticated GitHub profile.

        Optional flags determine whether repositories
        and contributions should also be fetched.
        """

        logger.info("Loading GitHub profile...")

        profile_payload = self.cache.get_or_fetch(
            "profile",
            lambda: self.fetcher.execute(GitHubQueries.VIEWER_PROFILE,),
        )
        profile = self.parser.parse_profile(profile_payload,)

        # ------------------------------------------
        # Repositories
        # ------------------------------------------

        if repositories:

            repositories_payload = self.cache.get_or_fetch(
                "repositories",
                lambda: self.fetcher.execute(GitHubQueries.REPOSITORIES,),
            )
            profile.repositories = (self.parser.parse_repositories(repositories_payload,))

        # ------------------------------------------
        # Contributions
        # ------------------------------------------

        if contributions:

            contributions_payload = self.cache.get_or_fetch(
                "contributions",
                lambda: self.fetcher.execute(GitHubQueries.CONTRIBUTIONS,),
            )
            profile.contributions = (self.parser.parse_contributions(contributions_payload,))

        return profile