from bs4 import BeautifulSoup
import urllib2

iupac_chemicals = open("IUPACNAMES.txt", 'w')
letters = ["A", "B", "C",  "D", "E","F","G", "H","I", "JK", "L", "M", "N", "O", "P", "Q","R", "S", "T", "U","V", "WX", "Z"]
for i in letters:
    soup = BeautifulSoup(urllib2.urlopen('http://www.thegoodscentscompany.com/upacname-' + i.lower() + '.html').read())

    table = soup.find('table', id= 'alltableList1')
    rows = table.findAll('tr')
    for row in rows[4:-2]:
        cells = row.findAll("td")
        leftShift = cells[1].get_text() #Second Column
        name = cells[2].get_text()
        name= leftShift + name
        if len(name) < 30:
            iupac_chemicals.write(name.encode('utf-8'))
            iupac_chemicals.write("\n")

iupac_chemicals.close()