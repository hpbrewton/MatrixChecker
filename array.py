import inspect
import numpy as np

def input_to_logger_input(inp):
	if type(inp) == int:
		return str(inp)
	elif isinstance(inp, LoggerArray):
		return f"${inp.number}"
	else:
		return None

def ufunc_to_logger_op(ufunc):
	name = ufunc.__name__
	if name == "multiply": return "multiply"
	if name == "add": return "add"
	else: return "unknown" 

class LoggerArray:

	next_variable = 1

	def __init__(self, *dimensions):
		self.number = LoggerArray.next_variable
		if len(dimensions) == 0:
			self._log("array_variable", self, [])
		else:
			mapped_dimensions = [input_to_logger_input(dim) for dim in dimensions]
			self._log("array_fixed", self, mapped_dimensions)
		LoggerArray.next_variable += 1

	def __repr__(self):
		return f"{self.__class__.__name__}(#={self.number})"

	def __array__(self, dtype=None):
		return self._i * np.eye(self._N, dtype=dtype)

	def _log(self, op, output, inputs):
		(lineno, colno) = self.get_line_number()
		vector = [str(lineno), str(colno), op, input_to_logger_input(output), *inputs]
		string = " ".join(vector)
		print(string)

	def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
		if method == '__call__':
			# check inputs are okay
			logger_inputs = [input_to_logger_input(i) for i in inputs]
			logger_inputs_not_ok = any(x is None for x in logger_inputs)
			if logger_inputs_not_ok:
				return NotImplemented
			output = LoggerArray()
			self._log(ufunc_to_logger_op(ufunc), output, logger_inputs)

			return output
		else:
			return NotImplemented

	def get_line_number(self):
		last_position = self.last_position()
		frame = inspect.currentframe()
		self_filename = frame.f_code.co_filename
		while (frame.f_code.co_filename == self_filename) and (frame.f_lineno <= last_position):
			frame = frame.f_back
		return (frame.f_lineno, "?")

	def last_position(self):
		return inspect.currentframe().f_lineno


arr1 = LoggerArray(2, 2)
for i in range(10):
	arr1 = np.add(arr1, arr1)