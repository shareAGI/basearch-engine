from typing import List
import requests
from app.core.config import settings
from logging import getLogger

logger = getLogger(__name__)

class Vectorizer:
    def __init__(self):
        self.api_url = settings.EMBEDDING_API_URL
        self.api_key = settings.EMBEDDING_API_KEY
        self.embedding_model = settings.EMBEDDING_MODEL

    def vectorize(self, text: str) -> List[float]:
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', '')
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.api_key}',
            'content-type': 'application/json',
        }
        data = {
            "model": self.embedding_model,
            "input": text,
        }
        try:
            logger.info(f"text len: {len(text)}, vectorizing...")
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            # breakpoint() 
            embedding = response.json()['data'][0]['embedding']
            return embedding
        except requests.exceptions.HTTPError as err:
            try:
                logger.error(f"vectorize error, re-vectorizing...")
                data = {
                    "model": self.embedding_model,
                    "input": text[:300],
                }
                response = requests.post(self.api_url, headers=headers, json=data)
                response.raise_for_status()
                # breakpoint()
                embedding = response.json()['data'][0]['embedding']
                return embedding
            except requests.exceptions.HTTPError as err:
                logger.error(f"HTTP error occurred: {err}")
                raise err

vectorizer = Vectorizer()


def get_embedding_vector(text: str) -> list:
    return vectorizer.vectorize(text)
