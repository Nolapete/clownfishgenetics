"""just a holder for the traits and genotypes of a fish
the constructor can be reformated, as long as self.types holds a dictionary of
trait names to genotype tuples
example entry: {"Picasso": ('P','+')}"""


class fish:
    # example with current input: Picasso would be ('Picasso', ('P', '+'))
    def __init__(self, types):
        self.types = {}
        for t in types:
            self.types[t[0]] = t[1]

    # return our type dictionary
    def get_types(self):
        return self.types


"""given p1 and p2, determine which one should be in front, considering
wildtypes and recessive vs dominant any genotype that starts with a lowercase
letter is considered recssive for this """


def format_allele(p1, p2):
    if p1 == "+":
        if ord(p2[0]) >= ord("a") and ord(p2[0]) <= ord("z"):
            return p1 + "/" + p2
        return p2 + "/" + p1
    elif p2 == "+":
        if ord(p1[0]) >= ord("a") and ord(p1[0]) <= ord("z"):
            return p2 + "/" + p1
    return p1 + "/" + p2


"""uses the properties of an expanded dihybrid cross table to determine the
resultant type ind is a tuple of (x, y) for horizontal and vertical index
length is h where the table is h x h
h_axis is the genotypes along the horizontal axis
v_axis is the genotypes along the vertical axis
h_axis and v_axis should be sorted in the same order"""


def cross_at_index(ind, length, h_axis, v_axis):
    # start_x and start_y are used to determine which
    # genotype to take at a given index
    start_x = length // 2
    start_y = length // 2

    # resulting genotype string
    res = ""

    x = ind[0]
    y = ind[1]

    # the x and y components of the genotype as calculated by the whileloop
    xpart = None
    ypart = None
    # our current index in the axes
    ax_ind = 0
    # while we still have elements left, determine which component to take
    # based on the index
    while start_x > 0:
        if x >= start_x:
            xpart = h_axis[ax_ind][1]
        else:
            xpart = h_axis[ax_ind][0]
        if y >= start_y:
            ypart = v_axis[ax_ind][1]
        else:
            ypart = v_axis[ax_ind][0]

        # cut out full wildtypes
        if xpart != "+" or ypart != "+":
            res += " " + format_allele(xpart, ypart)

        # setup for the next loop
        x %= start_x
        y %= start_y
        start_x //= 2
        start_y //= 2
        ax_ind += 1

    # clear extra whitespace and return the genotype
    return res.strip()


# f1 and f2 are fish objects
def cross_fish(f1, f2):
    f1_types = f1.get_types()
    f1_type_names = f1_types.keys()
    f2_types = f2.get_types()
    f2_type_names = f2_types.keys()

    # find any missing keys from either fish
    f2_missing = list(filter(lambda a: a not in f2_type_names, f1_type_names))
    f1_missing = list(filter(lambda a: a not in f1_type_names, f2_type_names))

    # add in the missing keys
    for n in f1_missing:
        f1_types[n] = ("+", "+")

    for n in f2_missing:
        f2_types[n] = ("+", "+")

    f1_final = []
    f2_final = []
    """based on the ordering of one of the fish dictionaries, create a
    horizontal and vertical axis list the lists need to be in the same order,
    so using one dictionary's ordering ensures this """
    names = list(f1_types.keys())
    for n in names:
        f1_final.append(f1_types[n])
        f2_final.append(f2_types[n])

    # our table grows exponentially with the number of traits to consider
    table_length = 2 ** len(f1_final)

    # for tracking the percentages for each genotype
    total_entries = float(table_length * table_length)
    percent_counter = {}

    # loop through the entire cross table, adding up the percentages
    for x in range(0, table_length):
        for y in range(0, table_length):
            res = cross_at_index((x, y), table_length, f1_final, f2_final)
            if res in percent_counter:
                percent_counter[res] += 100.0 / total_entries
            else:
                percent_counter[res] = 100.0 / total_entries

    return percent_counter


