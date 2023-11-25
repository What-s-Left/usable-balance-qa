import os
from dotenv import find_dotenv, load_dotenv
import contextvars

context_external_user = contextvars.ContextVar("external_user", default=None)
context_external_user_token = contextvars.ContextVar(
    "external_user_token", default=None
)
context_user = contextvars.ContextVar("user", default=None)

global_external_user = None

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)