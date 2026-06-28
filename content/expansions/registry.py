"""Merged registry of all editorial expansions."""

from content.expansions.articles import CORE_ARTICLE_EXPANSIONS
from content.expansions.batch4_remaining import BATCH4_ARTICLE_EXPANSIONS
from content.expansions.priority_batch import PRIORITY_ARTICLE_EXPANSIONS
from content.expansions.side_hustle import SIDE_HUSTLE_EXPANSION

ALL_ARTICLE_EXPANSIONS: dict[str, dict] = {
    **CORE_ARTICLE_EXPANSIONS,
    **PRIORITY_ARTICLE_EXPANSIONS,
    **BATCH4_ARTICLE_EXPANSIONS,
    **SIDE_HUSTLE_EXPANSION,
}
