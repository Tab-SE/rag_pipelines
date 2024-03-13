import os
from dotenv import load_dotenv

from scripts.query import query

load_dotenv()
env_vars = os.environ

DOMAIN = env_vars['TABLEAU_DOMAIN']
API = env_vars['TABLEAU_API']
SITE = env_vars['TABLEAU_SITE']
CLIENT_ID = env_vars['TABLEAU_JWT_CLIENT_ID']
SECRET = env_vars['TABLEAU_REST_JWT_SECRET']
SECRET_ID = env_vars['TABLEAU_REST_JWT_SECRET_ID']
USER = env_vars['TABLEAU_USER']
OPENAI_API_KEY = env_vars['OPENAI_API_KEY']
MODEL = env_vars['MODEL']
PINECONE_API_KEY = env_vars['PINECONE_API_KEY']
PINECONE_ENVIRONMENT = env_vars['PINECONE_ENVIRONMENT']
PINECONE_INDEX_NAME = env_vars['PINECONE_INDEX_NAME']

def main():
  insights = query({
    'DOMAIN': DOMAIN,
    'API': API,
    'SITE': SITE,
    'CLIENT_ID': CLIENT_ID,
    'SECRET': SECRET,
    'SECRET_ID': SECRET_ID,
    'USER': USER
  })
  return


if __name__ == "__main__":
  main()
