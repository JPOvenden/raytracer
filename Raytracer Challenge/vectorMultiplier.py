class Tuple:
    def __init__(self, x, y, z, w):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = int(w)

    def __add__(self, other):
        return Tuple(self.x + other.x,
                     self.y + other.y,
                     self.z + other.z,
                     self.w or other.w)
    def __sub__(self, other):
        return Tuple(self.x - other.x,
                     self.y - other.y,
                     self.z - other.z,
                     self.w and not other.w)
    
    def __neg__(self):
        return Tuple(-self.x,
                     -self.y,
                     -self.x,
                     self.w)
    
    def __mul__(self, other):
        return self.__class__(self.x * other,
                     self.y * other,
                     self.z * other,
                     self.w * other)
    
    def __truediv__(self, other):
        return Tuple(self.x / other,
                     self.y / other,
                     self.z / other,
                     self.w / other)

    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2 + self.w**2) ** 0.5

    def normalize(self):
        d = self.magnitude()
        if d == 0:
            return self
        inverse = 1.0/d
        return self.__class__(self.x * inverse,
                              self.y * inverse,
                              self.z * inverse,
                              self.w * inverse)
    
    def dot(self, other):
        return (self.x * other.x +
                self.y * other.y +
                self.z * other.z +
                self.w * other.w)

    def cross(self, other):
        return self.__class__(self.y * other.z - self.z * other.y,
                              self.z * other.x - self.x * other.z,
                              self.x * other.y - self.y * other.x)

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}, w: {self.w}"

class Vector(Tuple):
    def __init__(self, x, y, z, w=0.0):
        super().__init__(x, y, z, w)

    def __str__(self):
        return f"V({self.x},{self.y},{self.z})"

class Color(Tuple):
    def __init__(self, r, g, b, w=0):
        super().__init__(r, g, b, w)

    @property
    def red(self):
        return self.x

    @property
    def green(self):
        return self.y

    @property
    def blue(self):
        return self.z

    def __mul__(self, other):
        if isinstance(other, Color):
            return Color(self.x * other.x, self.y * other.y, self.z * other.z)
        return super().__mul__(other)
        
class Point(Tuple):
    def __init__(self, x, y, z, w=1.0):
        super().__init__(x, y, z, w=1.0)

    def __str__(self):
        return f"P({self.x},{self.y},{self.z})"

class Matrix:
    def __init__(self, matrix):
        self.size = len(matrix)
        for x in matrix:
            if len(x) != self.size:
                raise TypeError
        self.matrix = matrix

    def identity(self):
        identityMatrix = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        return(self * identityMatrix)

    def transpose(self):
        transposedMat = [([0] * self.size) for _ in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                transposedMat[col][row] = self[row][col]
        return Matrix(transposedMat)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            mat = [([0] * self.size) for _ in range(self.size)]
            for row in range(self.size):
                for column in range(self.size):
                    ans = 0
                    for index in range(self.size):
                        ans += self.matrix[row][index] * other.matrix[index][column]
                    mat[row][column] = ans
            return Matrix(mat)

        elif isinstance(other, Tuple):
            if self.size != 4:
                raise ValueError("The matrix os not the same size as the tuple.")
            result = []
            for row in range(self.size):
                row_tuple = Tuple(*self.matrix[row])
                result.append(Tuple.dot(row_tuple, other))
            return Tuple(*result)
        
        else:
            raise TypeError("The expected operand argument is of an unsupported type")
        
    def determinant(self):
        if self.size == 2:
            return (self[0][0] * self[1][1] - self[0][1] * self[1][0])
        total = 0
        for col in range(self.size):
            total += self[0][col] * self.cofactor(0, col)
        return total
        
    def submatrix(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            raise IndexError("Row or column index out of range")
        subMatrix = [
                [self.matrix[r][c] for c in range(self.size) if c != col]
                for r in range(self.size) if r != row
            ]
        return Matrix(subMatrix)

    def minor(self, row, col):
        return self.submatrix(row, col).determinant()

    def cofactor(self, row, col):
        if (row + col) % 2 != 0:
            return -(self.minor(row, col))
        else:
            return self.minor(row, col)
        #or use this: return -(self.minor(row, col)) if (row + col) % 2 != 0 else self.minor(row, col)
        
    def isinvertible(self):
        return self.determinant() != 0

    def invert(self):
        d = self.determinant()
        m = Matrix([([0] * self.size) for _ in range(self.size)])
        sz = range(self.size)
        for row in sz:
            for col in sz:
                m[row][col] = self.cofactor(row, col) / d
        m = m.transpose()
        return m

#######Maybe move this section to separate classes
    def translation(x, y, z):
        return Matrix([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]])
    
    def transform(point, translation):
        t = translation * point
        return Point(t.x, t.y, t.z)

    def scaling(x, y, z):
        return Matrix([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]])

##################################################
    
    def __getitem__(self, index):
        return self.matrix[index]

    def __setitem__(self, key, value):
        self.matrix[key] = value
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

    def __eq__(self, other):#I used this method instead of element by element because at these sizes it is 20-30% faster
        if self.size != other.size:
            return False
        if ''.join(map(str, sum(self.data, []))) != ''.join(map(str, sum(other.data, []))):
            return False
        return True


class Rotate:
    #Static value of Euler's number, trying to avoid imports, 
    #in theory this could be calculated but would require some overhead.
    e = 2.718281828459045
    
    @staticmethod
    def my_cos(x):
        return (Rotate.e**(x * 1j)).real

    @staticmethod
    def my_sin(x):
        return (Rotate.e**(x * 1j)).imag

    @staticmethod
    def x(r):
        return Matrix([
            [1, 0, 0, 0],
            [0, Rotate.my_cos(r), -Rotate.my_sin(r), 0],
            [0, Rotate.my_sin(r), Rotate.my_cos(r), 0],
            [0, 0, 0, 1]
        ])
    
    @staticmethod
    def y(r):
        return Matrix([
            [Rotate.my_cos(r), 0, Rotate.my_sin(r), 0],
            [0, 1, 0, 0],
            [-Rotate.my_sin(r), 0, Rotate.my_cos(r), 0],
            [0, 0, 0, 1]
        ])
    
    @staticmethod
    def z(r):
        return Matrix([
            [Rotate.my_cos(r), -Rotate.my_sin(r), 0, 0],
            [Rotate.my_sin(r), Rotate.my_cos(r), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
