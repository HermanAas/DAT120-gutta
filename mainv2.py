import datetime
import calendar
import math
import matplotlib.pyplot as plt

VÆRSTASJONER = {
    "Oslo Blindern": "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": "tromsoe_1954_2025_med_makstemperatur.csv",
    "Værnes": "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": "venabu_1954_2025_med_makstemperatur.csv",
    "Sinnes": "sinnes_2014_2025_med_makstemperatur.csv"
}

#Gjør en verdi fra CSV-filen om til et tall.
def les_tall(verdi):
    verdi = verdi.strip().replace(",", ".")

    if verdi == "" or verdi == "-":
        return None
    
    try:
        return float(verdi)
    except ValueError:
        return None


#Leser værdata fra en CSV-fil og returnerer en liste med dictionaries.
def les_data(filnavn):
    data = []

    with open(filnavn, "r", encoding="utf-8-sig") as fil:
        next(fil, None)  # Hopper over overskriftsraden

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

    data.sort(key=lambda rad: rad["dato"])
    return data


#Henter data for en valgt værstasjon.
def hent_stasjonsdata(stasjonsnavn):
    filnavn = VÆRSTASJONER[stasjonsnavn]
    return les_data(filnavn)


#Lar brukeren velge en værstasjon.
def velg_værstasjon():
    navn = list(VÆRSTASJONER.keys())

    print("\nVelg værstasjon:")
    for i, stasjon in enumerate(navn, start=1):
        print(f"{i} - {stasjon}")

    valg = input("Velg stasjon: ").strip()

    try:
        indeks = int(valg) - 1
        if 0 <= indeks < len(navn):
            return navn[indeks]
    except ValueError:
        pass

    print("Ugyldig valg.")
    return None


# OPPGAVE A: MÅNEDLIG PLOTTING OG AGGREGERING
def grupper_per_måned(data): #Samler målinger etter år og måned.
    måneder = {}

    for rad in data:
        dato = rad["dato"]
        nøkkel = (dato.year, dato.month)

        if nøkkel not in måneder:
            måneder[nøkkel] = {
                "snø": [],
                "nedbør": [],
                "temperatur": [],
                "vind": []
            }

        if rad["snodybde"] is not None:
            måneder[nøkkel]["snø"].append(rad["snodybde"])

        if rad["nedbor"] is not None:
            måneder[nøkkel]["nedbør"].append(rad["nedbor"])

        if rad["temperatur"] is not None:
            måneder[nøkkel]["temperatur"].append(rad["temperatur"])

        if rad["vind"] is not None:
            måneder[nøkkel]["vind"].append(rad["vind"])

    resultat = []

    for nøkkel in sorted(måneder):
        verdier = måneder[nøkkel]
        snø = verdier["snø"]
        nedbør = verdier["nedbør"]
        temperatur = verdier["temperatur"]
        vind = verdier["vind"]

        resultat.append({
            "dato": datetime.datetime(nøkkel[0], nøkkel[1], 1),
            "maks_snø": max(snø) if snø else None,
            "total_nedbør": sum(nedbør) if len(nedbør) > 20 else None,
            "maks_temp": max(temperatur) if temperatur else None,
            "min_temp": min(temperatur) if temperatur else None,
            "maks_vind": max(vind) if vind else None
        })

    return resultat


