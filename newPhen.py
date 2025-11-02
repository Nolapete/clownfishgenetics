import fmtIt


def newPhen(nm, geno):
    if nm.find("ocellaris") != -1:
        if geno == "Sf/+":
            newnm = fmtIt('Amphiprion ocellaris "Snowflake"')
        elif geno == "N/+":
            newnm = fmtIt('Amphiprion ocellaris "Naked"')
        elif geno == "DV/+":
            newnm = fmtIt('Amphiprion ocellaris "DaVinci / Fancy White / Gladiator"')
        elif geno == "DV/+ +/a":
            newnm = fmtIt(
                'Amphiprion ocellaris "DaVinci / Fancy White / Gladiator" het. albino'
            )
        elif geno == "WB/+":
            newnm = fmtIt('Amphiprion ocellaris "Wide Bar Gladiator"')
        elif geno == "Sf/+ DV/+":
            newnm = fmtIt('Amphiprion ocellaris "Frostbite"')
        elif geno == "DV/DV":
            newnm = fmtIt('Amphiprion ocellaris "Wyoming White"')
        elif geno == "+/+":
            newnm = fmtIt("Amphiprion ocellaris")
        elif geno.find("Sf/Sf") != -1:
            newnm = fmtIt('Amphiprion ocellaris "Snowflake Double Dose"*')
        else:
            newnm = nm

    elif nm.indexOf("percula") != -1:
        if geno == "P/P":
            newnm = fmtIt('Amphiprion percula "Platinum"')
        elif geno == "+/+":
            newnm = fmtIt("Amphiprion percula")
        elif geno == "P/+":
            newnm = fmtIt('Amphiprion percula "Picasso"')
        else:
            newnm = nm

    else:
        newnm = nm

    return newnm
