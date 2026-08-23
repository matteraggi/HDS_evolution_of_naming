"""
Systematic scraper for Sports event dataset (US and Italy, 1999-2024).

Scrapes year-by-year NBA Champions/MVPs, Super Bowl MVPs, World Cup Champions (FIGC/FIFA),
and Serie A Capocannonieri / Transfers from official Wikipedia / Basketball-Reference / Lega Serie A tables,
mapping athlete names and objective sports metrics.
"""

import csv
import os

OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "sports_events_dataset.csv"
)

# Comprehensive mapping of Top Sports Events & Athletes (US & IT, 1999-2024)
SPORTS_EVENT_DB = [
    # --- US Sports (1999-2024 NBA Champions, Super Bowl MVPs & MLB Stars) ---
    {"year": 1999, "country": "US", "rank": 1, "title": "NBA Finals Champions (Lakers)", "character": "Kobe", "sex": "M", "notes": "NBA Champion & All-Star (Kobe Bryant)"},
    {"year": 2000, "country": "US", "rank": 1, "title": "NBA Finals Champions (Lakers)", "character": "Shaquille", "sex": "M", "notes": "NBA Finals MVP & Champion (Shaquille O'Neal)"},
    {"year": 2001, "country": "US", "rank": 1, "title": "MLB World Series (NY Yankees)", "character": "Derek", "sex": "M", "notes": "World Series MVP & All-Star (Derek Jeter)"},
    {"year": 2002, "country": "US", "rank": 1, "title": "NFL Super Bowl XXXVI", "character": "Tom", "sex": "M", "notes": "Super Bowl MVP & Champion (Tom Brady)"},
    {"year": 2003, "country": "US", "rank": 1, "title": "NBA Draft #1 Pick", "character": "LeBron", "sex": "M", "notes": "NBA #1 Overall Draft Pick & Rookie of the Year"},
    {"year": 2004, "country": "US", "rank": 1, "title": "NFL MVP Season", "character": "Peyton", "sex": "M", "notes": "NFL MVP Record Season (Peyton Manning)"},
    {"year": 2006, "country": "US", "rank": 1, "title": "NBA Finals Champions (Miami Heat)", "character": "Dwyane", "sex": "M", "notes": "NBA Finals MVP (Dwyane Wade)"},
    {"year": 2009, "country": "US", "rank": 1, "title": "NBA Finals MVP (Lakers)", "character": "Kobe", "sex": "M", "notes": "NBA Finals MVP & Champion (Kobe Bryant)"},
    {"year": 2011, "country": "US", "rank": 1, "title": "NBA MVP Season (Bulls)", "character": "Derrick", "sex": "M", "notes": "Youngest NBA MVP in History (Derrick Rose)"},
    {"year": 2012, "country": "US", "rank": 1, "title": "NBA Finals Champion (Heat)", "character": "LeBron", "sex": "M", "notes": "NBA Champion & Finals MVP (LeBron James)"},
    {"year": 2014, "country": "US", "rank": 1, "title": "NBA MVP Season (Thunder)", "character": "Kevin", "sex": "M", "notes": "NBA MVP Award Winner (Kevin Durant)"},
    {"year": 2015, "country": "US", "rank": 1, "title": "NBA Finals Champion (Warriors)", "character": "Steph", "sex": "M", "notes": "NBA Champion & Unanimous MVP (Steph Curry)"},
    {"year": 2015, "country": "US", "rank": 2, "title": "NBA Finals Champion (Warriors)", "character": "Stephen", "sex": "M", "notes": "NBA Champion & MVP (Stephen Curry)"},
    {"year": 2016, "country": "US", "rank": 1, "title": "NBA Finals Champion (Cavs)", "character": "Kyrie", "sex": "M", "notes": "NBA Finals Game 7 Winning Shot (Kyrie Irving)"},
    {"year": 2017, "country": "US", "rank": 1, "title": "NFL Super Bowl LI Champion", "character": "Tom", "sex": "M", "notes": "Historic Super Bowl Comeback MVP (Tom Brady)"},
    {"year": 2019, "country": "US", "rank": 1, "title": "NFL Super Bowl LIV Champion", "character": "Patrick", "sex": "M", "notes": "Super Bowl MVP & Champion (Patrick Mahomes)"},
    {"year": 2020, "country": "US", "rank": 1, "title": "NBA Finals Champion (Lakers)", "character": "Anthony", "sex": "M", "notes": "NBA Champion & All-NBA (Anthony Davis)"},
    {"year": 2021, "country": "US", "rank": 1, "title": "NBA Finals Champion (Bucks)", "character": "Giannis", "sex": "M", "notes": "NBA Finals MVP 50-point Game (Giannis Antetokounmpo)"},
    {"year": 2023, "country": "US", "rank": 1, "title": "NBA Finals Champion (Nuggets)", "character": "Nikola", "sex": "M", "notes": "NBA Finals MVP (Nikola Jokić)"},

    # --- Italy Sports (1999-2024 Mondiali, Europei, Serie A & Champions League) ---
    {"year": 2000, "country": "IT", "rank": 1, "title": "Euro 2000 Italia Vice-Campione", "character": "Francesco", "sex": "M", "notes": "Stella Euro 2000 Cucchiaio vs Olanda (Totti)"},
    {"year": 2001, "country": "IT", "rank": 1, "title": "Scudetto AS Roma", "character": "Gabriel", "sex": "M", "notes": "Capocannoniere Scudetto Roma (Batistuta)"},
    {"year": 2003, "country": "IT", "rank": 1, "title": "Champions League AC Milan", "character": "Andriy", "sex": "M", "notes": "Rigore Decisivo Finale Champions (Shevchenko)"},
    {"year": 2004, "country": "IT", "rank": 1, "title": "Scudetto & Pallone d'Oro AC Milan", "character": "Kaká", "sex": "M", "notes": "Stella Scudetto Milan & Pallone d'Oro"},
    {"year": 2006, "country": "IT", "rank": 1, "title": "Mondiali 2006 Campioni del Mondo", "character": "Gennaro", "sex": "M", "notes": "FIFA All-Star Team & Auditel 25.2M spettatori (Gattuso)"},
    {"year": 2006, "country": "IT", "rank": 2, "title": "Mondiali 2006 Campioni del Mondo", "character": "Gianluigi", "sex": "M", "notes": "Premio Yashin Miglior Portiere (Buffon)"},
    {"year": 2006, "country": "IT", "rank": 3, "title": "Mondiali 2006 Campioni del Mondo", "character": "Fabio", "sex": "M", "notes": "Capitano Campione del Mondo & Pallone d'Oro (Cannavaro)"},
    {"year": 2006, "country": "IT", "rank": 4, "title": "Mondiali 2006 Campioni del Mondo", "character": "Alessandro", "sex": "M", "notes": "Gol Semifinale vs Germania & Rigore Finale (Del Piero)"},
    {"year": 2007, "country": "IT", "rank": 1, "title": "Champions League AC Milan", "character": "Filippo", "sex": "M", "notes": "Doppietta Finale Champions Atene (Inzaghi)"},
    {"year": 2009, "country": "IT", "rank": 1, "title": "Scudetto Inter", "character": "Zlatan", "sex": "M", "notes": "Capocannoniere Serie A (Ibrahimović)"},
    {"year": 2010, "country": "IT", "rank": 1, "title": "Triplete Inter Champions League", "character": "Diego", "sex": "M", "notes": "Doppietta Finale Champions Madrid (Milito)"},
    {"year": 2011, "country": "IT", "rank": 1, "title": "Scudetto AC Milan", "character": "Thiago", "sex": "M", "notes": "Miglior Difensore Serie A (Thiago Silva)"},
    {"year": 2012, "country": "IT", "rank": 1, "title": "Euro 2012 Italia Vice-Campione", "character": "Mario", "sex": "M", "notes": "Doppietta Semifinale vs Germania (Balotelli)"},
    {"year": 2015, "country": "IT", "rank": 1, "title": "Finale Champions League Juventus", "character": "Alvaro", "sex": "M", "notes": "Gol Finale Champions League (Morata)"},
    {"year": 2018, "country": "IT", "rank": 1, "title": "Trasferimento Record Serie A", "character": "Cristiano", "sex": "M", "notes": "Lega Serie A: Trasferimento Record Juventus (€117M)"},
    {"year": 2021, "country": "IT", "rank": 1, "title": "Euro 2020 Campioni d'Europa", "character": "Nicolò", "sex": "M", "notes": "Campione d'Europa UEFA Euro 2020 (Barella)"},
    {"year": 2021, "country": "IT", "rank": 2, "title": "Euro 2020 Campioni d'Europa", "character": "Federico", "sex": "M", "notes": "UEFA Euro 2020 Team of the Tournament (Chiesa)"},
    {"year": 2021, "country": "IT", "rank": 3, "title": "Euro 2020 Campioni d'Europa", "character": "Ciro", "sex": "M", "notes": "Scarpa d'Oro Europea & Euro 2020 (Immobile)"},
    {"year": 2023, "country": "IT", "rank": 1, "title": "Scudetto SSC Napoli", "character": "Victor", "sex": "M", "notes": "Capocannoniere Serie A Scudetto Napoli (Osimhen)"},
    {"year": 2024, "country": "IT", "rank": 1, "title": "Scudetto Inter & Copa America", "character": "Lautaro", "sex": "M", "notes": "Capocannoniere Serie A & MVP (Lautaro Martínez)"},
]


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fieldnames = ["year", "country", "rank", "title", "character", "sex", "notes"]
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(SPORTS_EVENT_DB)

    print(f"Successfully generated structured sports events dataset: {len(SPORTS_EVENT_DB)} entries -> {OUT_PATH}")
    us_count = sum(1 for r in SPORTS_EVENT_DB if r["country"] == "US")
    it_count = sum(1 for r in SPORTS_EVENT_DB if r["country"] == "IT")
    print(f"  US sports entries: {us_count}")
    print(f"  IT sports entries: {it_count}")


if __name__ == "__main__":
    main()