def plott_månedlige_data(stasjonsnavn):
    data = hent_stasjonsdata(stasjonsnavn)
    månedlige_data = grupper_per_måned(data)

    if not månedlige_data:
        print("Fant ingen data for denne værstasjonen.")
        return

    datoer = [rad["dato"] for rad in månedlige_data]
    snø = [rad["maks_snø"] for rad in månedlige_data]
    nedbør = [rad["total_nedbør"] for rad in månedlige_data]
    maks_temp = [rad["maks_temp"] for rad in månedlige_data]
    min_temp = [rad["min_temp"] for rad in månedlige_data]
    vind = [rad["maks_vind"] for rad in månedlige_data]

    fig, akser = plt.subplots(4, 1, figsize=(15, 12), sharex=True)

    akser[0].plot(datoer, snø)
    akser[0].set_title("Maksimal snødybde per måned")
    akser[0].set_ylabel("Snødybde (cm)")
    akser[0].grid(True)

    akser[1].plot(datoer, nedbør)
    akser[1].set_title("Total nedbør per måned")
    akser[1].set_ylabel("Nedbør (mm)")
    akser[1].grid(True)

    akser[2].plot(datoer, maks_temp, label="Maksimum")
    akser[2].plot(datoer, min_temp, label="Minimum")
    akser[2].set_title("Maksimum og minimum middeltemperatur")
    akser[2].set_ylabel("Temperatur (°C)")
    akser[2].legend()
    akser[2].grid(True)

    akser[3].plot(datoer, vind)
    akser[3].set_title("Maksimal middelvind per måned")
    akser[3].set_ylabel("Vind (m/s)")
    akser[3].set_xlabel("År")
    akser[3].grid(True)

    fig.suptitle(f"Månedlige værdata fra {stasjonsnavn}", fontsize=16)
    fig.autofmt_xdate(rotation=30, ha="right")
    fig.tight_layout()
    plt.show()


# OPPGAVE B: SOMMERDAGER, HØYSOMMERDAGER OG TROPEDAGER
def tell_varme_dager_per_år(data): #Teller varme dager for hvert år.
    telling = {}

    for rad in data:
        år = rad["dato"].year
        temperatur = rad["maks_temp"]

        if år not in telling:
            telling[år] = {
                "sommerdager": 0,
                "høysommerdager": 0,
                "tropedager": 0
            }

        if temperatur is None:
            continue

        if temperatur > 20:
            telling[år]["sommerdager"] += 1

        if temperatur > 25:
            telling[år]["høysommerdager"] += 1

        if temperatur > 30:
            telling[år]["tropedager"] += 1

    return telling


def plott_varme_dager():
    fig, akse = plt.subplots(figsize=(13, 6))
    fant_data = False

    for stasjonsnavn in VÆRSTASJONER:
        try:
            data = hent_stasjonsdata(stasjonsnavn)
        except FileNotFoundError:
            print(f"Fant ikke filen for {stasjonsnavn}. Hopper over stasjonen.")
            continue

        telling = tell_varme_dager_per_år(data)

        if not telling:
            continue

        år = sorted(telling)
        sommer = [telling[a]["sommerdager"] for a in år]

        # Oppgaven krever minst Oslo Blindern. Vi plotter sommerdager
        # for alle stasjonene for å gjøre sammenlikningen oversiktlig.
        akse.plot(år, sommer, marker=".", label=stasjonsnavn)
        fant_data = True

    if not fant_data:
        print("Fant ingen data å plotte.")
        plt.close(fig)
        return

    akse.set_title("Antall sommerdager per år")
    akse.set_xlabel("År")
    akse.set_ylabel("Antall dager med maksimumstemperatur over 20 °C")
    akse.grid(True)
    akse.legend()
    fig.tight_layout()
    plt.show()

    # Eget plott for Oslo Blindern med alle tre dagtypene.
    if "Oslo Blindern" in VÆRSTASJONER:
        try:
            oslo_data = hent_stasjonsdata("Oslo Blindern")
            oslo_telling = tell_varme_dager_per_år(oslo_data)

            år = sorted(oslo_telling)
            fig, akse = plt.subplots(figsize=(13, 6))

            akse.plot(
                år,
                [oslo_telling[a]["sommerdager"] for a in år],
                marker="o",
                label="Sommerdager (> 20 °C)"
            )
            akse.plot(
                år,
                [oslo_telling[a]["høysommerdager"] for a in år],
                marker="o",
                label="Høysommerdager (> 25 °C)"
            )
            akse.plot(
                år,
                [oslo_telling[a]["tropedager"] for a in år],
                marker="o",
                label="Tropedager (> 30 °C)"
            )

            akse.set_title("Varme dager per år – Oslo Blindern")
            akse.set_xlabel("År")
            akse.set_ylabel("Antall dager")
            akse.grid(True)
            akse.legend()
            fig.tight_layout()
            plt.show()
        except FileNotFoundError:
            print("Fant ikke CSV-filen for Oslo Blindern.")


