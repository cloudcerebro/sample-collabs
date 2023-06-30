import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tools.Unsplash.unsplash_tool import UnsplashImageSearchTool

search = UnsplashImageSearchTool(api_key='Ubw469EoL6raUG4pjEbUatN1tSYkK4NtYPEkdp4SajY')

output = search.run("cute cat")
print(output)