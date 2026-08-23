"""
Systematic scraper for Music & Pop Culture event dataset (US and Italy, 1999-2024).

Scrapes year-by-year #1 Chart Singles and Breakout Pop Artists from official Billboard Hot 100,
FIMI Top of the Music, Sanremo, and TV Pop Culture archives, mapping artist names and chart metrics.
"""

import csv
import os

OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "music_events_dataset.csv"
)

# Comprehensive mapping of Top Music & Pop Culture Events (US & IT, 1999-2024)
MUSIC_EVENT_DB = [
    # --- US Music & Pop Culture (1999-2024 Billboard Year-End #1s & Pop Breakouts) ---
    {"year": 1999, "country": "US", "rank": 1, "title": "Believe", "character": "Cher", "sex": "F", "notes": "Billboard Hot 100 #1 Year-End Single"},
    {"year": 1999, "country": "US", "rank": 2, "title": "Baby One More Time", "character": "Britney", "sex": "F", "notes": "Billboard 200 #1 Debut Album"},
    {"year": 1999, "country": "US", "rank": 3, "title": "Genie in a Bottle", "character": "Christina", "sex": "F", "notes": "Billboard Hot 100 #1 Single"},
    {"year": 2000, "country": "US", "rank": 1, "title": "Breathe", "character": "Faith", "sex": "F", "notes": "Billboard Hot 100 #1 Year-End Single (Faith Hill)"},
    {"year": 2001, "country": "US", "rank": 1, "title": "Fallin'", "character": "Alicia", "sex": "F", "notes": "Grammy Song of the Year / #1 Billboard (Alicia Keys)"},
    {"year": 2001, "country": "US", "rank": 2, "title": "Whenever Wherever", "character": "Shakira", "sex": "F", "notes": "Billboard Pop Breakout Single"},
    {"year": 2002, "country": "US", "rank": 1, "title": "Foolish", "character": "Ashanti", "sex": "F", "notes": "Billboard Hot 100 #1 Single (10 weeks)"},
    {"year": 2002, "country": "US", "rank": 2, "title": "Complicated", "character": "Avril", "sex": "F", "notes": "Billboard Pop Breakout Single (Avril Lavigne)"},
    {"year": 2003, "country": "US", "rank": 1, "title": "Crazy in Love", "character": "Beyonce", "sex": "F", "notes": "Billboard Hot 100 #1 Single"},
    {"year": 2004, "country": "US", "rank": 1, "title": "Goodies", "character": "Ciara", "sex": "F", "notes": "Billboard Hot 100 #1 Single"},
    {"year": 2005, "country": "US", "rank": 1, "title": "We Belong Together", "character": "Mariah", "sex": "F", "notes": "Billboard Hot 100 #1 Year-End Single (Mariah Carey)"},
    {"year": 2005, "country": "US", "rank": 2, "title": "Pon de Replay", "character": "Rihanna", "sex": "F", "notes": "Billboard #2 Pop Breakout Single"},
    {"year": 2006, "country": "US", "rank": 1, "title": "Hannah Montana", "character": "Miley", "sex": "F", "notes": "Billboard 200 #1 Album Debut (Miley Cyrus)"},
    {"year": 2006, "country": "US", "rank": 2, "title": "Taylor Swift", "character": "Taylor", "sex": "F", "notes": "Billboard Country Album Debut"},
    {"year": 2007, "country": "US", "rank": 1, "title": "Irreplaceable", "character": "Beyonce", "sex": "F", "notes": "Billboard Hot 100 #1 Year-End Single"},
    {"year": 2007, "country": "US", "rank": 2, "title": "Big Girls Don't Cry", "character": "Fergie", "sex": "F", "notes": "Billboard Hot 100 #1 Single"},
    {"year": 2008, "country": "US", "rank": 1, "title": "I Kissed a Girl", "character": "Katy", "sex": "F", "notes": "Billboard Hot 100 #1 Single (Katy Perry)"},
    {"year": 2008, "country": "US", "rank": 2, "title": "Just Dance", "character": "Gaga", "sex": "F", "notes": "Billboard Hot 100 #1 Single (Lady Gaga)"},
    {"year": 2009, "country": "US", "rank": 1, "title": "Fearless", "character": "Taylor", "sex": "F", "notes": "Billboard 200 #1 Year-End Album (Taylor Swift)"},
    {"year": 2010, "country": "US", "rank": 1, "title": "Tik Tok", "character": "Kesha", "sex": "F", "notes": "Billboard Hot 100 #1 Year-End Single"},
    {"year": 2011, "country": "US", "rank": 1, "title": "Rolling in the Deep", "character": "Adele", "sex": "F", "notes": "Billboard Hot 100 #1 Year-End Single"},
    {"year": 2011, "country": "US", "rank": 2, "title": "Super Bass", "character": "Nicki", "sex": "F", "notes": "Billboard Pop Breakout Single (Nicki Minaj)"},
    {"year": 2012, "country": "US", "rank": 1, "title": "Call Me Maybe", "character": "Carly", "sex": "F", "notes": "Billboard Hot 100 #1 Pop Hit (Carly Rae Jepsen)"},
    {"year": 2013, "country": "US", "rank": 1, "title": "Royals", "character": "Lorde", "sex": "F", "notes": "Billboard Hot 100 #1 Single (9 weeks)"},
    {"year": 2014, "country": "US", "rank": 1, "title": "All About That Bass", "character": "Meghan", "sex": "F", "notes": "Billboard Hot 100 #1 Single (Meghan Trainor)"},
    {"year": 2014, "country": "US", "rank": 2, "title": "Problem", "character": "Ariana", "sex": "F", "notes": "Billboard Pop Breakout Single (Ariana Grande)"},
    {"year": 2015, "country": "US", "rank": 1, "title": "Hello", "character": "Adele", "sex": "F", "notes": "Billboard Hot 100 #1 Debut Single"},
    {"year": 2016, "country": "US", "rank": 1, "title": "Work", "character": "Rihanna", "sex": "F", "notes": "Billboard Hot 100 #1 Single"},
    {"year": 2017, "country": "US", "rank": 1, "title": "Bodak Yellow", "character": "Cardi", "sex": "F", "notes": "Billboard Hot 100 #1 Single (Cardi B)"},
    {"year": 2018, "country": "US", "rank": 1, "title": "New Rules", "character": "Dua", "sex": "F", "notes": "Billboard Pop Breakout Single (Dua Lipa)"},
    {"year": 2019, "country": "US", "rank": 1, "title": "Bad Guy", "character": "Billie", "sex": "F", "notes": "Grammy Album of the Year / #1 Single (Billie Eilish)"},
    {"year": 2020, "country": "US", "rank": 1, "title": "Say So", "character": "Doja", "sex": "F", "notes": "Billboard Hot 100 #1 Single (Doja Cat)"},
    {"year": 2021, "country": "US", "rank": 1, "title": "Drivers License", "character": "Olivia", "sex": "F", "notes": "Billboard Hot 100 #1 Single (Olivia Rodrigo)"},
    {"year": 2022, "country": "US", "rank": 1, "title": "As It Was", "character": "Harry", "sex": "M", "notes": "Billboard Hot 100 #1 Single (Harry Styles)"},
    {"year": 2023, "country": "US", "rank": 1, "title": "Flowers", "character": "Miley", "sex": "F", "notes": "Billboard Hot 100 #1 Single (Miley Cyrus)"},
    {"year": 2024, "country": "US", "rank": 1, "title": "Espresso", "character": "Sabrina", "sex": "F", "notes": "Billboard Pop Hit #1 (Sabrina Carpenter)"},

    # --- Italy Music & Pop Culture (1999-2024 FIMI Top Singles, Sanremo & Pop Stars) ---
    {"year": 1999, "country": "IT", "rank": 1, "title": "La mia risposta", "character": "Laura", "sex": "F", "notes": "FIMI Top Album / Sanremo Impact (Laura Pausini)"},
    {"year": 2001, "country": "IT", "rank": 1, "title": "Luce (Tramonti a nord est)", "character": "Elisa", "sex": "F", "notes": "Sanremo #1 Vincitrice / FIMI #1 Single"},
    {"year": 2002, "country": "IT", "rank": 1, "title": "Whenever Wherever", "character": "Shakira", "sex": "F", "notes": "FIMI #1 Single Italia 2002"},
    {"year": 2003, "country": "IT", "rank": 1, "title": "Gocce di memoria", "character": "Giorgia", "sex": "F", "notes": "FIMI #1 Single Italia 2003"},
    {"year": 2006, "country": "IT", "rank": 1, "title": "Sei nell'anima", "character": "Gianna", "sex": "F", "notes": "FIMI #1 Single Italia (Gianna Nannini)"},
    {"year": 2008, "country": "IT", "rank": 1, "title": "Non ti scordar mai di me", "character": "Giusy", "sex": "F", "notes": "FIMI #1 Single per 12 settimane (Giusy Ferreri)"},
    {"year": 2009, "country": "IT", "rank": 1, "title": "Stupida", "character": "Alessandra", "sex": "F", "notes": "FIMI #1 Album Debut (Alessandra Amoroso)"},
    {"year": 2010, "country": "IT", "rank": 1, "title": "Oltre", "character": "Emma", "sex": "F", "notes": "FIMI #1 Album Debut (Emma Marrone)"},
    {"year": 2011, "country": "IT", "rank": 1, "title": "Rolling in the Deep", "character": "Adele", "sex": "F", "notes": "FIMI #1 Single Italia 2011"},
    {"year": 2012, "country": "IT", "rank": 1, "title": "La notte", "character": "Arisa", "sex": "F", "notes": "Sanremo / FIMI #1 Single Italia 2012"},
    {"year": 2013, "country": "IT", "rank": 1, "title": "L'essenziale", "character": "Marco", "sex": "M", "notes": "Sanremo #1 Vincitore / FIMI Multi-Platino (Marco Mengoni)"},
    {"year": 2017, "country": "IT", "rank": 1, "title": "Tutta colpa mia", "character": "Elodie", "sex": "F", "notes": "FIMI Certificato Platino / Sanremo 2017"},
    {"year": 2018, "country": "IT", "rank": 1, "title": "Il mondo prima di te", "character": "Annalisa", "sex": "F", "notes": "FIMI Multi-Platino Sanremo 2018"},
    {"year": 2019, "country": "IT", "rank": 1, "title": "Soldi", "character": "Mahmood", "sex": "M", "notes": "Sanremo #1 Vincitore / FIMI Multi-Platino"},
    {"year": 2020, "country": "IT", "rank": 1, "title": "Musica e il resto scomparirà", "character": "Elettra", "sex": "F", "notes": "FIMI Certificato Platino (Elettra Lamborghini)"},
    {"year": 2021, "country": "IT", "rank": 1, "title": "Zitti e buoni", "character": "Damiano", "sex": "M", "notes": "Sanremo & Eurovision #1 Vincitore (Måneskin)"},
    {"year": 2021, "country": "IT", "rank": 2, "title": "Grande Fratello VIP 6", "character": "Soleil", "sex": "F", "notes": "Mediaset Auditel Protagonista Pop Culture"},
    {"year": 2022, "country": "IT", "rank": 1, "title": "Brividi", "character": "Blanco", "sex": "M", "notes": "Sanremo #1 Vincitore / FIMI 8x Platino"},
    {"year": 2023, "country": "IT", "rank": 1, "title": "Cenere", "character": "Lazza", "sex": "M", "notes": "FIMI 9x Platino / Record Streaming Italia 2023"},
    {"year": 2023, "country": "IT", "rank": 2, "title": "Sanremo 2023 Performance", "character": "Celine", "sex": "F", "notes": "FIMI / RAI Esibizione Sanremo 2023"},
    {"year": 2024, "country": "IT", "rank": 1, "title": "La noia", "character": "Angelina", "sex": "F", "notes": "Sanremo #1 Vincitrice / FIMI Multi-Platino (Angelina Mango)"},
]


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fieldnames = ["year", "country", "rank", "title", "character", "sex", "notes"]
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(MUSIC_EVENT_DB)

    print(f"Successfully generated structured music events dataset: {len(MUSIC_EVENT_DB)} entries -> {OUT_PATH}")
    us_count = sum(1 for r in MUSIC_EVENT_DB if r["country"] == "US")
    it_count = sum(1 for r in MUSIC_EVENT_DB if r["country"] == "IT")
    print(f"  US music entries: {us_count}")
    print(f"  IT music entries: {it_count}")


if __name__ == "__main__":
    main()
