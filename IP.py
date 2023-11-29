# Subnetworks in Python :)
import string

letters = string.letters + string.punctuation.replace(".", "")

numbers = string.digits


def menu():
    print "1. Look up the IP of x device in the subnetwork"
    print "2. Choose a different subnetwork"
    print "3. Enter a new IP"
    option = input("What would you like to do [1-3]: ")
    while option not in range(1, 4):
        option = input("Please enter a number between the range[1-3]: ")
    print
    return option


def searchpc(subIP, broadcastIP):
    i = len(subIP)-1
    j = len(broadcastIP)-1
    numIP = ""
    numbroadcast = ""

    while subIP[i] != ".":
        numIP += subIP[i]
        i -= 1
    while broadcastIP[j] != ".":
        numbroadcast += broadcastIP[j]
        j -= 1

    numIP, numbroadcast = int(numIP[::-1]), int(numbroadcast[::-1])
    PCamount = numbroadcast - numIP

    pcnum = input("There are "+str(PCamount)+" devices in this network, which one would like to see the IP of?: ")
    while pcnum <= 0 or pcnum >= numbroadcast-numIP:
        pcnum = input("There are "+str(PCamount)+" devices in this subnetwork, please choose a number between 0 and " + str(PCamount)+": ")

    newend = str(numIP + pcnum)
    deviceip = ""

    dotcount = 0
    k = 0
    while dotcount < 3:
        if subIP[k] == ".":
            dotcount += 1
        deviceip += subIP[k]
        k += 1

    deviceip += newend

    return deviceip, pcnum


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


def choice(number):
    subs = 2 ** (number-2)
    pcs = 2 ** (number-1) - 2

    print "You can make up to", str(subs), "subnetworks"

    answer = raw_input("Do you want to split your network into more subnetworks depending on the amount of PCs or amount of Subnetworks? [PC/Sub]: ")
    while answer != "PC" and answer != "Sub":
        answer = raw_input("Please enter either 'PC' or 'Sub': ")

    if answer == "PC":
        new = input("How many devices do you want your new subnetworks to at least have?(Max devices "+str(pcs)+"): ")
        while new > pcs or new <= 0:
            new = input("In order to make subnetworks, each one must have at maximum "+str(pcs)+" devices: ")
    else:
        new = input("How many subnetworks do you want to at least have?: ")
        while new > subs or new <= 0:
            new = input("You can't make this many subnetworks, please keep it under or equal to "+str(subs)+": ")

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

    newsubnetmask, null = netmask(newcidr)

    return newsubnetmask, newcidr, new


def access(cidr, newcidr, newdigits, dec):
    subnetsum = 2 ** (newcidr - cidr)
    print "Your network has been divided to", subnetsum, "subnetworks"+"\n"
    answer = input("Which subnetwork do you want to get information from? [1-"+str(subnetsum)+"]: ")
    while answer > subnetsum or answer <= 0:
        answer = input("Please choose a number in the range listed above: ")
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
    zerocounter = 0
    for i in range(1, cidr + 1):
        netmask += "1"
        if i % 8 == 0 and i != 32:
            netmask += "."
    for i in range(cidr + 1, 33):
        netmask += "0"
        zerocounter += 1
        if i % 8 == 0 and i != 32:
            netmask += "."
    return netmask, zerocounter


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
if IP == "0.0.0.0":
    again = False
while again:
    subagain = True
    IP = Check(IP)
    IPlist = separate(IP)
    sure = "N"
    goagain = "N"
    cidring = True

    while cidring:
        cidr = input("Please enter the CIDR 1-32: ")
        while cidr not in range(1, 33):
            cidr = input("Please enter the CIDR 1-32: ")

        if cidr > 29:
            sure = raw_input("Are you sure you want to proceed? Your cidr is higher than 30, so you will not be able to make subnets [Y/N]: ")
            while sure not in ["Y", "N"]:
                sure = raw_input("Please enter either 'Y' or 'N': ")
        else:
            cidring = False
        if sure == "Y":
            cidring = False

    netmaskstr, amount = netmask(cidr)
    deccomplete = bintodec(IPlist)

    print "IP Address in decimal: ", deccomplete
    print "Your net mask is: ", netmaskstr + "\n"

    if sure != "Y":
        answer, newnumber = choice(amount)
        while subagain:
            menuing = True
            newmask, newcidr, newdigits = subnet(answer, newnumber)
            subnetIP, subnetIPbroadcast = access(cidr, newcidr, newdigits, deccomplete)
            decsubnetIP, decsubnetIPbroadcast = translate(subnetIP, subnetIPbroadcast)

            print "Your subnetwork IP (in bin) is: ", subnetIP
            print "Your subnetwork Broadcast IP (in bin) is: ", subnetIPbroadcast
            print "Your subnetwork IP (in dec) is: ", decsubnetIP
            print "Your subnetwork Broadcast IP (in dec) is: ", decsubnetIPbroadcast
            print "Your new subnet mask is: ", newmask
            print
            while menuing:
                next = menu()
                if next == 1:
                    pcIP, pcnumber = searchpc(decsubnetIP, decsubnetIPbroadcast)
                    print "Device #"+str(pcnumber), "has the following IP: "+pcIP+"\n"
                elif next == 2:
                    subagain = True
                    menuing = False
                else:
                    subagain = False
                    menuing = False
    if IP != "0.0.0.0":
        IP = raw_input("Please enter a new IP address (Type 0.0.0.0 to end program): ")
    if IP == "0.0.0.0":
        again = False
        print "We're done here pal"
