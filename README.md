# 🕷️ Universal Web Scraper

A flexible Python script that extracts product data (name, price, rating) from any e‑commerce website based on user‑provided CSS selectors. Handles pagination and outputs a CSV file.

## ✨ Features

- **Interactive setup** – you provide the URL and selectors.
- **Pagination support** – follows "next" links if selector is given.
- **Polite scraping** – includes random delays.
- **CSV export** – clean, structured output.
- **Error‑resistant** – gracefully handles missing elements.

## 🚀 How to Run

1. **Clone** the repo and install dependencies:
   ```bash
   pip install -r requirements.txt