# OPPGAVE C: GJENNOMSNITTSTEMPERATUR PER ÅR
def gjennomsnittstemperatur_per_år(data):
    """Beregner årsgjennomsnitt når minst 300 dager har gyldig temperatur."""
    temperaturer = {}

    for rad in data:
        år = rad["dato"].year
        temperatur = rad["temperatur"]

        if temperatur is not None:
            if år not in temperaturer:
                temperaturer[år] = []
            temperaturer[år].append(temperatur)

    resultat = {}

    for år, verdier in temperaturer.items():
        if len(verdier) >= 300:
            resultat[år] = sum(verdier) / len(verdier)

    return resultat


def plott_temperatursammenlikning():
    fig, akse = plt.subplots(figsize=(14, 7))
    fant_data = False

    for stasjonsnavn in VÆRSTASJONER:
        try:
            data = hent_stasjonsdata(stasjonsnavn)
        except FileNotFoundError:
            print(f"Fant ikke filen for {stasjonsnavn}. Hopper over stasjonen.")
            continue

        gjennomsnitt = gjennomsnittstemperatur_per_år(data)

        if not gjennomsnitt:
            continue

        år = sorted(gjennomsnitt)
        temperatur = [gjennomsnitt[a] for a in år]

        akse.plot(år, temperatur, marker=".", label=stasjonsnavn)
        fant_data = True

    if not fant_data:
        print("Fant ingen år med minst 300 gyldige temperaturmålinger.")
        plt.close(fig)
        return

    akse.set_title("Årlig gjennomsnittstemperatur for værstasjonene")
    akse.set_xlabel("År")
    akse.set_ylabel("Gjennomsnittstemperatur (°C)")
    akse.grid(True)
    akse.legend()
    fig.tight_layout()
    plt.show()


# OPPGAVE D: MINIMUM, MEDIAN OG MAKSIMUM VIND PER MÅNED
def median(liste): #Beregner median uten å bruke statistics-modulen.
    sortert = sorted(liste)
    antall = len(sortert)

    if antall == 0:
        return None

    midten = antall // 2

    if antall % 2 == 1:
        return sortert[midten]

    return (sortert[midten - 1] + sortert[midten]) / 2


def vindstatistikk_per_måned(data): #Samler vindmålinger etter kalendermåned, uten å skille mellom år.
    vind_per_måned = {måned: [] for måned in range(1, 13)}

    for rad in data:
        vind = rad["vind"]

        if vind is not None:
            måned = rad["dato"].month
            vind_per_måned[måned].append(vind)

    resultat = {}

    for måned, verdier in vind_per_måned.items():
        if verdier:
            resultat[måned] = {
                "min": min(verdier),
                "median": median(verdier),
                "maks": max(verdier)
            }

    return resultat


def plott_vindstatistikk(stasjonsnavn):
    data = hent_stasjonsdata(stasjonsnavn)
    statistikk = vindstatistikk_per_måned(data)

    måneder = sorted(statistikk)

    if not måneder:
        print("Fant ingen vindmålinger.")
        return

    min_vind = [statistikk[m]["min"] for m in måneder]
    median_vind = [statistikk[m]["median"] for m in måneder]
    maks_vind = [statistikk[m]["maks"] for m in måneder]

    navn_på_måneder = [
        calendar.month_name[m] for m in måneder
    ]

    fig, akse = plt.subplots(figsize=(12, 6))
    akse.plot(navn_på_måneder, min_vind, marker="o", label="Minimum")
    akse.plot(navn_på_måneder, median_vind, marker="o", label="Median")
    akse.plot(navn_på_måneder, maks_vind, marker="o", label="Maksimum")

    akse.set_title(f"Vindstatistikk per måned – {stasjonsnavn}")
    akse.set_xlabel("Måned")
    akse.set_ylabel("Vindstyrke (m/s)")
    akse.grid(True)
    akse.legend()
    fig.tight_layout()
    plt.show()


