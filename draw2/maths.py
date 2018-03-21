from copy import deepcopy
from math import sin, cos, sqrt, acos

class Matrix:
    def __init__(self, vect1 = [1, 0, 0], vect2 = [0, 1, 0], vect3 = [0, 0, 1]):
        self.data = [vect1, vect2, vect3]
    def __len__(self):
        return len(self.data)
    def __repr__(self):
        return '\n'.join(map(str, self.data))
    def __str__(self):
        return '\n'.join(map(str, self.data))    
    def __setitem__(self, index, value):
        self.data[index] = value
    def __getitem__(self, index):
        return self.data[index]    
    def __add__(self, other):
        new = Matrix()
        for i in range(len(selfs)):
            for j in range(len(self[i])):
                new[i][j] = self[i][j] + other[i][j]
        return new
    def __sub__(self, other):
            new = Matrix()
            for i in range(3):
                for j in range(3):
                    new[i][j] = self[i][j] - other[i][j]
            return new    
    def __mul__(self, other):
        if type(other) == type(Vector()):
            new = Vector()
            for i in range(3):
                for j in range(3):
                    new[i] += self[i][j] * other[j]
        elif type(self) == type(other):
            new = Matrix()
            for line in range(len(self)):
                vect1 = Vector(self[line][0], self[line][1], self[line][2])
                for row in range(len(other[line])):
                    vect2 = Vector(other[0][row], other[1][row], other[2][row])
                    new[line][row] = vect1 * vect2
        return new
    

class Vector:
    def __init__(self, a = 0, b = 0, c = 0):
        self.data = [a, b, c]
    def __add__(self, other):
        new = Vector()
        for i in range(3):
            new.data[i] = self.data[i] + other.data[i]
        return new
    def __sub__(self, other):
        new = Vector()
        for i in range(3):
            new.data[i] = self.data[i] - other.data[i]
        return new        
    def __mul__(self, other):
        if type(self) == type(other):
            return self.data[0] * other.data[0] + self.data[1] * other.data[1] + self.data[2] * other.data[2]
        elif type(other) == type(0.0) or type(other) == type(0):
            a, b, c = [x * other for x in self]
            return Vector(a, b, c)
    def __setitem__(self, index, value):
        self.data[index] = value
    def __getitem__(self, index):
        return self.data[index]
    def __repr__(self):
        return str(self.data)
    def length(self):
        return sqrt(self.data[0] ** 2 + self.data[1] ** 2 + self.data[2] ** 2)
    
def rotateEvaluation(axis, angle, matrix):
    newMatrix = deepcopy(matrix)
    if axis == 'x':
        newMatrix = Matrix([1, 0, 0], [0, cos(angle), sin(angle)], [0, -sin(angle), cos(angle)]) * newMatrix
    elif axis == 'y':
        newMatrix = Matrix([cos(angle), 0, -sin(angle)], [0, 1, 0], [sin(angle), 0, cos(angle)]) * newMatrix
    elif axis == 'z':
        newMatrix = Matrix([cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]) * newMatrix
    return newMatrix

def getAngle(vect1, vect2):
    #vect1.length * vect2.length * cos(angle) = vect1 * vect2
    #print(vect1, vect2)
    #print(vect1.length() * vect2.length())
    if vect1.length() * vect2.length() != 0:
        return acos(round(vect1 * vect2, 5) / round(vect1.length() * vect2.length(), 7))
