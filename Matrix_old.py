class Matrix:
	def __init__(self, rows, columns):
		self.matrix = []
		self.rows = rows
		self.columns = columns

		for row in range(rows):
			row = []
			for column in range(columns):
				row.append(0)
			self.matrix.append(row)

	def __abs__(self, other):

		return Determinant(self)

	def __add__(self, other):
		if isinstance(other, Matrix):
			if (self.rows != other.rows) or (self.columns != other.columns):
				raise MatrixSizeException
			result = Matrix(self.rows, self.columns)
			for row in range(self.rows):
				for column in range(self.columns):
					result.matrix[row][column] = self.matrix[row][column] + other.matrix[row][column]
		elif isinstance(other, (int, float)):
			result = Matrix(self.rows, self.columns)
			for i in range(self.rows):
				for j in range(self.columns):
					result.matrix[i][j] = self.matrix[i][j] + other
		else:
			raise Typerror
		return result

	def __sub__(self, other):

		return self + (-other)

	def __neg__(self):
		result = Matrix(self.rows, self.columns)
		for row in range(self.rows):
			for column in range(self.columns):
				result.matrix[row][column] = -self.matrix[row][column]
		return result

	def __mul__(self, other):
		if isinstance(other, Matrix):
			if self.columns != other.rows:
				raise MatrixSizeException
			result = Matrix(self.rows, other.columns)
			for i in range(result.rows):
				for j in range(result.columns):
					for k in range(self.columns):
						result.matrix[i][j] = result.matrix[i][j] + (self.matrix[i][k] * other.matrix[k][j])
		elif isinstance(other, (int, float)):
			result = Matrix(self.rows, self.columns)
			for i in range(self.rows):
				for j in range(self.columns):
					result.matrix[i][j] = self.matrix[i][j] * other
		else:
			raise Typerror
		return result

	def __div__(self, other):
		if isinstance(other, Matrix):
			return self * other.Inverse()
		elif isinstance(other, (int, float)):
			result = Matrix(self.rows, self.columns)
			for i in range(self.rows):
				for j in range(self.columns):
					result.matrix[i][j] = self.matrix[i][j] / other
			return result
		else:
			raise Typerror

	def __truediv__(self, other):
		if isinstance(other, Matrix):
			return self * other.Inverse()
		elif isinstance(other, (int, float)):
			result = Matrix(self.rows, self.columns)
			for i in range(self.rows):
				for j in range(self.columns):
					result.matrix[i][j] = self.matrix[i][j] / other
			return result
		else:
			raise Typerror

	def __floordiv__(self, other):
		
		return floor(self / other)

	def __pow__(self, other):
		if self.rows != self.columns:
			raise MatrixSizeException
		else:
			if other < 0:
				raise ValueError
			result = Identity(self.rows)
			for i in range(other):
				result = result * self
			return result

	def __ceil__(self, other):
		result = Matrix(self.rows, self.columns)
		for i in self.rows:
			for j in self.columns:
				result.matrix[i][j] = ceil(self.matrix[i][j])
		return result

	def __floor__(self, other):
		result = Matrix(self.rows, self.columns)
		for i in self.rows:
			for j in self.columns:
				result.matrix[i][j] = floor(self.matrix[i][j])
		return result

	def __bool__(self):
		if self.Determinant():
			return True
		else:
			return False

	def __int__(self):
		result = Matrix(self.rows, self.columns)
		for i in self.rows:
			for j in self.columns:
				result.matrix[i][j] = int(self.matrix[i][j])
		return self.rows * self.columns

	def __float__(self):
		result = Matrix(self.rows, self.columns)
		for i in self.rows:
			for j in self.columns:
				result.matrix[i][j] = float(self.matrix[i][j])
		return self.rows * self.columns

	def __str__(self):
		result = "\n["
		for i in range(self.rows):
			result = result + "\n\t["
			for j in range(self.columns):
				result = result + str(self.matrix[i][j])
				if j != self.columns-1:
					result = result + "\t"
			result = result + "]"
		result = result + "\n]\n"
		return result

	def __contains__(self, item):
		for i in self.rows:
			for j in self.columns:
				if self.matrix[i][j] == item:
					return True
		return False

	def Expand(self, row, column):
		if row > self.rows - 1:
			for r in range(row - (self.rows - 1)):
				r = []
				for c in range(self.columns):
					r.append(0)
				self.matrix.append(r)
			self.rows = row + 1
		if column > self.columns - 1:
			for r in range(self.rows):
				for c in range(column - (self.columns - 1)):
					self.matrix[r].append(0)
			self.columns = column + 1

	def Row(self, row, List):
		column = len(List) - 1
		self.Expand(row, column)
		r = []
		if column < self.columns - 1:
			for c in range(column - (self.columns - 1)):
				List.append(0)
		self.matrix[row] = List

	def Column(self, column, List):
		row = len(List) - 1
		self.Expand(row, column)
		if row < self.rows - 1:
			for r in range(row - (self.rows - 1)):
				List.append(0)
		for r in range(self.rows):
			self.matrix[r][column] = List[r]

	def Value(self, row, column, value):
		self.Expand(row, column)
		self.matrix[row][column] = value


