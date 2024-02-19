import logging

import pycountry


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_primary_language(country: str) -> str | None:
    country_obj = pycountry.countries.search_fuzzy(country)
    try:
        country_code = country_obj[0].alpha_2
        language = pycountry.languages.get(alpha_2=country_code)
        return language.alpha_2
    except AttributeError:
        logger.warning(f"Country name '{country}' not found.")
