
import datetime
import matplotlib.pyplot as plt


filnavn = "sinnes_2014_2025.csv"


# Oppgave d: Les værdata for et valgt år
def les_årsdata(valgt_år):
    datoer = []
    temperaturer = []
    nedbor = []
    vind = []
    snødybder = []

    with open(filnavn, "r", encoding="utf-8-sig") as fil:
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
                snø = parts[6].strip().replace(",", ".")

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
                snødybder.append(
                    float(snø) if snø != "-" else None
                )

            except (ValueError, IndexError):
                continue

    return datoer, temperaturer, nedbor, vind, snødybder


# Oppgave d: Lag diagrammer
def plott_år(valgt_år):
    datoer, temperaturer, nedbor, vind, snødybder = (
        les_årsdata(valgt_år)
    )

    if not datoer:
        print("Fant ingen værdata for dette året.")
        return

    fig, akser = plt.subplots(4, 1, figsize=(12, 12))

    akser[0].plot(datoer, snødybder)
    akser[0].set_title("Snødybde")
    akser[0].set_ylabel("Snødybde (cm)")

    akser[1].plot(datoer, nedbor)
    akser[1].set_title("Nedbør")
    akser[1].set_ylabel("Nedbør (mm)")

    akser[2].plot(datoer, temperaturer)
    akser[2].set_title("Middeltemperatur")
    akser[2].set_ylabel("Temperatur (grader C)")

    akser[3].plot(datoer, vind)
    akser[3].set_title("Høyeste middelvind")
    akser[3].set_ylabel("Vind (m/s)")
    akser[3].set_xlabel("Dato")

    fig.suptitle(f"Værdata for {valgt_år}")
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()


# Oppgave e: Tell dager med skiføre
def tell_skiforedager(sessong_input):
    ski_føre = 0

    with open(filnavn, "r", encoding="utf-8-sig") as fil:
        for linje in fil:
            parts = linje.strip().split(";")

            try:
                dag, måned, år = map(
                    int, parts[2].strip().split(".")
                )
                snø_data = float(
                    parts[6].strip().replace(",", ".")
                )

            except (ValueError, IndexError):
                continue

            i_sesong = (
                (år == sessong_input - 1 and måned >= 11)
                or (år == sessong_input and måned <= 5)
            )

            if i_sesong and snø_data >= 20:
                ski_føre += 1

    return ski_føre
# Oppgave f: Plantevekst
def vekts_per_år(årstall):
    temperatur_år = []
    plante_vekst = 0.0


    with open(filnavn, "r", encoding="utf-8" ) as tempfil:
        
        for linjer in tempfil:
            
            rekke = linjer.split(";")
            året = rekke[2]
           
            str_årstall = str(årstall)

            if året.endswith(str_årstall):
                try:
                    temperatur_år.append(float(rekke[3].replace(",",".")))
                except ValueError, TypeError:
                    continue
            else: 
                continue
        for i in temperatur_år:
            if i >= 5:
                plante_vekst += (i - 5)
            else:
                continue
        print(f"\nPlanten har vokst {round(plante_vekst)} mm i {str_årstall}\n")
        print("Program fullført\n")


# Hovedprogram
def main():
    print("Velg oppgave:")
    print("1 - Plotting av værdata (oppgave d)")
    print("2 - Tell dager med skiføre (oppgave e)")
    print("3 - Plantevekst per år (oppgave f)")

    valg = input("Skriv inn 1 eller 2: ")

    if valg == "1":
        valgt_år = int(input("Skriv inn årstallet du vil plotte: "))
        plott_år(valgt_år)

    elif valg == "2":
        sessong_input = int(
            input("Skriv inn årstallet til skisesongen: ")
        )

        ski_føre = tell_skiforedager(sessong_input)
        print("Antall dager med skiføre:", ski_føre)

    elif valg == "3":
        Godkjente_år = [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025] 
        print(f"\nÅr i liste: {Godkjente_år} ")
        while True:
        try:
            valgt_år = int(input("\nSkriv inn år mellom 2014 og 2025: "))
            if valgt_år in Godkjente_år:
                vekts_per_år(valgt_år)
                break
            else:
                print(f"\n{valgt_år} er ikke i listen: {Godkjente_år}")
                print("Prøv på nytt\n")
                continue
        except ValueError, TypeError:
            print(f"\nDet er bare tall fra denne listen som er godkjent: {Godkjente_år}")
            print("Prøv på nytt\n")
            continue
        

    else:
        print("Ugyldig valg. Velg 1, 2 eller 3.")


if __name__ == "__main__":
    main()


