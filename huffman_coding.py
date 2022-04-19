
from base64 import decode


class Tree:
	def __init__(self, left=None, right=None, value=None):
		self.value = value
		self.left = left
		self.right = right

	def __repr__(self) -> str:
		return str(self.to_dict())

	def to_dict(self):
		if type(self.left) is Tree:
			left = self.left.to_dict()
		else:
			left = str(self.left)
		
		if type(self.right) is Tree:
			right = self.right.to_dict()
		else:
			right = str(self.right)
		
		if self.value is None:
			return [left, right]
		else:
			return {self.value: [left, right]}

	def add_keys(self, keys):
		if len(keys) == 2:
			self.left, self.right = keys
		elif len(keys) % 2 == 1:
			self.left = keys.pop()
			self.right = Tree().add_keys(keys)
		else:
			mid = len(keys) // 2
			self.left = Tree().add_keys(keys[:mid])
			self.right = Tree().add_keys(keys[mid:])
		return self
	
	def depth(self):
		return (0 if 
			type(self.left) is not Tree and 
			type(self.right) is not Tree 
			else max(self.left.depth(), self.right.depth())) + 1
	
	def values(self):
		if type(self.left) is Tree:
			for pre, key in self.left.values():
				yield '0' + pre, key
		else:
			yield '0', self.left
		
		if type(self.right) is Tree:
			for pre, key in self.right.values():
				yield '1' + pre, key
		else:
			yield '1', self.right
	
	def get_pre(self, l):
		if self.left == l:
			return '0'
		elif self.right == l:
			return '1'
		else:
			if type(self.left) is Tree:
				left = self.left.get_pre(l)
				if left is not None:
					return '0' + left
			if type(self.right) is Tree:
				right = self.right.get_pre(l)
				if right is not None:
					return '1' + right
			return None

	def get_bit(self, bit):
		if int(bit) == 0:
			return self.left
		else:
			return self.right

	@classmethod
	def from_dict(self, data):
		last = None
		for p, keys in sorted(data.items(), key=lambda e:e[0]):
			if last is not None:
				keys += [last]
			last = Tree().add_keys(keys)
		return last

def huffman_encode(string):
	letters = {}
	for l in string:
		if l not in letters:
			letters[l] = 1
		else:
			letters[l] += 1
	
	probs = {}

	for l, c in letters.items():
		prob = c/len(string)
		if prob not in probs:
			probs[prob] = []
		probs[prob].append(l)
	
	tree = Tree.from_dict(probs)

	encoded = ''.join(tree.get_pre(l) for l in string)

	return tree, encoded

def huffman_decode(tree, code):
	orig = tree
	string = ''
	for i in code:
		tree = tree.get_bit(i)
		if type(tree) is str:
			string += tree
			tree = orig
	return string

tree, encoded = huffman_encode('salut comment ca va?')
print(encoded)

decoded = huffman_decode(tree, encoded)
print(decoded)
