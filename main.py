import requests
from bs4 import BeautifulSoup
import json
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import sys

# ----------------------- Logging Setup -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ----------------------- IMDb Scraper (JSON-LD) -----------------------
class IMDbScraper:
    def __init__(self, url="https://www.imdb.com/chart/top/"):
        self.url = url

    def get_top_movies(self, count=5):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            script = soup.find("script", type="application/ld+json")
            data = json.loads(script.string)

            movies = []
            for item in data["itemListElement"][:count]:
                movie = item["item"]
                movies.append({
                    "title": movie["name"],
                    "year": movie.get("datePublished", ""),
                    "rating": movie.get("aggregateRating", {}).get("ratingValue", ""),
                    "link": movie["url"]
                })

            logging.info(f"Scraped top {len(movies)} movies from IMDb.")
            return movies
        except Exception as e:
            logging.error(f"Error scraping IMDb: {e}")
            return []

# ----------------------- CSV Handler -----------------------
class CSVHandler:
    def __init__(self, filename="top_movies.csv"):
        self.filename = filename

    def save_to_csv(self, movies):
        try:
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["title", "year", "rating", "link"])
                writer.writeheader()
                writer.writerows(movies)
            logging.info(f"Saved {len(movies)} movies to {self.filename}.")
        except Exception as e:
            logging.error(f"Error writing CSV: {e}")

# ----------------------- Email Sender -----------------------
class EmailSender:
    def __init__(self, sender_email, sender_password, smtp_server="smtp.gmail.com", port=587):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.port = port

    def send_email(self, recipient_email, subject, movies, attachment_path):
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject

            # Build HTML table
            html = """
            <html>
            <body>
            <h2>Top IMDb Movies</h2>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr>
                    <th style="width: 40%;">Title</th>
                    <th style="width: 15%;">Year</th>
                    <th style="width: 15%;">Rating</th>
                    <th style="width: 30%;">Link</th>
                </tr>
            """
            for movie in movies:
                html += f"""
                <tr>
                    <td>{movie['title']}</td>
                    <td>{movie['year']}</td>
                    <td>{movie['rating']}</td>
                    <td><a href="{movie['link']}">IMDb Page</a></td>
                </tr>
                """
            html += """
            </table>
            </body>
            </html>
            """

            msg.attach(MIMEText(html, "html"))

            # Attach CSV as well
            with open(attachment_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={attachment_path}")
                msg.attach(part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logging.info(f"Email sent successfully to {recipient_email}.")
        except Exception as e:
            logging.error(f"Error sending email: {e}")

# ----------------------- Main Script -----------------------
if __name__ == "__main__":
    # 1️⃣ Scrape IMDb
    scraper = IMDbScraper()
    movies = scraper.get_top_movies(count=5)
    logging.info(f"Movies: {movies}")

    # 2️⃣ Save to CSV
    csv_handler = CSVHandler("top_movies.csv")
    csv_handler.save_to_csv(movies)

    # 3️⃣ Send Email
    email_sender = EmailSender(
        sender_email="your_email@gmail.com",
        sender_password="your_app_passwordng"
    )
    email_sender.send_email(
        recipient_email="reciever_email@gmail.com",
        subject="Top 5 IMDb Movies",
        movies=movies,
        attachment_path="top_movies.csv"
    )

    logging.info("✅ Top 5 IMDb movies scraped, saved to CSV, and emailed successfully!")
