"""Util that calls Unsplash Search.

Requires setup: Get API key from https://unsplash.com/developers
"""

from typing import Dict
from pydantic import BaseModel, Extra, Field
import requests

class UnsplashSearchAPIWrapper(BaseModel):
    """Wrapper for Unsplash Search API.

    Requires an API key setup
    """
    api_key: str

    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid

    def run(self, query: str) -> str:
        """Run query through Unsplash and return first image URL."""
        url = f"https://api.unsplash.com/search/photos?query={query}"
        headers = {"Authorization": f"Client-ID {self.api_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        if not data["results"]:
            raise ValueError("No images found for the given query.")
        
        # Return the URL of the first image
        return data["results"][0]["urls"]
