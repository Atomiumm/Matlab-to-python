from copy import deepcopy

class Matrix:
	def __init__(self, *args):
		self.matrix = []
		if len(args) >= 2:
			if isinstance(args[0], int) and isinstance(args[1], int) and args[0] > 0 and args[1] > 0:
				self.rows = args[0]
				self.columns = args[1]
				for row in range(self.rows):
					self.matrix.append([0] * self.columns)
			else:
				raise Typerror
		if isinstance(args[0], list):
			for i in args[0]:
				if not isinstance(i, list):
					raise Typerror
				else:
					for j in i:
						if not isinstance(j, (int, float)):
							raise Typerror
			self.rows = len(args[0])
			self.columns = len(args[0][0])
			for row in range(self.rows):
					self.matrix.append([0] * self.columns)
			for row in range(self.rows):
				self.set_row(row+1, args[0][row])

	def __str__(self):
		result = "\n["
		for row in range(self.rows):
			result = result + "\n\t["
			for column in range(self.columns):
				result = result + str(self.matrix[row][column])
				if column != self.columns-1:
					result = result + "\t"
			result = result + "]"
		result = result + "\n]\n"
		return result

	def __neg__(self):
		result = Matrix(self.rows, self.columns)
		for row in range(self.rows):
			for column in range(self.columns):
				result.matrix[row][column] = -self.matrix[row][column]
		return result

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
			for row in range(self.rows):
				for column in range(self.columns):
					result.matrix[row][column] = self.matrix[row][column] + other
		else:
			raise Typerror
		return result

	def __sub__(self, other):

		return self + (-other)

	def __mul__(self, other):
		if isinstance(other, Matrix):
			if self.columns != other.rows:
				raise MatrixSizeException
			result = Matrix(self.rows, other.columns)
			for row in range(result.rows):
				for column in range(result.columns):
					for elem in range(self.columns):
						result.matrix[row][column] += (self.matrix[row][elem] * other.matrix[elem][column])
		elif isinstance(other, (int, float)):
			result = Matrix(self.rows, self.columns)
			for row in range(self.rows):
				for column in range(self.columns):
					result.matrix[row][column] = self.matrix[row][column] * other
		else:
			raise Typerror
		return result

	def __iter__(self):
		res = []
		for row in self.matrix:
			res += row
		return res.__iter__()

	def determinant(self):
		if self.rows != self.columns:
			raise MatrixSizeException
		elif self.rows == 1:
			return self.matrix[0][0]
		elif self.rows == 2:
			return self.matrix[0][0]*self.matrix[1][1] - self.matrix[0][1]*self.matrix[1][0]
		else:
			result = 0
			for column in range(self.columns):
				N = Matrix(self.rows-1, self.columns-1)
				for newrow in range(N.rows):
					row = []
					for newcolumn in range(self.columns):
						if newcolumn != column:
							row.append(self.matrix[newrow+1][newcolumn])
					N.matrix[newrow] = row
				result += ((-1)**column) * self.matrix[0][column] * N.determinant()
			return result

	def inverse(self):
		if self.rows != self.columns:
			raise MatrixSizeException
		if self.determinant() == 0:
			raise NonInvertibilityException
		copyM = deepcopy(self)
		result = Identity(self.rows)
		for row in range(copyM.rows):
			if copyM.matrix[row][row] == 0:
				for i in range(copyM.rows-row-1):
					if copyM.matrix[row+i+1][row] != 0:
						for j in range(copyM.columns):
							copyM.matrix[row][j] += copyM.matrix[row+i+1][j]
							result.matrix[row][j] += result.matrix[row+i+1][j]
						break
			a = copyM.matrix[row][row]
			for column in range(copyM.columns):
				copyM.matrix[row][column] = copyM.matrix[row][column] / a
				result.matrix[row][column] = result.matrix[row][column] / a
			for j in range(row+1, copyM.rows):
				a = copyM.matrix[j][row]
				for column in range(copyM.columns):
					copyM.matrix[j][column] -= a * copyM.matrix[row][column]
					result.matrix[j][column] -= a * result.matrix[row][column]
		for row in range(copyM.rows):
			for j in range(copyM.rows-1-row):
				a = copyM.matrix[copyM.rows-2-row-j][copyM.columns-1-row]
				for k in range(copyM.columns):
					copyM.matrix[copyM.rows-2-row-j][k] = copyM.matrix[copyM.rows-2-row-j][k] - a * copyM.matrix[copyM.columns-1-row][k]
					result.matrix[copyM.rows-2-row-j][k] = result.matrix[copyM.rows-2-row-j][k] - a * result.matrix[copyM.columns-1-row][k]
		return result

	def transpose(self):
		Transposed = Matrix(self.columns, self.rows)
		for row in range(self.rows):
			for column in range(self.columns):
				Transposed.matrix[column][row] = self.matrix[row][column]
		return Transposed

	def T(self):

		return self.transpose()

	def set_row(self, index, row):
		if len(row) < self.columns:
			for i in range(self.columns-len(row)):
				row.append(0)
		self.matrix[index-1] = row[:self.columns]

	def set_column(self, index, column):
		if len(column) < self.rows:
			for i in range(self.rows-len(column)):
				column.append(0)
		for i in range(self.rows):
			self.matrix[i][index-1] = column[i]

	def get_row(self, index):
		row = Matrix(1, self.columns)
		row.matrix[0] = self.matrix[index-1][:]
		return row

	def get_column(self, index):
		column = Matrix(self.rows, 1)
		for row in range(len(self.matrix)):
			column.matrix[row][0] = self.matrix[row][index-1]
		return column


class MatrixSizeException(Exception):
	pass

class NonInvertibilityException(Exception):
	pass

def Identity(size):
	M = Matrix(size, size)
	for i in range(size):
		M.matrix[i][i] = 1
	return M
		