class MatrixSizeException(Exception):
	pass

		

def Identity(size):
	M = Matrix(size, size)
	for i in range(size):
		M.matrix[i][i] = 1
	return M

def Ones(rows, columns):
	M = Matrix(rows, columns)
	M = M + 1
	return M

def RandomM(rows, columns):
	M = Matrix(rows, columns)
	import random
	for i in range(rows):
		for j in range(columns):
			M.matrix[i][j] = random.randint(0, 10)
	del random
	return M

def RandomMF(rows, columns):
	M = Matrix(rows, columns)
	import random
	for i in range(rows):
		for j in range(columns):
			M.matrix[i][j] = random.random()
	del random
	return M

def Transpose(M):
	Transposed = Matrix(M.columns, M.rows)
	for row in range(M.rows):
		for column in range(M.columns):
			Transposed.matrix[column][row] = M.matrix[row][column]
	return Transposed

def Determinant(M):
		if M.rows != M.columns:
			raise MatrixSizeException
		if M.rows == 1:
			result = M.matrix[0][0]
		elif M.rows == 2:
			result = M.matrix[0][0]*M.matrix[1][1] - M.matrix[0][1]*M.matrix[1][0]
		else:
			result = 0
			for column in range(M.columns):
				N = Matrix(M.rows-1, M.columns-1)
				for newrow in range(M.rows-1):
					row = []
					for newcolumn in range(M.rows):
						if newcolumn != column:
							row.append(M.matrix[newrow+1][newcolumn])
					N.matrix[newrow] = row
				result = result + N.Determinant()
		return result

def Inverse(M):
	if M:
		import copy
		copyM = copy.deepcopy(M)
		del copy
		result = Identity(M.rows)
		for i in range(M.rows):
			a = copyM.matrix[i][i]
			for j in range(M.columns):
				copyM.matrix[i][j] = copyM.matrix[i][j] / a
				result.matrix[i][j] = result.matrix[i][j] / a
			for j in range(i+1, M.rows):
				a = copyM.matrix[j][i]
				for k in range(M.columns):
					copyM.matrix[j][k] = copyM.matrix[j][k] - a * copyM.matrix[i][k]
					result.matrix[j][k] = result.matrix[j][k] - a * result.matrix[i][k]
		for i in range(M.rows):
			for j in range(M.rows-1-i):
				a = copyM.matrix[M.rows-2-i-j][M.columns-1-i]
				for k in range(M.columns):
					copyM.matrix[M.rows-2-i-j][k] = copyM.matrix[M.rows-2-i-j][k] - a * copyM.matrix[M.columns-1-i][k]
					result.matrix[M.rows-2-i-j][k] = result.matrix[M.rows-2-i-j][k] - a * result.matrix[M.columns-1-i][k]
		return result	
	else:
		raise ValueError

def ElemMult(M1, M2):
	if (M1.rows != M2.rows) or (M1.columns != M2.columns):
		raise MatrixSizeException
	result = Matrix(M1.rows, M1.columns)
	for row in range(M1.rows):
		for column in range(M1.columns):
			result.matrix[row][column] = M1.matrix[row][column] * M2.matrix[row][column]
	return result

def ElemDiv(M1, other):
	if (M1.rows != M2.rows) or (M1.columns != M2.columns):
		raise MatrixSizeException
	result = Matrix(M1.rows, M1.columns)
	for row in range(M1.rows):
		for column in range(M1.columns):
			result.matrix[row][column] = M1.matrix[row][column] / M2.matrix[row][column]
	return result

def ElemPow(M, Pow):
	result = Matrix(M.rows, M.columns)
	for row in range(M.rows):
		for column in range(M.columns):
			result.matrix[row][column] = M.matrix[row][column] ** Pow
	return result

def ElemInv(M):
	result = Matrix(M.rows, M.columns)
	for row in range(M.rows):
		for column in range(M.columns):
			result.matrix[row][column] = 1 / M.matrix[row][column]
	return result

def ElemExp(M):
	result = Matrix(M.rows, M.columns)
	import math
	for row in range(M.rows):
		for column in range(M.columns):
			result.matrix[row][column] = math.exp(M.matrix[row][column])
	del math
	return result

def ElemLog(M):
	result = Matrix(M.rows, M.columns)
	import math
	for row in range(M.rows):
		for column in range(M.columns):
			result.matrix[row][column] = math.log(M.matrix[row][column])
	del math
	return result


ToAdd = dir(int)
for f in dir(float):
	if f not in ToAdd:
		ToAdd.append(f)
for f in dir(complex):
	if f not in ToAdd:
		ToAdd.append(f)
for f in dir(str):
	if f not in ToAdd:
		ToAdd.append(f)
for f in dir(list):
	if f not in ToAdd:
		ToAdd.append(f)
for f in dir(tuple):
	if f not in ToAdd:
		ToAdd.append(f)
for f in dir(dict):
	if f not in ToAdd:
		ToAdd.append(f)
#for f in dir(Matrix):
#	if f in ToAdd:
#		ToAdd.remove(f)
ToAdd.sort()
print(ToAdd)





