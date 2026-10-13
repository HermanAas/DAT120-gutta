import datetime
import matplotlib.pyplot as plt

filnavn = "sinnes_2014_2025_med_makstemperatur.csv"

# Gjør en verdi fra CSV-filen om til et tall
def les_tall(verdi):
    verdi = verdi.strip().replace(",", ".")

    if verdi == "" or verdi == "-":
        return None

    try:
        return float(verdi)
    except ValueError:
        return None


# Leser værdata fra CSV-filen
def les_data():
    data = []

    with open(filnavn, "r", encoding="utf-8-sig") as fil:
        next(fil)

        for linje in fil:
            rekke = linje.strip().split(";")

            if len(rekke) < 8:
                continue

            try:
                dato = datetime.datetime.strptime(
                    rekke[2].strip(), "%d.%m.%Y"
                )
            except ValueError:
                continue

            data.append({
                "dato": dato,
                "maks_temp": les_tall(rekke[3]),
                "temperatur": les_tall(rekke[4]),
                "nedbor": les_tall(rekke[5]),
                "vind": les_tall(rekke[6]),
                "snodybde": les_tall(rekke[7])
            })

    return data


# Oppgave d: Plott værdata for et valgt år
def plott_år(år):
    data = les_data()

    datoer = []
    snodybde = []
    nedbor = []
    temperaturer = []
    vind = []

    for rad in data:
        if rad["dato"].year == år:
            datoer.append(rad["dato"])
            snodybde.append(rad["snodybde"])
            nedbor.append(rad["nedbor"])
            temperaturer.append(rad["temperatur"])
            vind.append(rad["vind"])

    if not datoer:
        print("Fant ingen data for dette året.")
        return

    fig, akser = plt.subplots(4, 1, figsize=(14, 12), sharex=True)

    akser[0].plot(datoer, snodybde)
    akser[0].set_title("Snødybde")
    akser[0].set_ylabel("Snødybde (cm)")
    akser[0].grid(True)

    akser[1].plot(datoer, nedbor)
    akser[1].set_title("Nedbør")
    akser[1].set_ylabel("Nedbør (mm)")
    akser[1].grid(True)

    akser[2].plot(datoer, temperaturer)
    akser[2].set_title("Middeltemperatur")
    akser[2].set_ylabel("Temperatur (°C)")
    akser[2].grid(True)

    akser[3].plot(datoer, vind)
    akser[3].set_title("Høyeste middelvind")
    akser[3].set_ylabel("Vind (m/s)")
    akser[3].set_xlabel("Dato")
    akser[3].grid(True)

    fig.suptitle(f"Værdata fra Sinnes i {år}")
    fig.autofmt_xdate(rotation=30, ha="right")
    fig.tight_layout()
    plt.show()


# Oppgave e: Tell dager med skiføre
def tell_skiforedager(år):
    data = les_data()
    antall_dager = 0

    for rad in data:
        dato = rad["dato"]
        snodybde = rad["snodybde"]

        if snodybde is None:
            continue

        if (
            dato.year == år - 1 and dato.month >= 11
        ) or (
            dato.year == år and dato.month <= 5
        ):
            if snodybde >= 20:
                antall_dager += 1

    print(f"Antall dager med skiføre i skisesongen {år}: {antall_dager}")

    if år == 2014:
        print("Merk: Skisesongen er ufullstendig fordi filen starter i 2014.")


# Oppgave f: Beregn total plantevekst
def beregn_plantevekst(år):
    data = les_data()
    total_vekst = 0

    for rad in data:
        if rad["dato"].year == år:
            temperatur = rad["temperatur"]

            if temperatur is not None and temperatur > 5:
                total_vekst += temperatur - 5

    print(f"Total plantevekst i {år}: {total_vekst:.2f}")


# Oppgave g: Finn lengste periode uten nedbør
def finn_torrperiode():
    data = les_data()

    lengste_periode = 0
    periode = 0
    startdato = None
    beste_startdato = None
    beste_sluttdato = None
    forrige_dato = None

    for rad in data:
        dato = rad["dato"].date()
        nedbor = rad["nedbor"]

        # Manglende nedbørdata skal ikke regnes som tørre dager
        if nedbor is None:
            periode = 0
            startdato = None
            forrige_dato = dato
            continue

        # En manglende dato bryter en sammenhengende periode
        if (
            forrige_dato is not None
            and (dato - forrige_dato).days != 1
        ):
            periode = 0
            startdato = None

        if nedbor == 0:
            if periode == 0:
                startdato = dato

            periode += 1

            if periode > lengste_periode:
                lengste_periode = periode
                beste_startdato = startdato
                beste_sluttdato = dato
        else:
            periode = 0
            startdato = None

        forrige_dato = dato

    if lengste_periode == 0:
        print("Fant ingen sammenhengende periode uten nedbør.")
    else:
        print("Lengste periode uten nedbør:", lengste_periode, "dager")
        print("Startdato:", beste_startdato)
        print("Sluttdato:", beste_sluttdato)


# Oppgave h: Tell sommerdager, høysommerdager og tropedager
def tell_varme_dager(år):
    data = les_data()

    sommerdager = 0
    høysommerdager = 0
    tropedager = 0

    for rad in data:
        if rad["dato"].year == år:
            temperatur = rad["maks_temp"]

            if temperatur is None:
                continue

            if temperatur > 20:
                sommerdager += 1

            if temperatur > 25:
                høysommerdager += 1

            if temperatur > 30:
                tropedager += 1

    print(f"Sommerdager i {år}: {sommerdager}")
    print(f"Høysommerdager i {år}: {høysommerdager}")
    print(f"Tropedager i {år}: {tropedager}")


# Hovedmeny
def main():
    while True:
        print("\n--- Værdata fra Sinnes ---")
        print("1 - Plott værdata (oppgave d)")
        print("2 - Tell dager med skiføre (oppgave e)")
        print("3 - Beregn plantevekst (oppgave f)")
        print("4 - Finn lengste tørre periode (oppgave g)")
        print("5 - Tell varme dager (oppgave h)")
        print("0 - Avslutt")

        try:
            valg = input("Velg oppgave: ").strip()

            if valg == "0":
                print("Programmet avsluttes.")
                break

            elif valg == "1":
                år = int(input("Skriv inn år (2014–2025): "))

                if 2014 <= år <= 2025:
                    plott_år(år)
                else:
                    print("Velg et år mellom 2014 og 2025.")

            elif valg == "2":
                år = int(input("Skriv inn år for skisesongen (2014–2025): "))

                if 2014 <= år <= 2025:
                    tell_skiforedager(år)
                else:
                    print("Velg et år mellom 2014 og 2025.")

            elif valg == "3":
                år = int(input("Skriv inn år (2014–2025): "))

                if 2014 <= år <= 2025:
                    beregn_plantevekst(år)
                else:
                    print("Velg et år mellom 2014 og 2025.")

            elif valg == "4":
                finn_torrperiode()

            elif valg == "5":
                år = int(input("Skriv inn år (2014–2025): "))

                if 2014 <= år <= 2025:
                    tell_varme_dager(år)
                else:
                    print("Velg et år mellom 2014 og 2025.")

            else:
                print("Ugyldig valg. Prøv igjen.")

        except ValueError:
            print("Ugyldig input. Skriv inn et gyldig tall.")

        except KeyboardInterrupt:
            print("\nProgrammet avsluttes.")
            break

        except FileNotFoundError:
            print("Fant ikke CSV-filen. Kontroller filnavnet og plasseringen.")
            break


if __name__ == "__main__":
    main()
