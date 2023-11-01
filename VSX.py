import os
import csv

def prevod_desetiny_stupne_text(desetinny_tvar):   # prevede stupně v desetinném tvaru na text a vrátí text + stupně, minuty a vteřiny
    stupne = int(desetinny_tvar)
    if abs(stupne) < 10:
        if desetinny_tvar >= 0:
            stupne_text = "+0"+str(stupne)
        else:
            stupne_text = "-0" + str(abs(stupne))
    else:
        if stupne >= 0:
            stupne_text = "+"+str(stupne)
        else:
            stupne_text = str(stupne)

    minuty = int((desetinny_tvar - stupne) * 60)

    sekundy = abs(round((desetinny_tvar - stupne - minuty / 60) * 3600, 2))
    if sekundy < 10:
        text_sekundy = "0"+str(sekundy)
    else:
        text_sekundy = str(sekundy)
    if len(text_sekundy) == 4:
        text_sekundy = text_sekundy + "0"
    elif len(text_sekundy) == 3:
        text_sekundy = text_sekundy + "00"
    elif len(text_sekundy) == 2:
        text_sekundy = text_sekundy + ".00"
    else:
        pass
    minuty = abs(minuty)
    if minuty < 10:
        text_minuty = "0"+str(minuty)
    else:
        text_minuty = str(minuty)
    text = stupne_text + "° " + text_minuty + "' " + text_sekundy + '"'
    cisla = stupne_text + " " + text_minuty + " " + text_sekundy
    vysledek = [text, cisla]
    return vysledek


def prevod_desetiny_hodiny_text(desetinny_tvar):   # prevede hodiny v desetinném tvaru na text a vrátí text + hodiny, minuty a vteřiny
    hodiny = int(desetinny_tvar)
    minuty = int((desetinny_tvar - hodiny) * 60)
    sekundy = round((desetinny_tvar - hodiny - minuty / 60) * 3600, 2)
    if hodiny < 10:
        hodiny_text = "0"+str(hodiny)
    else:
        hodiny_text = str(hodiny)
    if minuty < 10:
        minuty_text = "0"+str(minuty)
    else:
        minuty_text = str(minuty)
    if sekundy < 10:
        sekundy_text = "0"+str(sekundy)
    else:
        sekundy_text = str(sekundy)
    if len(sekundy_text) == 4:
        sekundy_text = sekundy_text + "0"
    elif len(sekundy_text) == 3:
        sekundy_text = sekundy_text + "00"
    elif len(sekundy_text) == 2:
        sekundy_text = sekundy_text + ".00"
    else:
        pass

    text = hodiny_text + "h " + minuty_text + "' " + sekundy_text + '"'
    cisla = hodiny_text + " " + minuty_text + " " + sekundy_text
    vysledek = [text, cisla]
    return vysledek



vsx = []
konec = True
with open(os.path.join("H:", "astro", "B_vsx.txt"), "r", encoding="utf-8") as f:
    for radek in f.readlines():
        id = radek[0:7].strip()
        if konec :
            if id == "-------":
                konec = False
            else:
                jmeno = radek[8:38].strip()
                nazev_souboru = jmeno.replace(".", "_").replace("+", "_").replace("-", "_").replace(" ", "_")
                ra = float(radek[41:50].strip())
                rektascenze = prevod_desetiny_hodiny_text(ra/15)
                de = float(radek[50:60].strip())
                deklinace = prevod_desetiny_stupne_text(de)
                type = radek[61:91].strip()
                mag = radek[94:100].strip()
                epocha = radek[130:142].strip()
                if epocha =="":
                    epocha = "2459000"
                if mag == "":
                    mag = "11.11"
                perioda = radek[147:163].strip()
                if perioda == "":
                    perioda = "1"
                souradnice = (rektascenze[1] + " " + deklinace[1])
                if float(mag) < 13  and float(mag) > 5 and ((type.find("VAR") != -1) or (type.find("VAR") != -1)):    #and float(perioda) <= 0.5:
                    zaznam = [souradnice, rektascenze[0] + " " + deklinace[0], jmeno, nazev_souboru, type, mag, epocha,
                              perioda]
                    vsx.append(zaznam)

with open(os.path.join("H:", "astro", "var.txt"), "w", encoding="utf-8") as l:
    for i in range(len(vsx)):
#       l.write(vsx[i][0] + ";" + vsx[i][1] + ";" + vsx[i][2] + ";" + vsx[i][3] + ";" + vsx[i][4] + ";" + vsx[i][5] + ";" + vsx[i][6] + ";" + vsx[i][7] + "\n")
        l.write(    vsx[i][0] + ";" + vsx[i][2] + ";" + vsx[i][4] + ";" + vsx[i][5] + ";" + vsx[i][6] + ";" + vsx[i][7] + "\n")



