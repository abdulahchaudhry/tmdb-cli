import os
import sys
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

console = Console()


def search_movie(title):
    """Ask TMDB for movies matching a title."""
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": title}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json().get("results", [])


def print_movie_list(results):
    """Print a numbered table of matching movies."""

    console.print("\n📽 [bold]Multiple matches found. Pick one:[/bold]\n")

    table = Table()
    table.add_column("#", justify="center")
    table.add_column("Title")
    table.add_column("Year", justify="center")

    for i, movie in enumerate(results, start=1):
        title = movie.get("title", "Unknown")
        year = (movie.get("release_date") or "????")[:4]

        table.add_row(str(i), title, year)

    console.print(table)
    console.print()


def print_movie_details(movie):
    """Print one movie's full details in a table."""

    table = Table(title="🎬 Movie Details")

    table.add_column("Field", style="bold")
    table.add_column("Details")

    table.add_row("Title", movie.get("title", "N/A"))
    table.add_row("Release", movie.get("release_date", "N/A"))
    table.add_row("Rating", f"{movie.get('vote_average', 'N/A')} / 10")
    table.add_row("Votes", str(movie.get("vote_count", "N/A")))
    table.add_row(
        "Language",
        movie.get("original_language", "N/A").upper()
    )
    table.add_row("Overview", movie.get("overview", "No overview."))

    console.print()
    console.print(table)
    console.print()


def ask_user_choice(max_num):
    """Keep asking until the user gives a valid number, or quits."""

    while True:
        choice = input(
            f" Enter a number (1-{max_num}) or 'q' to quit: "
        ).strip()

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


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "<movie title>"')
        sys.exit(1)

    if not API_KEY:
        print(" ❌ Missing TMDB_API_KEY. Check your .env file.")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    print(f"\n🔍 Searching for: {query}")

    try:
        results = search_movie(query)
    except requests.RequestException as e:
        print(f" ❌ Network error: {e}")
        sys.exit(1)

    if not results:
        print(" No movies found.")
        return

    # Case 1: only one match → skip the menu, show details directly
    if len(results) == 1:
        print_movie_details(results[0])
        return

    # Case 2: multiple matches → show list, ask, then show the chosen one
    print_movie_list(results)

    choice = ask_user_choice(len(results))
    selected = results[choice - 1]

    print_movie_details(selected)


if __name__ == "__main__":
    main()

