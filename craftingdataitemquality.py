import csv
from slpp import slpp as lua  
craftingdata = {}
with open('Wowdata/CraftingDataItemQuality.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    headers = next(spamreader)
    for row in spamreader:
        if row[headers.index("CraftingDataID")] not in craftingdata:
            craftingdata[row[headers.index("CraftingDataID")]] = []
        craftingdata[row[headers.index("CraftingDataID")]].append(row[headers.index("ItemID")])
        # Some appear out of order, but its probably safer to trust the order provided as being Q1-3 than it is to assume that sequential is always better
        # should really validate against these while building to see which are Q1-3 and pull accordingly
        #craftingdata[row[headers.index("CraftingDataID")]].sort()

outpattern = {}
outpattern["CraftingDataItemQuality"] = craftingdata
with open('out/tmp.lua', 'w') as tmp:
    tmp.writelines(lua.encode(outpattern))

# This would be more effectively done using shell commands, but that isn't helpful until i opt to build CI out
with open('out/tmp.lua', 'r') as cleanfile:
    cleanfile = cleanfile.readlines()[1:-1]
    with open('out/CraftingDataItemQuality.lua', 'w') as luafile:
        luafile.writelines(cleanfile)