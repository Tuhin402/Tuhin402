from collections import defaultdict
from scripts.github.models import (GitHubLanguage, GitHubProfile, GitHubStatistics,)
from scripts.utils.logger import logger


class GitHubStatisticsEngine:
    """
    Computes analytics from a GitHubProfile.
    """

    # ----------------------------------------------
    def __init__(self):
        self.statistics = GitHubStatistics()


    # ----------------------------------------------
    def repository_statistics(self, profile: GitHubProfile,):

        logger.info("Calculating repository statistics...")
        repositories = profile.repositories
        stats = self.statistics
        stats.total_repositories = len(repositories)
        stats.total_stars = sum(
            repo.stars
            for repo
            in repositories
        )

        stats.total_forks = sum(
            repo.forks
            for repo
            in repositories
        )

        if repositories:

            stats.average_stars = round(stats.total_stars / len(repositories), 2,)
            stats.average_forks = round(stats.total_forks / len(repositories), 2,)
            most_starred = max(repositories, key=lambda r: r.stars,)
            stats.most_starred_repository = (most_starred.name)
            most_forked = max(repositories, key=lambda r: r.forks,)
            stats.most_forked_repository = (most_forked.name)

        logger.info("Repository statistics complete.")


    # ----------------------------------------------    
    def language_statistics(self, profile: GitHubProfile,):

        logger.info("Calculating language statistics...")
        stats = self.statistics
        language_totals = defaultdict(int)
        total_bytes = 0

        for repository in profile.repositories:
            for language in repository.languages:
                language_totals[language.name] += language.bytes
                total_bytes += language.bytes

        if total_bytes == 0:
            logger.warning("No language statistics found.")
            return

        profile.languages.clear()

        for name, size in sorted(
            language_totals.items(),
            key=lambda item: item[1],
            reverse=True,
        ):

            percentage = (size / total_bytes) * 100

            profile.languages.append(
                GitHubLanguage(
                    name=name,
                    bytes=size,
                    percentage=percentage,
                )
            )

        stats.total_language_bytes = total_bytes
        stats.top_language = profile.languages[0].name
        logger.info("Language statistics complete.")


    #-----------------------------------------------    
    def contribution_statistics(self, profile: GitHubProfile,):

        logger.info("Calculating contribution statistics...")
        stats = self.statistics
        contributions = sorted(profile.contributions, key=lambda day: day.date,)

        if not contributions:
            logger.warning("No contribution data available.")
            return

        # ----------------------------------------
        # Totals
        # ----------------------------------------

        stats.total_contributions = sum(
            day.count
            for day
            in contributions
        )

        stats.active_days = sum(
            1
            for day
            in contributions
            if day.count > 0
        )

        stats.best_day = max(
            day.count
            for day
            in contributions
        )

        if stats.active_days:
            stats.average_contributions_per_day = round(stats.total_contributions / stats.active_days, 2,)

        # ----------------------------------------
        # Streaks
        # ----------------------------------------

        longest = 0
        current = 0
        running = 0

        # Longest streak

        for day in contributions:
            if day.count > 0:
                running += 1
                longest = max(longest, running,)

            else:
                running = 0

        # Current streak
        # Work backwards from today

        for day in reversed(contributions):
            if day.count > 0:
                current += 1
            else:
                break

        stats.longest_streak = longest
        stats.current_streak = current

        logger.info("Contribution statistics complete.")


    #-----------------------------------------------  
    def social_statistics(self, profile: GitHubProfile,):

        logger.info("Calculating social statistics...")
        stats = self.statistics
        stats.total_followers = profile.followers
        stats.total_following = profile.following
        logger.info("Social statistics complete.")


    #----------------------------------------------- 
    def compute(self, profile: GitHubProfile,) -> GitHubStatistics:

        logger.info("Computing GitHub statistics...")

        # Reset statistics for repeated calls
        self.statistics = GitHubStatistics()
        self.repository_statistics(profile)
        self.language_statistics(profile)
        self.contribution_statistics(profile)
        self.social_statistics(profile)

        logger.info("GitHub statistics complete.")
        return self.statistics