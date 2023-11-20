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
            IPlist, IPtest = [],[]
    return IPlist


IPlist = []
again = True
num = ""

IP = raw_input("Give IP: ")

IP = Check(IP)
IPlist = Separate(IP)

print IPlist

cidr = input("Please enter the CIDR 1-30 (for subnetting): ")

netmasks = ""

for i in range(1,cidr+1):
    netmasks += "1"
    if i % 8 == 0:
        netmasks += "."
for i in range(cidr+1, 33):
    netmasks += "0"
    if i % 8 == 0 and i!= 32:
        netmasks += "."

dec = []

for i in range(4):
    tempstr = ""
    num = IPlist[i]
    for j in range(7,-1,-1):
        if num / 2 ** j > 0:
            tempstr += "1"
            num -= 2**j
        else:
            tempstr += "0"
    dec.append(tempstr)

deccomplete = ""

for i in range(len(dec)):
    deccomplete += dec[i]
    if i != 3:
        deccomplete += "."
print dec
print "IP Address in decimal: ", deccomplete
print "Your net mask is: ", netmasks


'''
tempmask = []
netmaskd = ""

for i in range(len(netmasks)):
    tempmask.append(netmasks[i])
print tempmask
print len(tempmask)

for i in range(len(tempmask)):
    if tempmask[i] == ".":
        tempmask.pop(i)

for i in tempmask:
    netmaskd += i

print netmasks
print netmaskd
'''
