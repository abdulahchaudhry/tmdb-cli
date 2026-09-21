# 🎬 TMDB CLI

A simple command-line movie search tool built with Python and the **TMDB API**.

Search for movies directly from your terminal, choose from multiple results, and view detailed movie information in a clean table format.

## ✨ Features

* 🔎 Search movies by title
* 📋 Display multiple results in a table
* 🎯 Select a movie interactively
* ⭐ Display movie ratings
* 📅 Display release dates
* 🗳 Display vote counts
* 🌐 Display original language
* 📝 Display movie overview
* 🔐 Store your TMDB API key securely in `.env`
* ⚡ Simple and lightweight CLI

## 🛠️ Built With

* **Python**
* **Requests** — API requests
* **python-dotenv** — Environment variable management
* **Rich** — Terminal tables and formatting
* **TMDB API** — Movie data

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/abdulahchaudhry/tmdb-cli.git
cd tmdb-cli
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a TMDB API Key

Create an account on [The Movie Database](https://www.themoviedb.org/) and obtain an API key.

### 4. Create a `.env` file

Create a `.env` file in the project directory:

```env
TMDB_API_KEY=your_api_key_here
```

> **Important:** Never commit your `.env` file or expose your API key publicly.

## 🚀 Usage

Run the program by providing a movie title:

```bash
python main.py "Inception"
```

You can also search for movies with multiple words:

```bash
python main.py "The Dark Knight"
```

## 🔄 How It Works

The application follows a simple workflow:

```text
Movie Title
     │
     ▼
TMDB API Search
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

If only one movie matches the search, its details are displayed immediately.

If multiple movies are found, they are displayed in a table. Enter the number of the movie you want to view.

You can enter `q` to quit when selecting from multiple results.

## 📊 Example

### Multiple Results

```text
🔍 Searching for: Inception

📽 Multiple matches found. Pick one:

┏━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Title                 ┃ Year ┃
┡━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ 1 │ Inception             │ 2010 │
│ 2 │ Inception: The Cobol  │ 2010 │
└───┴───────────────────────┴──────┘

Enter a number (1-2) or 'q' to quit:
```

### Movie Details

```text
              🎬 Movie Details
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Field     ┃ Details                      ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Title     │ Inception                    │
│ Release   │ 2010-07-15                   │
│ Rating    │ 8.4 / 10                     │
│ Votes     │ 36,000+                      │
│ Language  │ EN                           │
│ Overview  │ A thief who steals secrets... │
└───────────┴──────────────────────────────┘
```

## 📁 Project Structure

```text
tmdb-cli/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🔑 Environment Variables

| Variable       | Description       |
| -------------- | ----------------- |
| `TMDB_API_KEY` | Your TMDB API key |

## 📋 Requirements

* Python 3.8+
* Internet connection
* TMDB API key

## 📄 License

This project is intended for learning and demonstration purposes.

## 🙌 Acknowledgements

Movie data is provided by [The Movie Database (TMDB)](https://www.themoviedb.org/).

This project is not affiliated with or endorsed by TMDB.

The project details: https://roadmap.sh/projects/tmdb-cli