def fmtIt(nm):
    parts = nm.split(' "')
    if len(parts) == 2:
        newnm = "".join([parts[0], ' <i>"', parts[1], "</i>"])
        # print(newnm)
    elif nm.find('"') != -1:
        newnm = parts[0]
    else:
        newnm = "<i>".join([parts[0], "</i>"])

    return newnm


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
                'Amphiprion ocellaris "DaVinci / '
                + 'Fancy White / Gladiator" het. albino'
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
    elif nm.find("percula") != -1:
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


def pheno(genotype, parent1, parent2):
    g1 = genotype.strip()
    p1S = parent1.split()
    p1Q = parent1.split(' "')
    p2S = parent2.split()
    p2Q = parent2.split(' "')
    spP1part1 = parent1.find(" ")
    spP2part1 = parent2.find(" ")
    spP1part2 = parent1.find(" ", spP1part1 + 1)
    spP2part2 = parent2.find(" ", spP2part1 + 1)
    spP1part3 = parent1.find(" ", spP1part2 + 1)
    spP2part3 = parent2.find(" ", spP2part2 + 1)
    p1epigra = parent1.find("Premnas sp. epigrammata")
    p2epigra = parent2.find("Premnas sp. epigrammata")
    p1darwin = parent1.find("Premnas sp. darwin")
    p2darwin = parent2.find("Premnas sp. darwin")
    parents = parent1 + parent2

    if parent1.find("ocellaris") != -1 and parent2.find("ocellaris") != -1:
        pheno = newPhen(
            fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            ),
            g1,
        )

    elif p1S[0] == p2S[0]:
        pheno = p1S[0] + "".join(
            [
                " (",
                fmtIt(" " + parent1[spP1part1 + 1 :]),
                " X",
                fmtIt(" " + parent2[spP2part1 + 1 :]),
                " )",
            ]
        )

    elif parent1.find("percula") != -1 and parent2.find("percula") != -1:
        pheno = newPhen(
            fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            ),
            g1,
        )

    elif parent1 == parent2:
        if (
            parents.find('Amphiprion percula "Picasso"') != -1
            or parents.find('Amphiprion percula "Platinum"') != -1
        ):
            if g1 == "P/+":
                pheno = fmtIt('Amphiprion percula "Picasso"')
            elif g1 == "P/P":
                pheno = fmtIt('Amphiprion percula "Platinum"')
            elif g1 == "+/+":
                pheno = fmtIt("Amphiprion percula")
            else:
                pheno = fmtIt(p1S[0]).join(
                    [
                        " ",
                        fmtIt(p1S[1]),
                        " (",
                        parent1[spP1part2 + 1 :],
                        " X ",
                        parent2[spP2part2 + 1 :],
                        ")",
                    ]
                )

        elif parent1 == 'Amphiprion "Black Ice"':
            if g1 == "Sf/+":
                pheno = fmtIt('Amphiprion ocellaris "Snowflake"')
            elif g1.find("Sf/Sf") != -1:
                pheno = fmtIt('Amphiprion ocellaris "Snowflake Double Dose"*')
            elif g1 == "+/+":
                pheno = fmtIt("Amphiprion (Mocha genetics)")
            else:
                pheno = fmtIt(p1S[0]).join(
                    [
                        " ",
                        fmtIt(p1S[1]),
                        " (",
                        parent1[spP1part2 + 1 :],
                        " X ",
                        parent2[spP2part2 + 1 :],
                        ")",
                    ]
                )

        elif parent1 == 'Premnas biaculeatus "Lightning"':
            if g1 == "L/+":
                pheno = fmtIt('Premnas biaculeatus "Lightning"')
            elif g1.find("L/L") != -1:
                pheno = fmtIt('Premnas biaculeatus "Lightning Double Dose"*')
            elif g1 == "+/+":
                pheno = fmtIt('Premnas biaculeatus "White Stripe"')
            else:
                pheno = fmtIt('Premnas biaculeatus "White Stripe"')

        # elif parent1 == 'Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"':
        #     if g1 == "G/+":
        #         pheno = fmtIt('Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"')
        #     elif g1.find("G/G") != -1:
        #         pheno = fmtIt('Premnas sp. epigrammata "Gold Nugget"')
        #     elif g1 == '+/+':
        #         pheno = fmtIt('Premnas sp. epigrammata "Gold Stripe"')
        #     else:
        #         pheno = fmtIt("Premnas sp. epigrammata".join([' ', parent1[spP1part3:]])

        # elif p1epigra != -1:
        #     pheno = fmtIt("Premnas sp. epigrammata".join([' ', parent1[spP1part3:]])

        # elif p1darwin != -1:
        #     pheno = fmtIt("Premnas sp. darwin".join([' ', parent1[spP1part3:]])
        #
        # elif spP1part2 != -1:
        #     pheno = fmtIt(parent1[0, spP1part2].join([' ', parent1[spP1part2 + 1:]]))
        #
        # else:
        #     pheno = fmtIt(parent1[0, spP1part1].join([' ', parent1[spP1part1 + 1:]])

    elif (
        parents.find('Premnas biaculeatus "Lightning"') != -1
        and parents.find('Premnas biaculeatus "White Stripe') != -1
    ):
        if g1 == "L/+":
            pheno = fmtIt('Premnas biaculeatus "Lightning"')
        else:
            if parent1.find("Lightning") != -1:
                pheno = fmtIt(parent2)
            else:
                pheno = fmtIt(parent1)

    elif (
        parents.find('Premnas biaculeatus "Lightning"') != -1
        and parents.find('Premnas biaculeatus "Morse') != -1
    ):
        if g1 == "L/+":
            pheno = fmtIt('Premnas biaculeatus "Lightning"')
        else:
            if parent1.find("Lightning") != -1:
                pheno = fmtIt(parent2)
            else:
                pheno = fmtIt(parent1)

    elif (
        parents.find("Amphiprion sp. darwin") != -1
        and parents.find('Amphiprion ocellaris "DaVinci / Fancy White / Gladiator"')
        != -1
    ):
        if g1 == "DV/+":
            pheno = fmtIt('Amphiprion "MochaVinci"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Mocha"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Double Black Photon"') != -1
        and parents.find('Amphiprion ocellaris "DaVinci / Fancy White / Gladiator"')
        != -1
    ):
        if g1 == "DV/+":
            pheno = fmtIt('Amphiprion "Dr. DaVinci"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Dr."')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion percula "Picasso"') != -1
        and parents.find('Amphiprion percula "Platinum"') != -1
    ):
        if g1 == "P/+":
            pheno = fmtIt('Amphiprion percula "Picasso"')
        elif g1 == "P/P":
            pheno = fmtIt('Amphiprion percula "Platinum"')
        elif g1 == "+/+":
            pheno = fmtIt("Amphiprion percula")
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )

    # elif parents.find('Premnas sp. epigrammata "Gold Nugget"') != -1 and parents.find('Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"') != -1:
    #     if g1 == "G/+":
    #         pheno = fmtIt('Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"')
    #     elif g1.find("G/G") != -1:
    #         pheno = fmtIt('Premnas sp. epigrammata "Gold Nugget"')
    #     elif g1 == '+/+':
    #         pheno = fmtIt('Premnas sp. epigrammata "Gold Stripe"')
    #     else:
    #         pheno = fmtIt("Premnas sp. epigrammata".join([' ', parent1[spP1part3:]])

    # elif parents.find('Premnas sp. epigrammata "Gold Stripe"') != -1 and parents.find('Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"') != -1:
    #     if g1 == "G/+":
    #         pheno = fmtIt('Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"')
    #     elif g1.find("G/G") != -1:
    #         pheno = fmtIt('Premnas sp. epigrammata "Gold Nugget"')
    #     elif g1 == '+/+':
    #         pheno = fmtIt('Premnas sp. epigrammata "Gold Stripe"')
    #     else:
    #         pheno = fmtIt("Premnas sp. epigrammata".join([' ', parent1[spP1part3:]])

    elif (
        parents.find('Amphiprion "Black Snowflake/Phantom"') != -1
        and parents.find('Amphiprion sp. darwin "Midnight"') != -1
    ):
        if g1 == "Sf/+ N/+":
            pheno = fmtIt('Amphiprion "Midnight Lightning"')
        elif g1 == "Sf/+":
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )
        elif g1 == "N/+":
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )
        elif g1 == "+/+":
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Black Ice"') != -1
        and parents.find('Amphiprion sp. darwin "Midnight"') != -1
    ):
        if g1 == "Sf/+ N/+":
            pheno = fmtIt('Amphiprion "Blacker Lightning"')
        elif g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Blacker Ice"')
        elif g1 == "N/+":
            pheno = fmtIt('Amphiprion "Chocolate Midnight"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Chocolate Mocha"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    parent1[spP1part1 + 1 :],
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Black Ice"') != -1
        and parents.find('Amphiprion sp. darwin "Midnight"') != -1
    ):
        if g1 == "Sf/+ N/+":
            pheno = fmtIt('Amphiprion "Blacker Lightning"')
        elif g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Blacker Ice"')
        elif g1 == "N/+":
            pheno = fmtIt('Amphiprion "Chocolate Midnight"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Chocolate Mocha"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    parent2[spP2part1 + 1 :],
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion ocellaris "Frostbite"') != -1
        and parents.find('Amphiprion "Mocha"') != -1
    ):
        if g1 == "Sf/+ DV/+":
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )
        elif g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Sunset Mocha Snowflake"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Sunset Mocha"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion percula "Picasso"') != -1
        and parents.find('Amphiprion "Black Photon"') != -1
    ):
        if g1 == "P/+":
            pheno = fmtIt('Amphiprion "Picasso Half Black Photon"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Half Black Photon"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion percula "Picasso"') != -1
        and parents.find('Amphiprion "Midnight Black Photon"') != -1
    ):
        if g1 == "P/+":
            pheno = fmtIt('Amphiprion "Picasso Half Black Photon"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Half Black Photon"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion ocellaris "Snowflake"') != -1
        and parents.find("Amphiprion sp. darwin") != -1
    ):
        if g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Black Ice"')
        elif g1 == "+/+":
            pheno = fmtIt("Amphiprion (Mocha genetics)")
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Black Ice"') != -1
        and parents.find("Amphiprion ocellaris") != -1
    ):
        if g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Sunset Mocha Snowflake"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Sunset Mocha"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )

    elif (
        parents.find("Amphiprion polymnus") != -1
        and parents.find("Amphiprion sebae") != -1
    ):
        pheno = fmtIt('Amphiprion "White Tipped"')

    elif (
        parents.find('Amphiprion "Mocha"') != -1
        and parents.find("Amphiprion sp. darwin") != -1
    ):
        pheno = fmtIt('Amphiprion "Chocolate Mocha"')

    elif (
        parents.find('Amphiprion ocellaris "Wide Bar Gladiator"') != -1
        and parents.find("Amphiprion sp. darwin") != -1
    ):
        if g1 == "+/+":
            pheno = fmtIt('Amphiprion "Mocha"')
        else:
            pheno = fmtIt('Amphiprion ocellaris "Wide Bar Mocha Gladiator"*')

    elif (
        parents.find("Amphiprion ocellaris") != -1
        and parents.find("Premnas sp. epigrammata") != -1
    ):
        if g1 == "+/+":
            pheno = fmtIt('Pramphiprion "Blood Orange"')
        else:
            pheno = "(".join([fmtIt('Pramphiprion "Blood Orange"'), ")"])

    elif (
        parents.find('Premnas sp. epigrammata "Gold Nugget"') != -1
        and parents.find('Premnas sp. epigrammata "Gold Stripe"') != -1
    ):
        pheno = fmtIt('Premnas sp. epigrammata "Goldflake / Gold Spot / Gold Rush"')

    elif (
        parents.find("Premnas biaculeatus") != -1
        and parents.find("Premnas sp. epigrammata") != -1
    ):
        if g1 == "+/+":
            pheno = fmtIt('Premnas "White Gold"')
        else:
            pheno = "(".join([fmtIt('Premnas "White Gold"'), ")"])

    elif (
        parents.find("Amphiprion percula") != -1
        and parents.find("Premnas biaculeatus") != -1
    ):
        if g1 == "+/+":
            pheno = fmtIt('Pramphiprion "Citron"')
        else:
            pheno = "(".join([fmtIt('Pramphiprion "Citron"'), ")"])

    elif (
        parents.find("Amphiprion ocellaris") != -1
        and parents.find("Premnas biaculeatus") != -1
    ):
        if g1 == "+/+":
            pheno = fmtIt('Pramphiprion "Mai Tai"')
        else:
            pheno = "(".join([fmtIt('Pramphiprion "Mai Tai"'), ")"])

    elif (
        parents.find("Amphiprion sp. darwin") != -1
        and parents.find("Premnas biaculeatus") != -1
    ):
        if g1 == "+/+":
            pheno = fmtIt('Pramphiprion "Cocoa"')
        else:
            pheno = "(".join([fmtIt('Pramphiprion "Cocoa"'), ")"])

    elif (
        p1S[0] == "Premnas"
        and p2S[0] != "Premnas"
        or p1S[0] != "Premnas"
        and p2S[0] == "Premnas"
    ):
        pheno = fmtIt("Pramphiprion ").join(
            [
                "(",
                fmtIt(parent1[spP1part1 + 1 :]),
                " X ",
                fmtIt(parent2[spP2part1 + 1 :]),
                ")",
            ]
        )

    elif (
        parents.find('Amphiprion chrysopterus "YT/YF Fiji"') != -1
        and parents.find("Amphiprion barberi") != -1
    ):
        pheno = fmtIt('Amphiprion "Red Bee"')

    elif (
        parents.find("Amphiprion ephippium") != -1
        and parents.find("Amphiprion barberi") != -1
    ):
        pheno = fmtIt('Amphiprion "Split-Face"')

    elif (
        parents.find("Amphiprion chrysopterus") != -1
        and parents.find("Amphiprion barberi") != -1
    ):
        pheno = fmtIt('Amphiprion "Maybe??? Red Bee"')

    elif (
        parents.find("Amphiprion ocellaris") != -1
        and parents.find("Amphiprion percula") != -1
    ):
        pheno = fmtIt('Amphiprion "Percularis"')

    elif (
        parents.find("Amphiprion sp. darwin") != -1
        and parents.find("Amphiprion percula") != -1
    ):
        pheno = fmtIt('Amphiprion "Black Photon"')

    elif (
        parents.find("Amphiprion sp. darwin") != -1
        and parents.find('Amphiprion percula "Picasso"') != -1
    ):
        if g1 == "P/+":
            pheno = fmtIt('Amphiprion "Smorcularis/Twilight"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Black Photon"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion sp. darwin "Midnight"') != -1
        and parents.find("Amphiprion percula") != -1
    ):
        pheno = fmtIt('Amphiprion "Midnight Black Photon"')

    elif (
        parents.find('Amphiprion "Black Photon"') != -1
        and parents.find("Amphiprion sp. darwin") != -1
    ):
        pheno = fmtIt('Amphiprion "Double Black Photon"')

    elif (
        parents.find('Amphiprion "Black Photon"') != -1
        and parents.find("Amphiprion percula") != -1
    ):
        pheno = fmtIt('Amphiprion "Half Black Photon"')

    elif (
        parents.find('Amphiprion "Snow Onyx"') != -1
        and parents.find('Amphiprion percula "Picasso"') != -1
    ):
        if g1 == "Sf/+ P/+":
            pheno = fmtIt('Amphiprion "White Knight"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Black Ice"') != -1
        and parents.find("Amphiprion sp. darwin") != -1
    ):
        if g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Blacker Ice"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Chocolate Mocha"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " ",
                    fmtIt(p1S[1]),
                    " (",
                    parent1[spP1part2 + 1 :],
                    " X ",
                    parent2[spP2part2 + 1 :],
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Blacker Ice"') != -1
        and parents.find("Amphiprion sp. darwin") != -1
    ):
        if g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Black Snowflake/Phantom"')
        else:
            if p1darwin == -1:
                pheno = fmtIt(parent1[0], spP1part1).join(
                    [
                        " (",
                        fmtIt(parent1[spP1part1 + 1 :]),
                        " X ",
                        parent2[spP2part1 + 1 :],
                        ")",
                    ]
                )
            else:
                pheno = fmtIt(parent1[0], spP1part1).join(
                    [
                        " (",
                        parent1[spP1part1 + 1 :],
                        " X ",
                        fmtIt(parent2[spP2part1 + 1 :]),
                        ")",
                    ]
                )

    elif (
        parents.find('Amphiprion ocellaris "Snowflake"') != -1
        and parents.find('Amphiprion percula "Picasso"') != -1
    ):
        if g1 == "Sf/+ P/+":
            pheno = fmtIt('Amphiprion "Picassnow"')
        elif g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Snow Onyx"')
        elif g1 == "P/+":
            pheno = fmtIt('Amphiprion "Picasso Percularis"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Percularis"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Midnight Lightning"') != -1
        and parents.find("Amphiprion percula") != -1
    ):
        if g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Snowflake Black Photon"')
        elif g1 == "N/+":
            pheno = fmtIt('Amphiprion "Midnight Black Photon"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Black Photon"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Black Snowflake/Phantom"') != -1
        and parents.find("Amphiprion percula") != -1
    ):
        if g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Snowflake Black Photon"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Black Photon"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Black Snowflake/Phantom"') != -1
        and parents.find('Amphiprion percula "Picasso"') != -1
    ):
        if g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Snowflake Black Photon"')
        elif g1 == "P/+":
            pheno = fmtIt('Amphiprion "Smorcularis/Twilight"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Black Photon"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif (
        parents.find('Amphiprion "Midnight Lightning"') != -1
        and parents.find("Amphiprion percula") != -1
    ):
        if g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Snowflake Black Photon"')
        elif g1 == "N/+":
            pheno = fmtIt('Amphiprion "Midnight Black Photon"')
        elif g1 == "+/+":
            pheno = fmtIt('Amphiprion "Black Photon"')
        else:
            pheno = fmtIt(p1S[0]).join(
                [
                    " (",
                    fmtIt(parent1[spP1part1 + 1 :]),
                    " X ",
                    fmtIt(parent2[spP2part1 + 1 :]),
                    ")",
                ]
            )

    elif p1epigra != -1 and p1epigra == p2epigra:
        pheno = fmtIt("Premnas sp. epigrammata").join(
            [" (", parent1[spP1part3 + 1 :], " X ", parent2[spP2part3:], ")"]
        )

    elif p1darwin != -1 and p1darwin == p2darwin:
        pheno = fmtIt("Amphiprion sp. darwin").join(
            [" (", parent1[spP1part3 + 1 :], " X ", parent2[spP2part3:], ")"]
        )

    elif (
        p1S[0] == p2S[0]
        and p1S[1] == p2S[1]
        and p1S[1] != "sp."
        and p1S.length >= 2
        and p2S.length >= 2
        and (p1Q.length == 1 or p2Q.length == 1)
    ):
        if parent1[spP1part2 + 1 :].find(p1S[1]) == -1:
            momV = parent1[spP1part2 + 1 :]
            dadV = '"Unknown Origin"'
        else:
            momV = '"Unknown Origin"'
            dadV = parent2[spP2part2 + 1 :]

        pheno = fmtIt(p1S[0]).join([" ", fmtIt(p1S[1]), " (", momV, " X ", dadV, ")"])

    elif p1epigra == -1 and p1darwin == -1 and p2epigra != -1:
        pheno = fmtIt(p1S[0]).join(
            [
                " (",
                fmtIt(parent1[spP1part1 + 1 :]),
                " X ",
                fmtIt("sp. epigrammata"),
                parent2[spP2part3:],
                ")",
            ]
        )

    elif p1epigra != -1 and p2epigra == -1 and p2darwin == -1:
        pheno = fmtIt(p1S[0]).join(
            [
                " (",
                fmtIt("sp. epigrammata"),
                parent1[spP1part3:],
                " X ",
                fmtIt(parent2[spP2part1 + 1 :]),
                ")",
            ]
        )

    elif (
        parents.find("Amphiprion ocellaris") != -1
        and parents.find("Amphiprion sp. darwin") != -1
    ) != -1:
        if g1 == "+/+":
            pheno = fmtIt('Amphiprion "Mocha"')
        elif g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Black Ice"')
        else:
            pheno = "(".join([fmtIt('Amphiprion "Mocha"'), ")"])

    elif p1epigra == -1 and p1darwin == -1 and p2darwin != -1:
        pheno = fmtIt(p1S[0]).join(
            [
                " (",
                fmtIt(parent1[spP1part1 + 1 :]),
                " X ",
                fmtIt("sp. darwin"),
                parent2[spP2part3:],
                ")",
            ]
        )

    elif p1darwin != -1 and p2epigra == -1 and p2darwin == -1:
        pheno = fmtIt(p1S[0]).join(
            [
                " (",
                fmtIt("sp. darwin"),
                parent1[spP1part3:],
                " X ",
                fmtIt(parent2[spP2part1 + 1 :]),
                ")",
            ]
        )

    elif (
        parents.find("Amphiprion percula") != -1
        and parents.find("Amphiprion ocellaris") != -1
    ):
        if g1 == "+/+":
            pheno = fmtIt('Amphiprion "Percularis"')
        elif g1 == "Sf/+":
            pheno = fmtIt('Amphiprion "Snow Onyx"')
        else:
            pheno = "(".join([fmtIt('Amphiprion "Percularis"'), ")"])

    # elif p1S[0] == p2S[0] and p1S[1] == p2S[1])):

    # pheno = fmtIt(p1S[0]).join([" ", fmtIt(p1S[1]), " (", parent1[spP1part2 + 1:], " X ", parent2[spP2part2 + 1:], ") TEST1")

    elif parent1[0:spP1part1] != parent2[0:spP2part1]:
        pheno = fmtIt(parent1).join([" X ", fmtIt(parent2)])

    else:
        pheno = fmtIt(parent1).join([" X ", fmtIt(parent2)])

    return pheno


# if __name__ == '__main__' :
#   f1 = fish([('T1', ('SM', '?')), ('T2', ('Z', '?')), ('T3', ('ST','?'))])
#   f2 = fish([('T4', ('S', '?')), ('T5', ('pb', 'pb')), ('T6', ('p', 'p'))])
#   results = cross_fish(f1, f2)
#
# for key in results.keys() :
#   if str(key) == '':
#       print ('+/+: ' + str(results[key]))
#   else:
#       print (str(key) + ': ' + str(results[key]))


# for l in loci:
# t1.append((l.gene, (l.allele1, l.allele2)))

# a.genotype = t1

# f1 = fish(a.genotype)
# f2 = fish(a.genotype)


# a1 = Animal.objects.values_list('phenotype','locus__gene', 'locus__allele1', 'locus__allele2').filter(phenotype='Amphiprion ocellaris "Frostbite"')

# t1 = []
# for a in a1:
#     t1.append((a[1], (a[2], a[3])))
