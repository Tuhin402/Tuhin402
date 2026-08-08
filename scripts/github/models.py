from dataclasses import dataclass
from dataclasses import field


# ============================================================
# Language
# ============================================================

@dataclass
class GitHubLanguage:
    """
    Represents one programming language.
    """

    name: str
    bytes: int
    percentage: float = 0.0


# ============================================================
# Repository
# ============================================================

@dataclass
class GitHubRepository:
    """
    Represents one GitHub repository.
    """

    name: str
    description: str
    stars: int
    forks: int
    url: str

    languages: list[GitHubLanguage] = field(default_factory=list)


# ============================================================
# Contribution
# ============================================================

@dataclass
class GitHubContribution:
    """
    Represents one day
    in the GitHub contribution calendar.
    """

    date: str
    count: int
    level: int


# ============================================================
# Profile
# ============================================================

@dataclass
class GitHubProfile:
    """
    Represents the authenticated
    GitHub user.
    """

    username: str
    name: str
    bio: str

    avatar_url: str
    followers: int
    following: int

    repositories: list[GitHubRepository] = field(default_factory=list)
    contributions: list[GitHubContribution] = field(default_factory=list)
    languages: list[GitHubLanguage] = field(default_factory=list)


# ============================================================
# Statistics
# ============================================================

@dataclass
class GitHubStatistics:
    """
    Aggregated statistics
    computed from GitHub data.
    """

    # ---------------------------
    # Repository
    # ---------------------------

    total_repositories: int = 0
    total_stars: int = 0
    total_forks: int = 0
    average_stars: float = 0.0
    average_forks: float = 0.0
    most_starred_repository: str = ""
    most_forked_repository: str = ""

    # ---------------------------
    # Contributions
    # ---------------------------

    total_contributions: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    active_days: int = 0
    average_contributions_per_day: float = 0.0
    best_day: int = 0

    # ---------------------------
    # Languages
    # ---------------------------

    top_language: str = ""
    total_language_bytes: int = 0

    # ---------------------------
    # Social
    # ---------------------------

    total_followers: int = 0
    total_following: int = 0