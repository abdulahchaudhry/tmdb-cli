# 🎬 TMDB CLI

A simple command-line movie search tool built with Python and the **TMDB API**.

Search for movies directly from your terminal, pick from the top matches, and view detailed movie information in a clean table.

## ✨ Features

- 🔎 Search movies by title
- 📋 Top 10 matches shown in a table, sorted by popularity
- 🎯 Select a movie interactively
- ⭐ Rating, 📅 release date, 🗳 vote count, 🌐 original language, 📝 overview
- 🚀 One-command setup: installs dependencies, asks for your API key, and verifies it
- 🔐 API key stored locally in `.env` (git-ignored, never committed)
- 🛑 Clear error messages for invalid API key, rate limits, and network problems
- ⚡ Simple and lightweight

## 🛠️ Built With

- **Python**
- **Requests** — API requests
- **python-dotenv** — Environment variable management
- **Rich** — Terminal tables and formatting
- **TMDB API** — Movie data

## 🚀 Quick Start

### Windows
```bash
git clone https://github.com/abdulahchaudhry/tmdb-cli.git
cd tmdb-cli
python setup.py
```
### Linux/MacOS
```bash
git clone https://github.com/abdulahchaudhry/tmdb-cli.git
cd tmdb-cli
```
```bash
# Creating a virtual env
python -m venv .venv          # use python3 if python not found
source .venv/bin/activate 
```
```bash  
# use python3 if python not found    
python setup.py
```

On the first run, `setup.py` will:

1. Install the dependencies from `requirements.txt` (only if something is missing)
2. Ask for your TMDB API key and check that TMDB accepts it
3. Save the key to `.env`
4. Start the app and prompt: `Enter movie name:`

On later runs, `python setup.py` skips straight to the prompt. It only asks for a key again if the saved one is missing or rejected.

### 🔑 Getting a TMDB API key

Create a free account on [The Movie Database](https://www.themoviedb.org/), then go to **Settings → API** and copy the **API Key (v3)**. You'll paste it when `setup.py` asks.


Activate the venv again (the `source` line) in any new terminal before running the app.

## 💻 Usage

Run the app and type a title when prompted:

```bash
python main.py
```

Or pass the title directly:

```bash
python main.py "The Dark Knight"
```

Setup also launches the app for you, so `python setup.py` works as a start command too.

## 🔄 How It Works

```
Movie Title
     │
     ▼
TMDB API Search
     │
     ▼
Sort by popularity, keep top 10
     │
     ▼
Results Found?
     │
 ┌───┴────────────┐
 │                │
 ▼                ▼
One Result    Multiple Results
 │                │
 ▼                ▼
Show Details   Show Results Table
                  │
                  ▼
              Select Movie
                  │
                  ▼
              Show Details
```

- If only one movie matches, its details are shown immediately.
- If several match, the 10 most popular appear in a table. Enter the number of the movie you want, or `q` to quit.

## 📊 Example

Illustrative output (your results will vary):

### Multiple Results

```
Enter movie name: Inception

🔍 Searching for: Inception

📽 Multiple matches found. Pick one:

┏━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Title                 ┃ Year ┃
┡━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ 1 │ Inception             │ 2010 │
│ 2 │ ...                   │ .... │
└───┴───────────────────────┴──────┘

 Enter a number (1-10) or 'q' to quit:
```

### Movie Details

```
              🎬 Movie Details
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Field     ┃ Details                      ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Title     │ Inception                    │
│ Release   │ 2010-07-15                   │
│ Rating    │ 8.4 / 10                     │
│ Votes     │ 36000                        │
│ Language  │ EN                           │
│ Overview  │ A thief who steals secrets...│
└───────────┴──────────────────────────────┘
```

## 🧯 Troubleshooting

| Message | Fix |
| ------- | --- |
| `Invalid TMDB API key` | Run `python setup.py` and enter a valid key |
| `Missing TMDB_API_KEY` | Run `python setup.py` to create `.env` |
| `Too many requests` | Wait a moment and try again |
| `Couldn't reach TMDB` | Check your internet connection |

## 📁 Project Structure

```
tmdb-cli/
├── main.py            # the CLI app
├── setup.py           # installs deps, saves API key, launches the app
├── requirements.txt
├── .gitignore
└── README.md
```

`.env` is created locally by `setup.py` and is git-ignored, so it isn't part of the repo.

## 🔑 Environment Variables

| Variable       | Description       |
| -------------- | ----------------- |
| `TMDB_API_KEY` | Your TMDB API key |

## 📋 Requirements

- Python 3.8+
- Internet connection
- TMDB API key (free)

## 📄 License

This project is intended for learning and demonstration purposes.

## 🙌 Acknowledgements

Movie data is provided by [The Movie Database (TMDB)](https://www.themoviedb.org/).

This project is not affiliated with or endorsed by TMDB.

Inspired by the roadmap.sh project: <https://roadmap.sh/projects/tmdb-cli>
