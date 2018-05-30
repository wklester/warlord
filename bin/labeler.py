import re
import os

f = open('next.dat')
for cardname in iter(f):
    cardname = cardname.rstrip('\n')
    cardname = cardname.replace("'", "`")
    cardname = re.escape(cardname)
    # print(cardname)
    this = '\"Nickname\": \"\",'
    that = '\"Nickname\": \"' + cardname + '\",'
    sedcommand = "sed -i '0,/" + this + "/s//" + that + "/' current.json"
    # print(sedcommand)
    os.system(sedcommand)
f.close()

sedcommand = "sed -i \"s/\`/'/g\" current.json"
os.system(sedcommand)
