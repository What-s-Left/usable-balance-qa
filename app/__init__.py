import os
from dotenv import find_dotenv, load_dotenv
import contextvars

context_external_user = contextvars.ContextVar("external_user")
context_external_user_token = contextvars.ContextVar("external_user_token")

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
