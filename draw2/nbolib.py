class Node:
    def __init__(self, num=None, x=None, y=None, z=None, bonds=None):
        '''
        Node constructor.
        Possible args:
            'num' is node number.
            'x', 'y' and 'z' are coords.
            'bonds' is array, containing Bond objects.
        '''
        self.num = num
        self.x = x
        self.y = y
        self.z = z
        self.bonds = bonds
        if self.bonds == None:
            self.bonds = NBOSet()
    
    def __str__(self):
        return "{{\n\tnum = {}\n\tx = {}\n\ty = {}\n\tz = {}\n}}".format(self.num, self.x, self.y)
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.x == other.x and\
                self.y == other.y and\
                    self.bonds == other.bonds

class Bond:
    def __init__(self, num=None, node1=None, node2=None, shiftX=None, shiftY=None, shiftZ=None):
        '''
        Bond constructor.
        Possible args:
            'num' is bond number.
            'node1' and 'node2' are bond nodes.
            'shiftX', 'shiftY' and 'shiftZ' are shift in primitive cells.
        '''
        self.num = num
        if node1 < node2:
            self.node1 = node1
            self.node2 = node2
            self.shiftX = shiftX
            self.shiftY = shiftY
            self.shiftZ = shiftZ
        else:
            self.node2 = node1
            self.node1 = node2
            self.shiftX = -shiftX
            self.shiftY = -shiftY
            if shiftZ is not None: # Dirty hack
                self.shiftZ = -shiftZ
            else:
                self.shiftZ = shiftZ
        
    def __str__(self):
        return "{{\n\tnum = {}\n\tnode1 = {}\n\tnode2 = {}\n\tshiftX = {}\n\tshiftY = {}\n\tshiftZ = {}\n}}".format(self.num, self.node1, self.node2, self.shiftX, self.shiftY, self.shiftZ)
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return isinstance(other, Bond) and self.node1 == other.node1 and\
                self.node2 == other.node2 and\
                    self.shiftX == other.shiftX and\
                        self.shiftY == other.shiftY and\
                            self.shiftZ == other.shiftZ
    
class NBOSet:
    def __init__(self, key='num', array=[]):
        if len(array) > 0:
            self.data = [None for i in range(max(map(lambda x: getattr(x, key), array)))]
        else:
            self.data = []
        self.key = key
        for obj in array:
            self.append(obj)
    
    def append(self, obj):
        index = getattr(obj, self.key)
        if index > len(self.data):
           self.data += [None for i in range(index - len(self.data))]
        self.data[index - 1] = obj
        
    def update(self, objects):
        for obj in objects:
            self.append(obj)
    
    def __getitem__(self, index):
        return self.data[index - 1]
    
    def __add__(self, other):
        if isinstance(other, NBOSet):
            result = NBOSet()
            result.update(self.data)
            result.update(other.data)
        else:
            result = NBOSet()
            result.update(self.data)
            result.append(other)
            
    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return self.data.__repr__()
    
    def __iter__(self):
        return filter(lambda x: x is not None, self.data).__iter__()
    
    def __eq__(self, other):
        return self.data == self.data
    
    def __contains__(self, obj):
        return obj in self.data
    
def igorToNBO3D(primitiveCell):
    readyNodes = NBOSet()
    readyBonds = NBOSet()
    rawData = primitiveCell[6] # Because first 6 values in primitiveCell is angles, a, b and c — not nodes and bonds.
    for rawNode in rawData:
        # print(rawNode)
        node = Node(num=rawNode[0], x=rawNode[1], y=rawNode[2], z=rawNode[3])
        rawBonds = rawNode[4:]
        currBonds = []
        for rawBond in rawBonds:
            bond = Bond(num=len(readyBonds.data) + 1, node1=node.num, node2=rawBond[3], shiftX=rawBond[0], shiftY=rawBond[1], shiftZ=rawBond[2])
            readyBonds.append(bond)
        readyNodes.append(node)
    for readyBond in readyBonds:
        readyNodes[readyBond.node1].bonds.append(readyBond)
        readyNodes[readyBond.node2].bonds.append(readyBond)
    return readyNodes, readyBonds

def igorToNBO2D(primitiveCell):
    readyNodes = NBOSet()
    readyBonds = NBOSet()
    rawData = primitiveCell[3] # Because first 3 values in primitiveCell is angle, a and b — not nodes and bonds.
    for rawNode in rawData:
        # print(rawNode)
        node = Node(num=rawNode[0], x=rawNode[1], y=rawNode[2])
        rawBonds = rawNode[3:]
        currBonds = []
        for rawBond in rawBonds:
            bond = Bond(num=len(readyBonds.data) + 1, node1=node.num, node2=rawBond[2], shiftX=rawBond[0], shiftY=rawBond[1])
            readyBonds.append(bond)
        readyNodes.append(node)
    for readyBond in readyBonds:
        readyNodes[readyBond.node1].bonds.append(readyBond)
        readyNodes[readyBond.node2].bonds.append(readyBond)
    return readyNodes, readyBonds

def igorToNBO(primitiveCell):
    '''
    Converts IGOR format data to Node and Bond objects.
    Accepts one argument — IGOR's primitiveCell.
    Returns Nodes, Bonds.
    '''
    if type(primitiveCell[3]) == type([]) or type(primitiveCell[3]) == type(()):
        return igorToNBO2D(primitiveCell)
    else:
        return igorToNBO3D(primitiveCell)

def nboToIGOR3D(nodes, bonds, angle, a, b, c):
    '''
    Converts Node and Bond objects to IGOR format data.
    Accepts five arguments — nodes, bonds, angle (is (angleA, angleB, angleG), a and b.
    Returns one value — IGOR's primitiveCell.
    '''
    result = (angle[0], angle[1], angle[2], a, b, c, [])
    readyCell = result[6]
    for node in nodes:
        if node is None:
            continue
        readyNode = [node.num, node.x, node.y, node.z]
        for bond in node.bonds:
            if bond is None:
                continue
            if bond.node1 == node.num: # Only for outcoming bonds.
                readyBond = [bond.shiftX, bond.shiftY, bond.shiftZ, bond.node2]
                readyNode.append(readyBond)
        readyCell.append(readyNode)
    return result

def nboToIGOR2D(nodes, bonds, angle, a, b):
    '''
    Converts Node and Bond objects to IGOR format data.
    Accepts five arguments — nodes, bonds, angle, a and b.
    Returns one value — IGOR's primitiveCell.
    '''
    result = (angle, a, b, [])
    readyCell = result[3]
    for node in nodes:
        if node is None:
            continue
        readyNode = [node.num, node.x, node.y]
        for bond in node.bonds:
            if bond is None:
                continue
            if bond.node1 == node.num: # Only for outcoming bonds.
                readyBond = [bond.shiftX, bond.shiftY, bond.node2]
                readyNode.append(readyBond)
        readyCell.append(readyNode)
    return result

def nboToIGOR(*args):
    if len(args) == 6:
        return nboToIGOR3D(*args)
    else:
        return nboToIGOR2D(*args)
    
def syncNBO(nodes, bonds):
    readyNodes = NBOSet(array=nodes)
    readyBonds = NBOSet(array=bonds)
    for bond in bonds:
        if bond not in readyNodes[bond.node1].bonds:
            readyNodes[bond.node1].bonds.append(bond)
        if bond not in readyNodes[bond.node2].bonds:
            readyNodes[bond.node2].bonds.append(bond)
    for node in nodes:
        for bond in node.bonds:
            if bond not in readyBonds:
                readyBonds.append(bond)
    return readyNodes, readyBonds