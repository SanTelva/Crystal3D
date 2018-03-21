import sys
#IGOR to IGOR 3D converter
#this script creates stereo-analog of IGOR PC description
if len(sys.argv) < 2:
    print('Usage:')
    print(sys.argv[0], 'filename.txt')
    raise ValueError
filename = sys.argv[1] # name of input file with ".txt"
fin = open(filename, "r")
fout = open(filename[:-4] + "3D" + ".txt", "w")
angle, a, b = fin.readline().split()
print(angle, 90, 90, a, b, (int(a) + int(b)) // 2, file = fout)
nodes = [node.split("\t") for node in fin.readlines()] # Get list of lists of strings
print(nodes)
for i in nodes:
    #print('\t'.join(map(str, i)))
    num, a, b = i[:3]
    bonds = i[3:]
    c = (float(a) + float(b)) / 2
    print(c)
    newbonds = []
    for bond in bonds:
        bond = bond.split()
        #print(bond[:2] + ['0'] + [bond[2]])
        newbonds.append(' '.join(bond[:2] + ['0'] + [bond[2]]))
    newbonds.append(' '.join(['0', '0', '1', num]))
    print(num, a, b, (float(a) + float(b)) / 2, sep = '\t', end = '\t', file = fout)
    for newbond in newbonds: print(newbond, sep = '\t', end = '\t', file = fout)
    print(file = fout)
fin.close()
fout.close()