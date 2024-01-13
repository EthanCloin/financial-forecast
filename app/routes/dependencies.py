from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi.security import APIKeyCookie
from config import Settings

settings = Settings()
templates = Jinja2Blocks(directory=settings.TEMPLATE_DIR)

# using Depends(cookie_scheme) will check the request for a cookie named 'session'
# TODO: look into fastapi Session construct for managing user session
cookie_scheme = APIKeyCookie(name="session")
