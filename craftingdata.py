import csv
from slpp import slpp as lua  
craftingdata = {}
with open('Wowdata/CraftingData.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    headers = next(spamreader)
    for row in spamreader:
        if int(row[headers.index("CraftedItemID")]) > 0:
            craftingdata[int(row[headers.index("ID")])] = row[int(headers.index("CraftedItemID"))]


outpattern = {}
outpattern["CraftingData"] = craftingdata
with open('out/tmp.lua', 'w') as tmp:
    tmp.writelines(lua.encode(outpattern))

# This would be more effectively done using shell commands, but that isn't helpful until i opt to build CI out
with open('out/tmp.lua', 'r') as cleanfile:
    cleanfile = cleanfile.readlines()[1:-1]
    with open('out/CraftingData.lua', 'w') as luafile:
        luafile.writelines(cleanfile)