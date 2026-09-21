import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def search_movie(title):
    """Ask TMDB for movies matching a title."""
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": title}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json().get("results", [])


def print_movie_list(results):
    """Print a numbered list of movies — just titles and years."""
    print("\n📽  Multiple matches found. Pick one:\n")
    for i, movie in enumerate(results, start=1):
        title = movie.get("title", "Unknown")
        year = (movie.get("release_date") or "????")[:4]  # take first 4 chars
        print(f"  {i}. {title} ({year})")
    print()


def print_movie_details(movie):
    """Pretty-print one movie's full details."""
    print("\n" + "=" * 60)
    print(f"🎬 Title:    {movie.get('title')}")
    print(f"📅 Release:  {movie.get('release_date', 'N/A')}")
    print(f"⭐ Rating:   {movie.get('vote_average')} / 10")
    print(f"🗳  Votes:    {movie.get('vote_count')}")
    print(f"🌐 Language: {movie.get('original_language', '').upper()}")
    print(f"📝 Overview: {movie.get('overview', 'No overview.')}")
    print("=" * 60 + "\n")


def ask_user_choice(max_num):
    """Keep asking until the user gives a valid number, or quits."""
    while True:
        choice = input(f"  Enter a number (1-{max_num}) or 'q' to quit: ").strip()

        if choice.lower() == "q":
            print("  👋 Bye!")
            sys.exit(0)

        # Make sure it's actually a number
        if not choice.isdigit():
            print("  ❌ Please enter a number.")
            continue

        num = int(choice)
        if 1 <= num <= max_num:
            return num

        print(f"  ❌ Pick a number between 1 and {max_num}.")


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "<movie title>"')
        sys.exit(1)

    if not API_KEY:
        print("  ❌ Missing TMDB_API_KEY. Check your .env file.")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"\n🔍 Searching for: {query}")

    try:
        results = search_movie(query)
    except requests.RequestException as e:
        print(f"  ❌ Network error: {e}")
        sys.exit(1)

    if not results:
        print("  No movies found.")
        return

    # Case 1: only one match → skip the menu, show details directly
    if len(results) == 1:
        print_movie_details(results[0])
        return

    # Case 2: multiple matches → show list, ask, then show the chosen one
    print_movie_list(results)
    choice = ask_user_choice(len(results))
    selected = results[choice - 1]  # lists are 0-indexed, humans count from 1
    print_movie_details(selected)


if __name__ == "__main__":
    main()