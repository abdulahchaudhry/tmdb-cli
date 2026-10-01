import os
import sys

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
MAX_RESULTS = 10

console = Console()


class InvalidAPIKeyError(Exception):
    """Raised when TMDB rejects the API key (HTTP 401)."""


def search_movie(title):
    """Ask TMDB for movies matching a title.

    Returns at most MAX_RESULTS movies, most popular first.
    """
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": title}

    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 401:
        raise InvalidAPIKeyError()
    response.raise_for_status()

    results = response.json().get("results", [])
    results.sort(key=lambda m: m.get("popularity") or 0, reverse=True)
    return results[:MAX_RESULTS]


def print_movie_list(results):
    """Print a numbered table of matching movies."""
    console.print("\n📽 [bold]Multiple matches found. Pick one:[/bold]\n")

    table = Table()
    table.add_column("#", justify="center")
    table.add_column("Title")
    table.add_column("Year", justify="center")

    for i, movie in enumerate(results, start=1):
        title = movie.get("title") or "Unknown"
        year = (movie.get("release_date") or "????")[:4]
        table.add_row(str(i), title, year)

    console.print(table)
    console.print()


def print_movie_details(movie):
    """Print one movie's full details in a table."""
    table = Table(title="🎬 Movie Details")
    table.add_column("Field", style="bold")
    table.add_column("Details")

    table.add_row("Title", movie.get("title") or "N/A")
    table.add_row("Release", movie.get("release_date") or "N/A")
    table.add_row("Rating", f"{movie.get('vote_average', 'N/A')} / 10")
    table.add_row("Votes", str(movie.get("vote_count", "N/A")))
    table.add_row("Language", (movie.get("original_language") or "N/A").upper())
    table.add_row("Overview", movie.get("overview") or "No overview.")

    console.print()
    console.print(table)
    console.print()


def ask_user_choice(max_num):
    """Keep asking until the user gives a valid number, or quits."""
    while True:
        choice = input(f" Enter a number (1-{max_num}) or 'q' to quit: ").strip()

        if choice.lower() == "q":
            print(" 👋 Bye!")
            sys.exit(0)

        if not choice.isdigit():
            print(" ❌ Please enter a number.")
            continue

        num = int(choice)
        if 1 <= num <= max_num:
            return num

        print(f" ❌ Pick a number between 1 and {max_num}.")


def get_query():
    """Use the command-line title if given, otherwise ask for one."""
    if len(sys.argv) >= 2:
        return " ".join(sys.argv[1:]).strip()

    while True:
        query = input("\nEnter movie name: ").strip()
        if query:
            return query
        print(" ❌ Movie name can't be empty.")


def main():
    if not API_KEY:
        print(" ❌ Missing TMDB_API_KEY. Run `python setup.py` to set it up.")
        sys.exit(1)

    query = get_query()
    print(f"\n🔍 Searching for: {query}")

    # Note: we never print the raw exception, because requests includes the
    # full URL (and therefore the API key) in its error messages.
    try:
        results = search_movie(query)
    except InvalidAPIKeyError:
        print(" ❌ Invalid TMDB API key. Run `python setup.py` to enter a new one.")
        sys.exit(1)
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        if status == 429:
            print(" ❌ Too many requests. Wait a moment and try again.")
        else:
            print(f" ❌ TMDB returned an error (HTTP {status}). Try again later.")
        sys.exit(1)
    except requests.RequestException:
        print(" ❌ Couldn't reach TMDB. Check your internet connection.")
        sys.exit(1)

    if not results:
        print(" No movies found.")
        return

    # Case 1: only one match -> skip the menu, show details directly
    if len(results) == 1:
        print_movie_details(results[0])
        return

    # Case 2: multiple matches -> show list, ask, then show the chosen one
    print_movie_list(results)
    choice = ask_user_choice(len(results))
    print_movie_details(results[choice - 1])


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n 👋 Bye!")
        sys.exit(0)
