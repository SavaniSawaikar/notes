# this is just a random tree, with a left and right child node
class TreeNode:
	def __init__(self, val):
		self.val = val
		self.left = None
		self.right = None


# Binary Search Tree

class BST:

	def __init__(self, root):
		self.root = root

	def get_minimum_node(self, start_node):
		"""	Function takes O(h) time where h is the height of the tree """
		node = start_node
		while node.left:
				node = node.left
		return node
				
	def get_maximum_node(self, start_node):
		"""	Function takes O(h) time where h is the height of the tree """
		node = start_node
		while node.right:
				node = node.right
		return node

	def insert_node(self, val):
			new_node = TreeNode(val)
			if self.root is None:
				self.root = new_node
				return
			node = self.root
			parent_link = None
			parent = self.root
			while node:
				if val <= node.val:
					parent_link = 'left'
					parent = node
					node = node.left 
				else:
					parent_link = 'right'
					parent = node
					node = node.right
			if parent_link == 'right':
				parent.right = new_node
			elif parent_link == 'left':
				parent.left = new_node


	def delete_node(self, del_value):
		curr_node = self.root
		parent = self.root
		link = None
		while curr_node:
			if del_value < curr_node.val:
				parent = curr_node
				link = 'left'
				curr_node = curr_node.left
			elif del_value > curr_node.val:
				parent = curr_node
				link = 'right'
				curr_node = curr_node.right
			else:
				# first case for deleting a node with no children nodes
				if not curr_node.left and not curr_node.right:
					if link == 'left':
						parent.left = None
					elif link == 'right':
						parent.right = None
				# second case for deleting a node with one child
				elif curr_node.left and not curr_node.right:
					if link == 'left':
						parent.left = curr_node.left
					elif link == 'right':
						parent.right = curr_node.left
				elif curr_node.right and not curr_node.left:
					if link == 'left':
						parent.left = curr_node.right
					elif link == 'right':
						parent.right = curr_node.right
				# third case for deleting a node with two children nodes
				elif curr_node.right and curr_node.left:
					replacement_node = self.get_minimum_node(curr_node)
					replacement_val = replacement_node.val
					replacement_node.val = curr_node.val
					curr_node.val = replacement_val
					self.delete_node(replacement_node)
				return
			
	def search_tree(self, search_val):
		node = self.root
		while node:
			if search_val < node.val:
				node = node.left
			elif search_val > node.val:
				node = node.right
			else:
				return 'found'
		return None
	
	def traversal(self):
		node = self.root
		#self.inorder_dfs(node)
		#self.preorder_dfs(node)
		#self.postorder_dfs(node)
		self.bfs()

	def inorder_dfs(self, node):
		if node is None:
			return
		self.inorder_dfs(node.left)
		print(node.val)
		self.inorder_dfs(node.right)

	def preorder_dfs(self, node):
		if not node:
			return
		print(node.val)
		self.preorder_dfs(node.left)
		self.preorder_dfs(node.right)

	def postorder_dfs(self, node):
		if not node:
			return
		self.postorder_dfs(node.left)
		self.postorder_dfs(node.right)
		print(node.val)

	def bfs(self):
		queue = [self.root]
		while len(queue) != 0:
			node = queue.pop(0)
			if node.left:
				queue.append(node.left)
			if node.right:
				queue.append(node.right)
			print(node.val)


	


				

tree = BST(None)
tree.insert_node(4)
tree.insert_node(2)
tree.insert_node(1)
tree.insert_node(3)
tree.insert_node(8)
tree.insert_node(5)
tree.insert_node(10)
tree.traversal()