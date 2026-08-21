"""
Scrape historical box office and cultural event source data from Wikipedia / Cinetel / Box Office Mojo.

Outputs raw tables used to populate dataset/events_dataset.csv for the RQ2 Event Study.
"""

import csv
import html.parser
import os
import urllib.request

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed")
os.makedirs(OUT_DIR, exist_ok=True)


class WikiTableParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_td = False
        self.current_row = []
        self.rows = []
        self.current_cell = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table" and "wikitable" in attrs_dict.get("class", ""):
            self.in_table = True
        if self.in_table:
            if tag == "tr":
                self.current_row = []
            elif tag in ("td", "th"):
                self.in_td = True
                self.current_cell = ""

    def handle_endtag(self, tag):
        if self.in_table:
            if tag == "tr":
                if self.current_row:
                    self.rows.append(self.current_row)
            elif tag in ("td", "th"):
                self.in_td = False
                self.current_row.append(self.current_cell.strip())
            elif tag == "table":
                self.in_table = False

    def handle_data(self, data):
        if self.in_td:
            self.current_cell += data


def fetch_us_box_office():
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films_in_the_United_States_by_year"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html_content = urllib.request.urlopen(req).read().decode("utf-8")
    parser = WikiTableParser()
    parser.feed(html_content)

    results = []
    for r in parser.rows:
        if len(r) >= 2 and r[0].isdigit() and int(r[0]) >= 1980:
            results.append({"year": r[0], "title": r[1], "country": "US"})
    return results


def fetch_it_box_office():
    url = "https://it.wikipedia.org/wiki/Film_con_maggiori_incassi_in_Italia"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html_content = urllib.request.urlopen(req).read().decode("utf-8")
    parser = WikiTableParser()
    parser.feed(html_content)

    results = []
    for r in parser.rows:
        if len(r) >= 3 and r[0].isdigit():
            results.append({"rank": r[0], "title": r[1], "year": r[2], "country": "IT"})
    return results


def main():
    us_movies = fetch_us_box_office()
    it_movies = fetch_it_box_office()
    print(f"Scraped {len(us_movies)} US top annual movies and {len(it_movies)} IT top historic movies.")


if __name__ == "__main__":
    main()
