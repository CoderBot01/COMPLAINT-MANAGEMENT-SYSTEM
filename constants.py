from os import getenv
from dotenv import load_dotenv


load_dotenv()

# Variables
DB_URL = getenv("DB_URL")
COS_ENDPOINT = getenv("COS_ENDPOINT")
COS_API_KEY_ID = getenv("COS_API_KEY_ID")
COS_RESOURCE_CRN = getenv("COS_RESOURCE_CRN")
COS_BUCKET_NAME = getenv("COS_BUCKET_NAME")
AUTH_ADMIN_CODES = list(getenv("AUTH_ADMIN_CODES", "admin").split(","))