class ASTNode:
    def __init__(self, node_type: str, value: str = None):
        
        self.node_type = node_type
        self.value = value
        self.left = None
        self.right = None

    def to_dict(self):
      
        node_dict = {'node_type': self.node_type, 'value': self.value}
        if self.left:
            node_dict['left'] = self.left.to_dict()
        if self.right:
            node_dict['right'] = self.right.to_dict()
        return node_dict
