filnavn = "sinnes_2014_2025.csv"

sessong_input = int(input('skriv inn årstallet for ski sessongen:  '))

ski_føre = 0

with open(filnavn, "r", encoding="utf-8") as fil:
    for linje in fil:
        parts = linje.split(";")
        snø_dager = parts[6]
        dato = parts[2]

        try:
            dag, måned, år = map(int,dato.split("."))
            snø_data = float(snø_dager.replace(",", "."))
        except(ValueError, IndexError):
            continue

        i_sessong = (år == sessong_input - 1 and måned >= 11) or (år == sessong_input and måned <= 5)
        if i_sessong and snø_data >= 20:
            ski_føre += 1

        # print(snø_data)



print(ski_føre)
