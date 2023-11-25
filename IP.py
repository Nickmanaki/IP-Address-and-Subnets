# Subnetworks in Python :)
import string

letters = string.letters + string.punctuation.replace(".","")

numbers = string.digits


def makelist(lista):
    items = []
    for item in lista:
        if item != ".":
            items.append(item)
    return items

def Check(IP):
    gtfo = False
    while not gtfo:
        dotcount = 0
        correct = True
        prev = "test"
        for i in range(len(IP)):
            if IP[i] == ".":
                dotcount += 1
            if IP[i] in letters:
                correct = False
            if prev == "." and IP[i] == ".":
                correct = False
            prev = IP[i]

        if IP[0] == "." or IP[-1] == ".":
            correct = False
        if dotcount != 3:
            correct = False

        if not correct:
            IP = raw_input("Give IP again (Wrong form): ")
        else:
            gtfo = True
    return IP


def separate(IP):
    again = True
    check = False
    while again:
        IP += "."
        IPlist = []
        num = ""

        for i in range(len(IP)):
            if IP[i] in numbers:
                num += IP[i]
            else:
                IPlist.append(num)
                num = ""

        again = False

        for i in range(len(IPlist)):
            digit = int(IPlist[i])
            IPlist[i] = digit
            if digit > 256:
                check = True
            else:
                again = False

        if check:
            IP = raw_input("Give IP again (Number >256): ")
            IP = Check(IP)
            again = True
            check = False
            IPlist = []

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
    found = False

    if answer == "PC":
        zeros = 0
        while not found:
            if 2 ** zeros - 2 >= new:
                found = True
            else:
                zeros += 1
        newcidr = 32 - zeros
        new = 32 - cidr - zeros
    else:
        ones = 0
        while not found:
            if 2 ** ones >= new:
                found = True
            else:
                ones += 1
        newcidr = cidr + ones
        new = ones

    newsubnetmask = netmask(newcidr)

    return newsubnetmask, newcidr, new


def access(cidr, newcidr, newdigits, dec):
    subnetsum = 2 ** (newcidr - cidr)
    print "Your network has been divided to", subnetsum, "subnetworks"
    answer = input("Which subnetwork do you want to get information from? [1-"+str(subnetsum)+"]: ")
    num = answer - 1
    IPdigitlist = makelist(dec)
    subnetIPlist = []
    subnetIPbroadcastlist = []
    tempstr = ""
    subnetIP = ""
    subnetIPbroadcast = ""
    c = 0

    for j in range(newdigits - 1, -1, -1):
        if num / 2 ** j > 0:
            tempstr += "1"
            num -= 2 ** j
        else:
            tempstr += "0"

    for i in range(cidr):
        subnetIPlist.append(IPdigitlist[i])

    for i in range(cidr, cidr + len(tempstr)):
        subnetIPlist.append(tempstr[c])
        c += 1

    for n in subnetIPlist:
        subnetIPbroadcastlist.append(n)

    start = cidr + len(tempstr)

    for i in range(start, 32):
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


def translate(subIP, subbroadcastIP):
    subIPlistdec = []
    subbroadcastIPlistdec = []
    IPfinal = ""
    IPbroadcastfinal = ""
    subIPlist = makelist(subIP)
    subbroadcastIPlist = makelist(subbroadcastIP)

    for i in range(4):
        nums = 0
        numb = 0
        for j in range(0, 8):
            if subIPlist[i * 8 + j] == "1":
                nums += 2 ** (7 - j)

            if subbroadcastIPlist[i * 8 + j] == "1":
                numb += 2 ** (7 - j)

        subIPlistdec.append(str(nums))
        subbroadcastIPlistdec.append(str(numb))

    for i in range(1, 6, 2):
        subIPlistdec.insert(i, ".")
        subbroadcastIPlistdec.insert(i, ".")

    for i in range(len(subbroadcastIPlistdec)):
        IPfinal += subIPlistdec[i]
        IPbroadcastfinal += subbroadcastIPlistdec[i]

    return IPfinal, IPbroadcastfinal

def netmask(cidr):
    netmask = ""
    for i in range(1, cidr + 1):
        netmask += "1"
        if i % 8 == 0:
            netmask += "."
    for i in range(cidr + 1, 33):
        netmask += "0"
        if i % 8 == 0 and i != 32:
            netmask += "."
    return netmask

def bintodec(lista):
    dec = []
    deccomplete = ""
    for i in range(4):
        tempstr = ""
        num = lista[i]
        for j in range(7, -1, -1):
            if num / 2 ** j > 0:
                tempstr += "1"
                num -= 2 ** j
            else:
                tempstr += "0"
        dec.append(tempstr)

    for i in range(len(dec)):
        deccomplete += dec[i]
        if i != 3:
            deccomplete += "."
    return deccomplete


again = True


IP = raw_input("Give IP: ")
while again:
    subagain = True
    IP = Check(IP)
    IPlist = separate(IP)

    cidr = input("Please enter the CIDR 1-30 (for subnetting): ")

    netmaskstr = netmask(cidr)

    deccomplete = bintodec(IPlist)

    print "IP Address in decimal: ", deccomplete
    print "Your net mask is: ", netmaskstr

    answer, newnumber = choice()
    while subagain:
        newmask, newcidr, newdigits = subnet(answer, newnumber)
        subnetIP, subnetIPbroadcast = access(cidr, newcidr, newdigits, deccomplete)
        decsubnetIP, decsubnetIPbroadcast = translate(subnetIP, subnetIPbroadcast)

        print "Your subnetwork IP (in bin) is: ", subnetIP
        print "Your subnetwork Broadcast IP (in bin) is: ", subnetIPbroadcast
        print "Your subnetwork IP (in dec) is: ", decsubnetIP
        print "Your subnetwork Broadcast IP (in dec) is: ", decsubnetIPbroadcast
        print "Your new subnet mask is: ", newmask
        goagain = raw_input("Would you like to access a different subnetwork? [Y/N]: ")
        while goagain not in ["Y", "N"]:
            goagain = raw_input("Would you like to access a different subnetwork? [Y/N]: ")
        if goagain == "N":
            IP = raw_input("Please enter a new IP address (Type 0.0.0.0 to end program): ")
            subagain = False
            if IP == "0.0.0.0":
                again = False
                print "We're done here pal"




