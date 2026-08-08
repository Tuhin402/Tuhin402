from scripts.github.models import (
    GitHubContribution,
    GitHubLanguage,
    GitHubProfile,
    GitHubRepository,
)

from scripts.utils.logger import logger


class GitHubParser:
    """
    Converts GitHub GraphQL JSON
    into internal models.
    """

    # --------------------------------------------------

    def parse_profile(

        self,

        payload,

    ):

        logger.info(

            "Parsing GitHub profile..."

        )

        viewer = payload["data"]["viewer"]

        return GitHubProfile(

            username=viewer["login"],

            name=viewer["name"] or "",

            bio=viewer["bio"] or "",

            avatar_url=viewer["avatarUrl"],

            followers=viewer["followers"]["totalCount"],

            following=viewer["following"]["totalCount"],

        )

    # --------------------------------------------------

    def parse_repositories(

        self,

        payload,

    ):

        logger.info(

            "Parsing repositories..."

        )

        repositories = []

        nodes = payload["data"]["viewer"]["repositories"]["nodes"]

        for repo in nodes:

            repository = GitHubRepository(

                name=repo["name"],

                description=repo["description"] or "",

                stars=repo["stargazerCount"],

                forks=repo["forkCount"],

                url=repo["url"],

            )

            for language in repo["languages"]["edges"]:

                repository.languages.append(

                    GitHubLanguage(

                        name=language["node"]["name"],

                        bytes=language["size"],

                    )

                )

            repositories.append(repository)

        logger.info(

            f"Repositories Parsed : {len(repositories)}"

        )

        return repositories

    # --------------------------------------------------

    def parse_contributions(

        self,

        payload,

    ):

        logger.info(

            "Parsing contributions..."

        )

        contributions = []

        weeks = payload["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]["weeks"]

        level_map = {

            "NONE": 0,

            "FIRST_QUARTILE": 1,

            "SECOND_QUARTILE": 2,

            "THIRD_QUARTILE": 3,

            "FOURTH_QUARTILE": 4,

        }

        for week in weeks:

            for day in week["contributionDays"]:

                contributions.append(

                    GitHubContribution(

                        date=day["date"],

                        count=day["contributionCount"],

                        level=level_map.get(

                            day["contributionLevel"],

                            0,

                        ),

                    )

                )

        logger.info(

            f"Contribution Days : {len(contributions)}"

        )

        return contributions