# 🎬 IMDb Top Movies Scraper & Emailer

A Python project that scrapes the **top movies from IMDb** and sends them via **email** as a **HTML table** with a **CSV attachment**.  
This project demonstrates **web scraping, CSV handling, OOP in Python, and email automation**.

---

## ✨ Features
- 🏆 Scrapes top movies from [IMDb Top 250](https://www.imdb.com/chart/top/)
- 💾 Saves movie data (`title`, `year`, `rating`, `link`) into a **CSV file**
- 📧 Sends a nicely formatted **HTML email** with:
  - Movie title, year, rating, and link
  - CSV attachment
- ⚙️ Adjustable number of movies to scrape

---

## 🛠️ Requirements
- Python **3.8+**
- Libraries:
  - `requests` 🔹 `beautifulsoup4`
