# from nolapete.models import Animal


def fmtIt(nm):
    parts = nm.split(' "')
    if len(parts) == 2:
        newnm = "<i>".join([parts[0], "</i>", ' "', parts[1]])
    elif nm.find('"') != -1:
        newnm = parts[0]
    else:
        newnm = "<i>".join([parts[0], "</i>"])

    return newnm


# animals = Animal.objects.all()
# for a in animals:
#     print(fmtIt(a.phenotype))
