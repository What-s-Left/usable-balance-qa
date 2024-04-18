import uvicorn
import os
from os import environ as env
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

if __name__ == "__main__":
    uvicorn.run(
        "app.www:www",
        host="0.0.0.0",
        port=8080,
        workers=4,
        log_level="info",
        reload=True,
        #ssl_keyfile=f"app/certs/{get_secret('SSL_KEYFILE')}",
        #ssl_certfile=f"app/certs/{get_secret('SSL_CERTFILE')}"
    )