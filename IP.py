# dec to bin

def Check(IP):
    gtfo = False
    letters = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    while not (gtfo):
        dotcount = 0
        for i in IP:
            if i in letters:
                gtfo = False
            else:
                gtfo = True
            if i == ".":
                dotcount += 1
            if dotcount != 3:
                gtfo = False
        if not (gtfo):
            IP = raw_input("Give IP again: ")
    return IP


def Separate(IP):
    again = True
    check = False
    while again:
        IPlist = []
        IPtest = []
        for k in IP:
            IPtest.append(k)
        for i in range(4):
            num = ""
            while len(IPtest) != 0 and IPtest[0] != ".":
                num += IPtest[0]
                IPtest.pop(0)
            if len(IPtest) > 0:
                IPtest.pop(0)
            IPlist.append(num)
        again = False
        for i in range(len(IPlist)):
            digit = int(IPlist[i])
            IPlist[i] = digit
            if digit > 256 or digit < 0:
                check = True
            else:
                again = False
        if check:
            IP = raw_input("Give IP again again: ")
            IP = Check(IP)
            again = True
            check = False
            IPlist, IPtest = [], []
    return IPlist


def choice():
    answer = raw_input(
        "Do you want to split your network into more subnetworks depending on the amount of PCs or amount of Subnetworks? [PC/Sub]: ")
    while answer != "PC" and answer != "Sub":
        answer = raw_input("[PC/Sub]: ")
    if answer == "PC":
        new = input("How many devices do you want your new subnetworks to at least have?: ")
    else:
        new = input("How many subnetworks do you want to at least have?: ")
    return answer, new


def subnet(answer, new):
    newsubnetmask = ""
    if answer == "PC":
        found = False
        zeros = 0
        while not found:
            if 2 ** zeros - 2 >= new:
                found = True
            else:
                zeros += 1
        newcidr = cidr + (32 - cidr - zeros)
        new = 32 - cidr - zeros
    else:
        found = False
        ones = 0
        while not found:
            if 2 ** ones >= new:
                found = True
            else:
                ones += 1
        newcidr = cidr + ones
        new = ones

    for i in range(1, newcidr + 1):
        newsubnetmask += "1"
        if i % 8 == 0:
            newsubnetmask += "."
    for i in range(newcidr + 1, 33):
        newsubnetmask += "0"
        if i % 8 == 0 and i != 32:
            newsubnetmask += "."

    return newsubnetmask, newcidr, new


def access(cidr, newcidr, newdigits, dec, mask):
    subnetsum = 2 ** (newcidr - cidr)
    print "Your network has been divided to", subnetsum, "subnetworks"
    answer = input("Which subnetwork do you want to get information from? [1-x]: ")
    num = answer - 1
    IPdigitlist = []
    maskdigitlist = []
    subnetIPlist = []
    subnetIPbroadcastlist = []
    tempstr = ""
    subnetIP = ""
    subnetIPbroadcast = ""
    c = 0
    for n in dec:
        if n != ".":
            IPdigitlist.append(n)
    for n in mask:
        if n != ".":
            maskdigitlist.append(n)

    for j in range(newdigits-1, -1, -1):
        if num / 2 ** j > 0:
            tempstr += "1"
            num -= 2 ** j
        else:
            tempstr += "0"

    for i in range(cidr):
        if IPdigitlist[i] == maskdigitlist[i]:
            subnetIPlist.append(maskdigitlist[i])
        else:
            subnetIPlist.append("0")

    for i in range(cidr + 1, cidr + len(tempstr) + 1):
        subnetIPlist.append(tempstr[c])
        c += 1

    for n in subnetIPlist:
        subnetIPbroadcastlist.append(n)

    start = cidr + len(tempstr)
    for i in range(start, 32):
        if i % 8 == 0 and i < 32:
            subnetIPlist.append(".")
            subnetIPbroadcastlist.append(".")
        subnetIPlist.append("0")
        subnetIPbroadcastlist.append("1")

    for i in range(8, 35, 9):
        subnetIPbroadcastlist.insert(i, ".")
        subnetIPlist.insert(i, ".")

    for l in subnetIPlist:
        subnetIP += l
    for l in subnetIPbroadcastlist:
        subnetIPbroadcast += l

    return subnetIP, subnetIPbroadcast


again = True
num = ""

IP = raw_input("Give IP: ")

IP = Check(IP)
IPlist = Separate(IP)

cidr = input("Please enter the CIDR 1-30 (for subnetting): ")


netmasks = ""

for i in range(1, cidr + 1):
    netmasks += "1"
    if i % 8 == 0:
        netmasks += "."
for i in range(cidr + 1, 33):
    netmasks += "0"
    if i % 8 == 0 and i != 32:
        netmasks += "."

dec = []

for i in range(4):
    tempstr = ""
    num = IPlist[i]
    for j in range(7, -1, -1):
        if num / 2 ** j > 0:
            tempstr += "1"
            num -= 2 ** j
        else:
            tempstr += "0"
    dec.append(tempstr)

deccomplete = ""

for i in range(len(dec)):
    deccomplete += dec[i]
    if i != 3:
        deccomplete += "."

print "IP Address in decimal: ", deccomplete
print "Your net mask is: ", netmasks

answer, newnumber = choice()
newmask, newcidr, newdigits = subnet(answer, newnumber)
subnetIP, subnetIPbroadcast = access(cidr, newcidr, newdigits, deccomplete, netmasks)
print "Your subnetwork IP is: ", subnetIP
print "Your subnetwork Broadcast IP is: ", subnetIPbroadcast
print "Your new subnet mask is: ", newmask
