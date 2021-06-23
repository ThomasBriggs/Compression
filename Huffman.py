from heapq import *
import pickle


class Node:
    def __init__(self, freq):
        self.freq = freq

    def __lt__(self, o):
        if isinstance(o, Node):
            return self.freq < o.freq
        return False


class Leaf(Node):
    def __init__(self, value, freq):
        self.val = value
        super().__init__(freq)

    def __str__(self):
        return 'Value: {0}, Frequency: {1}'.format(self.val, self.freq)

    def __repr__(self):
        return f'{self.val}:{self.freq}'


class Branch(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
        super().__init__(left.freq + right.freq)


class Tree:
    def __init__(self, string):
        heap = self.__heap_dict(self.__get_freq(string))
        while (len(heap) > 1):
            left = heappop(heap)
            right = heappop(heap)
            temp = Branch(left, right)
            heappush(heap, temp)
        self.root = heappop(heap)

    def __get_freq(self, string):
        output_dict = {}
        for i in string:
            if (i in output_dict):
                output_dict[i] += 1
            else:
                output_dict[i] = 1
        return output_dict

    def __heap_dict(self, dict):
        h = []
        for i in dict:
            heappush(h, Leaf(i, dict[i]))
        return h


class EncodingMap:
    def __init__(self, tree: Tree):
        self.encoding_map = {}
        self.__create_map(tree)

    def __create_map(self, tree: Tree):
        root = tree.root
        if isinstance(root, Leaf):
            self.encoding_map[root.val] = 0
        else:
            self.__rec_create_map(root.left, 0)
            self.__rec_create_map(root.right, 1)

    def __rec_create_map(self, node: Node, num: bin):
        if isinstance(node, Leaf):
            self.encoding_map[node.val] = num
        else:
            self.__rec_create_map(node.left, num << 1)
            self.__rec_create_map(node.right, (num << 1)+1)

    def getMap(self):
        return self.encoding_map

    def getMapBin(self):
        temp_map = self.encoding_map
        for i in temp_map:
            temp_map[i] = format(temp_map[i], 'b')
        return temp_map


test_string = "Hello, World! This is a test string"
test_string2 = "a"*15+"b"*7+"c"*6+"d"*6+"e"*5

tree = Tree(test_string2)
encoding_tree = EncodingMap(tree)

encoding_map = encoding_tree.getMapBin()
o = ""
for i in test_string2:
    o += encoding_map[i]

def pad(string):
    pad_amount = (8-(len(string)%8))
    padding = "0"*pad_amount
    return (padding+string, pad_amount)

padded_string, pad_amount = pad(o)

byte_array = bytearray()
for i in range(0, len(padded_string), 8):
    byte = padded_string[i:i+8]
    byte_array.append(int(byte, 2))

newFile = open("test.txt", "wb")
newFile.write(byte_array)
newFile.close

newFile = open("test.txt", "rb")
data = newFile.read()
read_byte_array = bytearray(data)

r = ""
for i in read_byte_array:
    r += format(i, '08b')
r = r[pad_amount::]
print(len(r))

inv_map = {v: k for k, v in encoding_map.items()}

temp = ""
output = ""
for i in r:
    temp += i
    if (temp in inv_map):
        output += inv_map[temp]
        temp = ""
print(output)

