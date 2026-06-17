"""900+ word editorial expansions for thin core articles."""

from content.expansions._helpers import (
    expansion_salary_words,
    expansion_word_count,
    resolve_slugs,
)
from content.expansions.articles import CORE_ARTICLE_EXPANSIONS

__all__ = [
    "CORE_ARTICLE_EXPANSIONS",
    "expansion_word_count",
    "expansion_salary_words",
    "resolve_slugs",
]
