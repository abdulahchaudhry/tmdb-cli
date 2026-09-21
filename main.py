import os
import sys
import requests
from dotenv import load_dotenv

# 1. Load the .env file so os.getenv() can find our key
load_dotenv()

# 2. Grab the API key from environment variables
API_KEY = os.getenv("TMDB_API_KEY")

# 3. Base URL for TMDB's search endpoint
BASE_URL = "https://api.themoviedb.org/3"


def search_movie(title):
    """Ask TMDB for movies matching a title."""
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title,
    }
    # Make the actual network request
    response = requests.get(url, params=params, timeout=10)

    # If something went wrong, raise an error
    response.raise_for_status()

    # Convert JSON text response into a Python dictionary
    data = response.json()
    return data.get("results", [])


def print_movie(movie):
    """Pretty-print one movie's details."""
    print("-" * 50)
    print(f"🎬 Title:       {movie.get('title')}")
    print(f"📅 Release:     {movie.get('release_date', 'N/A')}")
    print(f"⭐ Rating:      {movie.get('vote_average')} / 10")
    print(f"📝 Overview:    {movie.get('overview', 'No overview.')}")
    print("-" * 50)


def main():
    # sys.argv is the list of words typed in terminal
    # e.g. `python main.py Inception` → ['main.py', 'Inception']
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<movie title>\"")
        sys.exit(1)

    if not API_KEY:
        print("❌ Missing TMDB_API_KEY. Check your .env file.")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"\n🔍 Searching for: {query}\n")

    try:
        results = search_movie(query)
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)

    if not results:
        print("No movies found.")
        return

    # Show top 5 results
    for movie in results[:5]:
        print_movie(movie)


# This guard means: only run main() if this file is executed directly
if __name__ == "__main__":
    main()