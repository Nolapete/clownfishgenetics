# phenotype.py

from pyUpdatedto3.fmtIt import fmtIt
from pyUpdatedto3.newPhen import newPhen


def pheno(genotype, parent1, parent2):
    g1 = genotype.strip()
    p1S = parent1.split()
    p1Q = parent1.split(' "')
    p2S = parent2.split()
    p2Q = parent2.split(' "')

    # Using find() is safer as it returns -1 if not found.
    spP1part1 = parent1.find(" ")
    spP2part1 = parent2.find(" ")
    spP1part2 = parent1.find(" ", spP1part1 + 1) if spP1part1 != -1 else -1
    spP2part2 = parent2.find(" ", spP2part1 + 1) if spP2part1 != -1 else -1
    spP1part3 = parent1.find(" ", spP1part2 + 1) if spP1part2 != -1 else -1
    spP2part3 = parent2.find(" ", spP2part2 + 1) if spP2part2 != -1 else -1

    p1epigra = "Premnas sp. epigrammata" in parent1
    p2epigra = "Premnas sp. epigrammata" in parent2
    p1darwin = "Premnas sp. darwin" in parent1
    p2darwin = "Premnas sp. darwin" in parent2
    parents = parent1 + parent2
    pheno_val = None

    if "ocellaris" in parent1 and "ocellaris" in parent2:
        pheno_val = newPhen(
            f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})",
            g1,
        )
    elif p1S[0] == p2S[0]:
        pheno_val = f"{fmtIt(' '.join(p1S))} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"
    elif "percula" in parent1 and "percula" in parent2:
        pheno_val = newPhen(
            f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})",
            g1,
        )
    elif parent1 == parent2:
        if ('Amphiprion percula "Picasso"' in parents) or (
            parent1 == 'Amphiprion percula "Platinum"'
        ):
            if g1 == "P/+":
                pheno_val = fmtIt('Amphiprion percula "Picasso"')
            elif g1 == "P/P":
                pheno_val = fmtIt('Amphiprion percula "Platinum"')
            elif g1 == "+/+":
                pheno_val = fmtIt("Amphiprion percula")
            else:
                pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
        elif parent1 == 'Amphiprion "Black Ice"':
            if g1 == "Sf/+":
                pheno_val = fmtIt('Amphiprion ocellaris "Snowflake"')
            elif "Sf/Sf" in g1:
                pheno_val = fmtIt('Amphiprion ocellaris "Snowflake Double Dose"*')
            elif g1 == "+/+":
                pheno_val = f"{fmtIt('Amphiprion')}(Mocha genetics)"
            else:
                pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
        elif parent1 == 'Premnas biaculeatus "Lightning"':
            if g1 == "L/+":
                pheno_val = fmtIt('Premnas biaculeatus "Lightning"')
            elif "L/L" in g1:
                pheno_val = fmtIt('Premnas biaculeatus "Lightning Double Dose"*')
            elif g1 == "+/+":
                pheno_val = fmtIt('Premnas biaculeatus "White Stripe"')
            else:
                pheno_val = fmtIt('Premnas biaculeatus "White Stripe"')
        elif parent1 == 'Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"':
            if g1 == "G/+":
                pheno_val = fmtIt(
                    'Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"'
                )
            elif "G/G" in g1:
                pheno_val = fmtIt('Premnas sp. epigrammata "Gold Nugget"')
            elif g1 == "+/+":
                pheno_val = fmtIt('Premnas sp. epigrammata "Gold Stripe"')
            else:
                pheno_val = f"Premnas sp. epigrammata {parent1[spP1part3:]}"
        elif p1epigra:
            pheno_val = f"Premnas sp. epigrammata {parent1[spP1part3:]}"
        elif p1darwin:
            pheno_val = f"Premnas sp. darwin {parent1[spP1part3:]}"
        elif spP1part2 != -1:
            pheno_val = (
                f"{fmtIt(parent1[0:spP1part2])} {fmtIt(parent1[spP1part2 + 1:])}"
            )
        else:
            pheno_val = (
                f"{fmtIt(parent1[0:spP1part1])} {fmtIt(parent1[spP1part1 + 1:])}"
            )
    elif (
        'Premnas biaculeatus "Lightning"' in parents
        and 'Premnas biaculeatus "White Stripe"' in parents
    ):
        if g1 == "L/+":
            pheno_val = fmtIt('Premnas biaculeatus "Lightning"')
        else:
            if "Lightning" in parent1:
                pheno_val = fmtIt(parent2)
            else:
                pheno_val = fmtIt(parent1)
    elif (
        'Premnas biaculeatus "Lightning"' in parents
        and 'Premnas biaculeatus "Morse"' in parents
    ):
        if g1 == "L/+":
            pheno_val = fmtIt('Premnas biaculeatus "Lightning"')
        else:
            if "Lightning" in parent1:
                pheno_val = fmtIt(parent2)
            else:
                pheno_val = fmtIt(parent1)
    elif (
        "Amphiprion sp. darwin" in parents
        and 'Amphiprion ocellaris "DaVinci / Fancy White / Gladiator"' in parents
    ):
        if g1 == "DV/+":
            pheno_val = fmtIt('Amphiprion "MochaVinci"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Mocha"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
    elif (
        'Amphiprion "Double Black Photon"' in parents
        and 'Amphiprion ocellaris "DaVinci / Fancy White / Gladiator"' in parents
    ):
        if g1 == "DV/+":
            pheno_val = fmtIt('Amphiprion "Dr. DaVinci"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Dr."')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
    elif (
        'Amphiprion percula "Picasso"' in parents
        and 'Amphiprion percula "Platinum"' in parents
    ):
        if g1 == "P/+":
            pheno_val = fmtIt('Amphiprion percula "Picasso"')
        elif g1 == "P/P":
            pheno_val = fmtIt('Amphiprion percula "Platinum"')
        elif g1 == "+/+":
            pheno_val = fmtIt("Amphiprion percula")
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
    elif (
        'Premnas sp. epigrammata "Gold Nugget"' in parents
        and 'Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"' in parents
    ):
        if g1 == "G/+":
            pheno_val = fmtIt(
                'Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"'
            )
        elif "G/G" in g1:
            pheno_val = fmtIt('Premnas sp. epigrammata "Gold Nugget"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Premnas sp. epigrammata "Gold Stripe"')
        else:
            pheno_val = f"Premnas sp. epigrammata {parent1[spP1part3:]}"
    elif (
        'Premnas sp. epigrammata "Gold Stripe"' in parents
        and 'Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"' in parents
    ):
        if g1 == "G/+":
            pheno_val = fmtIt(
                'Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"'
            )
        elif "G/G" in g1:
            pheno_val = fmtIt('Premnas sp. epigrammata "Gold Nugget"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Premnas sp. epigrammata "Gold Stripe"')
        else:
            pheno_val = f"Premnas sp. epigrammata {parent1[spP1part3:]}"
    elif (
        'Amphiprion "Black Snowflake/Phantom"' in parents
        and 'Amphiprion sp. darwin "Midnight"' in parents
    ):
        if g1 == "Sf/+ N/+":
            pheno_val = fmtIt('Amphiprion "Midnight Lightning"')
        elif g1 == "Sf/+":
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
        elif g1 == "N/+":
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
        elif g1 == "+/+":
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
    elif (
        'Amphiprion "Black Ice"' in parents
        and 'Amphiprion sp. darwin "Midnight"' in parents
    ):
        if g1 == "Sf/+ N/+":
            pheno_val = fmtIt('Amphiprion "Blacker Lightning"')
        elif g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Blacker Ice"')
        elif g1 == "N/+":
            pheno_val = fmtIt('Amphiprion "Chocolate Midnight"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Chocolate Mocha"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"
    elif (
        'Amphiprion ocellaris "Frostbite"' in parents
        and 'Amphiprion "Mocha"' in parents
    ):
        if g1 == "Sf/+ DV/+":
            pheno_val = f"{fmtIt(' '.join(p1S))} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"
        elif g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Sunset Mocha Snowflake"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Sunset Mocha"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"
    elif (
        'Amphiprion percula "Picasso"' in parents
        and 'Amphiprion "Black Photon"' in parents
    ):
        if g1 == "P/+":
            pheno_val = fmtIt('Amphiprion "Picasso Half Black Photon"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Half Black Photon"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"
    elif (
        'Amphiprion percula "Picasso"' in parents
        and 'Amphiprion "Midnight Black Photon"' in parents
    ):
        if g1 == "P/+":
            pheno_val = fmtIt('Amphiprion "Picasso Half Black Photon"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Half Black Photon"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"
    elif (
        'Amphiprion ocellaris "Snowflake"' in parents
        and "Amphiprion sp. darwin" in parents
    ):
        if g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Black Ice"')
        elif g1 == "+/+":
            pheno_val = f"{fmtIt('Amphiprion')}(Mocha genetics)"
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
    elif 'Amphiprion "Black Ice"' in parents and "ocellaris" in parents:
        if g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Sunset Mocha Snowflake"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Sunset Mocha"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
    elif "Amphiprion polymnus" in parents and "Amphiprion sebae" in parents:
        pheno_val = fmtIt('Amphiprion "White Tipped"')
    elif 'Amphiprion "Mocha"' in parents and "Amphiprion sp. darwin" in parents:
        pheno_val = fmtIt('Amphiprion "Chocolate Mocha"')
    elif (
        'Amphiprion ocellaris "Wide Bar Gladiator"' in parents
        and "Amphiprion sp. darwin" in parents
    ):
        if g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Mocha"')
        else:
            pheno_val = fmtIt('Amphiprion ocellaris "Wide Bar Mocha Gladiator"*')
    elif "ocellaris" in parents and "epigrammata" in parents:
        if g1 == "+/+":
            pheno_val = fmtIt('Pramphiprion "Blood Orange"')
        else:
            pheno_val = f"({fmtIt('Pramphiprion \"Blood Orange\"')})"
    elif (
        'Premnas sp. epigrammata "Gold Nugget"' in parents
        and 'Premnas sp. epigrammata "Gold Stripe"' in parents
    ):
        pheno_val = fmtIt('Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"')
    elif "biaculeatus" in parents and "epigrammata" in parents:
        if g1 == "+/+":
            pheno_val = fmtIt('Premnas "White Gold"')
        else:
            pheno_val = f"({fmtIt('Premnas \"White Gold\"')})"
    elif "percula" in parents and "biaculeatus" in parents:
        if g1 == "+/+":
            pheno_val = fmtIt('Pramphiprion "Citron"')
        else:
            pheno_val = f"({fmtIt('Pramphiprion \"Citron\"')})"
    elif "ocellaris" in parents and "biaculeatus" in parents:
        if g1 == "+/+":
            pheno_val = fmtIt('Pramphiprion "Mai Tai"')
        else:
            pheno_val = f"({fmtIt('Pramphiprion \"Mai Tai\"')})"
    elif "darwin" in parents and "biaculeatus" in parents:
        if g1 == "+/+":
            pheno_val = fmtIt('Pramphiprion "Cocoa"')
        else:
            pheno_val = f"({fmtIt('Pramphiprion \"Cocoa\"')})"
    elif (p1S[0] == "Premnas" and p2S[0] != "Premnas") or (
        p1S[0] != "Premnas" and p2S[0] == "Premnas"
    ):
        pheno_val = f"{fmtIt('Pramphiprion ')} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"
    elif (
        'Amphiprion chrysopterus "YT/YF Fiji"' in parents
        and "Amphiprion barberi" in parents
    ):
        pheno_val = fmtIt('Amphiprion "Red Bee"')
    elif "Amphiprion ephippium" in parents and "Amphiprion barberi" in parents:
        pheno_val = fmtIt('Amphiprion "Split-Face"')
    elif "Amphiprion chrysopterus" in parents and "Amphiprion barberi" in parents:
        pheno_val = fmtIt('Amphiprion "Maybe??? Red Bee"')
    elif "ocellaris" in parents and "percula" in parents:
        pheno_val = fmtIt('Amphiprion "Percularis"')
    elif "Amphiprion sp. darwin" in parents and "percula" in parents:
        pheno_val = fmtIt('Amphiprion "Black Photon"')
    elif (
        "Amphiprion sp. darwin" in parents and 'Amphiprion percula "Picasso"' in parents
    ):
        if g1 == "P/+":
            pheno_val = fmtIt('Amphiprion "Smorcularis/Twilight"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Black Photon"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"
    elif 'Amphiprion sp. darwin "Midnight"' in parents and "percula" in parents:
        pheno_val = fmtIt('Amphiprion "Midnight Black Photon"')
    elif 'Amphiprion "Black Photon"' in parents and "Amphiprion sp. darwin" in parents:
        pheno_val = fmtIt('Amphiprion "Double Black Photon"')
    elif 'Amphiprion "Black Photon"' in parents and "percula" in parents:
        pheno_val = fmtIt('Amphiprion "Half Black Photon"')
    elif (
        'Amphiprion "Snow Onyx"' in parents
        and 'Amphiprion percula "Picasso"' in parents
    ):
        if g1 == "Sf/+ P/+":
            pheno_val = fmtIt('Amphiprion "White Knight"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"
    elif 'Amphiprion "Black Ice"' in parents and "Amphiprion sp. darwin" in parents:
        if g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Blacker Ice"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Chocolate Mocha"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} {fmtIt(' '.join(p1S))} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]})"
    elif 'Amphiprion "Blacker Ice"' in parents and "Amphiprion sp. darwin" in parents:
        if g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Black Snowflake/Phantom"')
        else:
            if not p1darwin:
                pheno_val = f"{fmtIt(parent1[0:spP1part1])} ({fmtIt(parent1[spP1part1 + 1:])} X {parent2[spP2part1 + 1:]})"
            else:
                pheno_val = f"{fmtIt(parent1[0:spP1part1])} ({parent1[spP1part1 + 1:]} X {fmtIt(parent2[spP2part1 + 1:])})"
    elif (
        'Amphiprion ocellaris "Snowflake"' in parents
        and 'Amphiprion percula "Picasso"' in parents
    ):
        if g1 == "Sf/+ P/+":
            pheno_val = fmtIt('Amphiprion "Picassnow"')
        elif g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Snow Onyx"')
        elif g1 == "P/+":
            pheno_val = fmtIt('Amphiprion "Picasso Percularis"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Percularis"')
        else:
            pheno_val = f"{fmtIt(' '.join(p1S))} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"

    elif 'Amphiprion "Midnight Lightning"' in parents and "percula" in parents:
        if g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Snowflake Black Photon"')
        elif g1 == "N/+":
            pheno_val = fmtIt('Amphiprion "Midnight Black Photon"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Black Photon"')
        else:
            pheno_val = f"{fmtIt(p1S[0])} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"

    elif 'Amphiprion "Black Snowflake/Phantom"' in parents and "percula" in parents:
        if g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Snowflake Black Photon"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Black Photon"')
        else:
            pheno_val = f"{fmtIt(p1S[0])} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"

    elif (
        'Amphiprion "Black Snowflake/Phantom"' in parents
        and 'Amphiprion percula "Picasso"' in parents
    ):
        if g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Snowflake Black Photon"')
        elif g1 == "P/+":
            pheno_val = fmtIt('Amphiprion "Smorcularis/Twilight"')
        elif g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Black Photon"')
        else:
            pheno_val = f"{fmtIt(p1S[0])} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt(parent2[spP2part1 + 1:])})"

    elif p1darwin and p1darwin == p2darwin:
        pheno_val = f"{fmtIt('Amphiprion sp. darwin')} ({parent1[spP1part3 + 1:]} X {parent2[spP2part3:]})"

    elif (
        p1S[0] == p2S[0]
        and p1S[1] == p2S[1]
        and p1S[1] != "sp."
        and len(p1S) >= 2
        and len(p2S) >= 2
        and (len(p1Q) == 1 or len(p2Q) == 1)
    ):
        momV, dadV = "", ""
        if parent1[spP1part2 + 1 :].find(p1S[1]) == -1:
            momV = parent1[spP1part2 + 1 :]
            dadV = '"Unknown Origin"'
        else:
            momV = '"Unknown Origin"'
            dadV = parent2[spP2part2 + 1 :]
        pheno_val = f"{fmtIt(p1S[0])} {fmtIt(p1S[1])} ({momV} X {dadV})"

    elif not p1epigra and not p1darwin and p2epigra:
        pheno_val = f"{fmtIt(p1S[0])} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt('sp. epigrammata')} {parent2[spP2part3:]})"

    elif p1epigra and not p2epigra and not p2darwin:
        pheno_val = f"{fmtIt(p1S[0])} ({fmtIt('sp. epigrammata')} {parent1[spP1part3:]} X {fmtIt(parent2[spP2part1 + 1:])})"

    elif "Amphiprion ocellaris" in parents and "Amphiprion sp. darwin" in parents:
        if g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Mocha"')
        elif g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Black Ice"')
        else:
            pheno_val = f"({fmtIt('Amphiprion \"Mocha\"')})"

    elif not p1epigra and not p1darwin and p2darwin:
        pheno_val = f"{fmtIt(p1S[0])} ({fmtIt(parent1[spP1part1 + 1:])} X {fmtIt('sp. darwin')} {parent2[spP2part3:]})"

    elif p1darwin and not p2epigra and not p2darwin:
        pheno_val = f"{fmtIt(p1S[0])} ({fmtIt('sp. darwin')} {parent1[spP1part3:]} X {fmtIt(parent2[spP2part1 + 1:])})"

    elif "Amphiprion percula" in parents and "Amphiprion ocellaris" in parents:
        if g1 == "+/+":
            pheno_val = fmtIt('Amphiprion "Percularis"')
        elif g1 == "Sf/+":
            pheno_val = fmtIt('Amphiprion "Snow Onyx"')
        else:
            pheno_val = f"({fmtIt('Amphiprion \"Percularis\"')})"

    elif p1S[0] == p2S[0] and p1S[1] == p2S[1]:
        pheno_val = f"{fmtIt(p1S[0])} {fmtIt(p1S[1])} ({parent1[spP1part2 + 1:]} X {parent2[spP2part2 + 1:]}) TEST1"
    elif parent1[0:spP1part1] != parent2[0:spP2part1]:
        pheno_val = f"{fmtIt(parent1)} X {fmtIt(parent2)}"
    else:
        pheno_val = "Unknown phenotype"

    return pheno_val
