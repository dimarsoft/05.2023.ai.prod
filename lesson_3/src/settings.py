import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env_dev')

APILAYER_APY_KEY = os.getenv("APILAYER_APY_KEY")
