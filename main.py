


import datetime
import matplotlib.pyplot as plt


FILNAVN = "DAT120-gutta/sinnes_2014_2025.csv"


def les_årsdata(valgt_år):
    datoer = []
    temperaturer = []
    nedbor = []
    vind = []
    snodybde = []

    with open(FILNAVN, "r", encoding="utf-8-sig") as fil:
        for linje in fil:
            parts = linje.strip().split(";")

            try:
                dato = datetime.datetime.strptime(
                    parts[2].strip(), "%d.%m.%Y"
                )

                if dato.year != valgt_år:
                    continue

                temperatur = parts[3].strip().replace(",", ".")
                regn = parts[4].strip().replace(",", ".")
                vindstyrke = parts[5].strip().replace(",", ".")
                sno = parts[6].strip().replace(",", ".")

                datoer.append(dato)
                temperaturer.append(
                    float(temperatur) if temperatur != "-" else None
                )
                nedbor.append(
                    float(regn) if regn != "-" else None
                )
                vind.append(
                    float(vindstyrke) if vindstyrke != "-" else None
                )
                snodybde.append(
                    float(sno) if sno != "-" else None
                )

            except (ValueError, IndexError):
                continue

    return datoer, temperaturer, nedbor, vind, snodybde


def plott_år(valgt_år):
    datoer, temperaturer, nedbor, vind, snodybde = (
        les_årsdata(valgt_år)
    )

    if not datoer:
        print("Fant ingen værdata for dette året.")
        return

    # Lag fire diagrammer, ett for hver værvariabel
    fig, akser = plt.subplots(4, 1, figsize=(12, 12))

    akser[0].plot(datoer, snodybde)
    akser[0].set_title("Snødybde")
    akser[0].set_ylabel("Snødybde (cm)")

    akser[1].plot(datoer, nedbor)
    akser[1].set_title("Døgnnedbør")
    akser[1].set_ylabel("Nedbør (mm)")

    akser[2].plot(datoer, temperaturer)
    akser[2].set_title("Middeltemperatur")
    akser[2].set_ylabel("Temperatur (°C)")

    akser[3].plot(datoer, vind)
    akser[3].set_title("Høyeste middelvind")
    akser[3].set_ylabel("Vind (m/s)")
    akser[3].set_xlabel("Dato")

    fig.suptitle(f"Værdata for {valgt_år}")
    fig.tight_layout()
    plt.show()


def tell_skiforedager(sessong_år):
    ski_føre = 0

    with open(FILNAVN, "r", encoding="utf-8-sig") as fil:
        for linje in fil:
            parts = linje.strip().split(";")

            try:
                dag, måned, år = map(
                    int, parts[2].strip().split(".")
                )
                snødybde = float(
                    parts[6].strip().replace(",", ".")
                )

            except (ValueError, IndexError):
                continue

            i_sesong = (
                (år == sessong_år - 1 and måned >= 11)
                or (år == sessong_år and måned <= 5)
            )

            if i_sesong and snødybde >= 20:
                ski_føre += 1

    return ski_føre


def main():
    print("1: Plotting av værdata (oppgave d)")
    print("2: Antall dager med skiføre (oppgave e)")

    valg = input("Velg oppgave (1 eller 2): ")

    if valg == "1":
        valgt_år = int(input("Skriv inn årstallet du vil plotte: "))
        plott_år(valgt_år)

    elif valg == "2":
        sessong_år = int(
            input("Skriv inn året skisesongen slutter: ")
        )
        ski_føre = tell_skiforedager(sessong_år)
        print("Antall dager med skiføre:", ski_føre)

    else:
        print("Ugyldig valg. Velg 1 eller 2.")


if __name__ == "__main__":
    main()


