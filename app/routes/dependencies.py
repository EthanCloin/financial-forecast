from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi.security import APIKeyCookie
from config import Settings

settings = Settings()
templates = Jinja2Blocks(directory=settings.TEMPLATE_DIR)

# using Depends(cookie_scheme) will check the request for a cookie named 'session'
# TODO: look into fastapi Session construct for managing user session
cookie_scheme = APIKeyCookie(name="session")


def dollars_to_cents(currency: str) -> int:
    cent_string = currency.replace("$", "").replace(",", "").replace(".", "").strip()
    return int(cent_string)


def cents_to_dollars(cent_val: int) -> str:
    """adds '$' commas and period to provided cent value"""
    cents = str(cent_val)[-2::]
    dollars = str(cent_val)[0:-2]
    formatted = ""

    for i, c in enumerate(dollars[::-1]):
        if i % 3 == 0 and i != 0:
            formatted += ","
        formatted += c
    return f"${formatted[::-1]}.{cents}"
