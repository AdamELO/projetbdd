import xml.etree.ElementTree as ET
tree = ET.parse("data/utilisateurs.xml")
root = tree.getroot()
for u in root.findall("utilisateur"):
    achats = u.find("achats")
    if achats is None:
        continue
    for o in achats.findall("objet"):
        if o.text and "savoir" in o.text.lower():
            print(repr(o.text))