# OPPGAVE E: ANTALL DAGER MED SKIFØRE PER SKISESONG
def tell_skiforedager_per_sesong(data):
    """
    Skisesongen regnes her fra 1. november til 31. mai.
    Skiføre betyr snødybde på minst 20 cm.

    Et sesongresultat tas bare med dersom minst halvparten av
    kalenderdagene i sesongen har en gyldig snødybdemåling.
    Sesongåret er året sesongen avsluttes i, f.eks. 2020 betyr
    november 2019 til og med mai 2020.
    """
    sesonger = {}

    for rad in data:
        dato = rad["dato"]
        snø = rad["snodybde"]

        if dato.month >= 11:
            sesongår = dato.year + 1
        elif dato.month <= 5:
            sesongår = dato.year
        else:
            continue

        if sesongår not in sesonger:
            sesonger[sesongår] = {
                "gyldige_dager": 0,
                "skiforedager": 0
            }

        if snø is not None:
            sesonger[sesongår]["gyldige_dager"] += 1

            if snø >= 20:
                sesonger[sesongår]["skiforedager"] += 1

    resultat = {}

    for sesongår, verdier in sesonger.items():
        startår = sesongår - 1
        antall_dager = (
            (datetime.date(sesongår, 6, 1) -
             datetime.date(startår, 11, 1)).days
        )
        minimum_gyldige = math.ceil(antall_dager / 2)

        if verdier["gyldige_dager"] >= minimum_gyldige:
            resultat[sesongår] = verdier["skiforedager"]

    return resultat


def plott_skiforedager():
    fig, akse = plt.subplots(figsize=(14, 7))
    fant_data = False

    for stasjonsnavn in VÆRSTASJONER:
        try:
            data = hent_stasjonsdata(stasjonsnavn)
        except FileNotFoundError:
            print(f"Fant ikke filen for {stasjonsnavn}. Hopper over stasjonen.")
            continue

        sesonger = tell_skiforedager_per_sesong(data)

        if not sesonger:
            continue

        år = sorted(sesonger)
        dager = [sesonger[a] for a in år]

        akse.plot(år, dager, marker="o", label=stasjonsnavn)
        fant_data = True

    if not fant_data:
        print("Fant ingen komplette nok skisesonger å plotte.")
        plt.close(fig)
        return

    akse.set_title("Antall dager med skiføre per skisesong")
    akse.set_xlabel("Sesong (året sesongen avsluttes)")
    akse.set_ylabel("Antall dager med minst 20 cm snø")
    akse.grid(True)
    akse.legend()
    fig.tight_layout()
    plt.show()


# ---------------------------------------------------------
# HOVEDMENY
# ---------------------------------------------------------

def main():
    while True:
        print("\n========== DAT120 – VÆRDATA ==========")
        print("1 - Oppgave a: Månedlige værdata og plotting")
        print("2 - Oppgave b: Sommerdager, høysommerdager og tropedager")
        print("3 - Oppgave c: Sammenlikne årstemperaturer")
        print("4 - Oppgave d: Vindstatistikk per måned")
        print("5 - Oppgave e: Dager med skiføre per sesong")
        print("0 - Avslutt")

        valg = input("Velg oppgave: ").strip()

        try:
            if valg == "0":
                print("Programmet avsluttes.")
                break

            elif valg == "1":
                stasjon = velg_værstasjon()
                if stasjon is not None:
                    plott_månedlige_data(stasjon)

            elif valg == "2":
                plott_varme_dager()

            elif valg == "3":
                plott_temperatursammenlikning()

            elif valg == "4":
                stasjon = velg_værstasjon()
                if stasjon is not None:
                    plott_vindstatistikk(stasjon)

            elif valg == "5":
                plott_skiforedager()

            else:
                print("Ugyldig valg. Velg et tall fra menyen.")

        except FileNotFoundError as feil:
            print("Fant ikke en CSV-fil:", feil.filename)
            print("Kontroller at Python-filen og CSV-filene ligger i samme mappe.")

        except KeyboardInterrupt:
            print("\nProgrammet avsluttes.")
            break


if __name__ == "__main__":
    main()
