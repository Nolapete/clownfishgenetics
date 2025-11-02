# newPhen.py
from pyUpdatedto3.fmtIt import fmtIt


def newPhen(nm, geno):
    """
    Generates a new phenotype based on the name and genotype,
    assuming 'fmtIt' is a defined function.
    """
    if "ocellaris" in nm:
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
        elif "Sf/Sf" in geno:
            newnm = fmtIt('Amphiprion ocellaris "Snowflake Double Dose"*')
        else:
            newnm = nm

    elif "percula" in nm:
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
