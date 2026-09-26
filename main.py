filnavn = "sinnes_2014_2025.csv"

with open(filnavn, "r", encoding="utf-8") as fil:
    for linje in fil:
        print(linje)
