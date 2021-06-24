from heapq import *
import json


class Node:
    def __init__(self, children= None, value=None, freq=None):
        if children is not None:
            self.left = children[0]
            self.right = children[1]
            self.freq = self.right.freq + self.left.freq
            self.value = self.left.__get_value() + self.right.__get_value()
        else:
            self.left = None
            self.right = None
            self.value = value
            self.freq = freq

    def __lt__(self, o):
        if isinstance(o, Node):
            return self.freq < o.freq
        return False

    def __get_value(self):
        if self.left is None and self.right is None:
            return self.value
        else:
            return self.left.__get_value() + self.right.__get_value()

    def __repr__(self):
        return f'{self.__get_value()}:{self.freq}'

    def is_leaf(self):
        return self.left is None or self.right is None

class Tree:
    def __init__(self, string):
        heap = self.__heap_dict(self.__get_freq(string))
        while (len(heap) > 1):
            left = heappop(heap)
            right = heappop(heap)
            temp = Node([left, right])
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
            heappush(h, Node(value=i, freq=dict[i]))
        return h

    def test(self, string):
        return self.__heap_dict(self.__get_freq(string))


class HuffmanCoding:
    def __init__(self, string):
        self.encoding_map = {}
        self.string = string
        tree = Tree(string)
        self.__create_map(tree)

    def __create_map(self, tree):
        root = tree.root
        if root.is_leaf():
            self.encoding_map[root.value] = "0"
        else:
            self.__rec_create_map(root.left, "0")
            self.__rec_create_map(root.right, "1")

    def __rec_create_map(self, node: Node, num: str):
        if node.is_leaf():
            self.encoding_map[node.value] = num
        else:
            self.__rec_create_map(node.left, num + "0")
            self.__rec_create_map(node.right, num + "1")

    def get_encoding_map(self):
        return self.encoding_map

    def get_decoding_map(self):
        return {v: k for k, v in self.encoding_map.items()}

    def encode(self, pad=True):
        o = ""
        for i in self.string:
            o += self.encoding_map[i]
        if not pad:
            return o
        else:
            return self.__pad(o)

    def __pad(self, string):
        pad_amount = (8-(len(string) % 8))
        padding = "0"*pad_amount
        return (padding+string, pad_amount)

    def decode(self, string):
        temp = ""
        output = ""
        inv_map = self.get_decoding_map()
        for i in string:
            temp += i
            if (temp in inv_map):
                output += inv_map[temp]
                temp = ""
        return output

    def __text_to_bytearray(self):
        compressed_text_bytes = bytearray()
        padded_string, pad_amount = self.encode()
        for i in range(0, len(padded_string), 8):
            byte = padded_string[i:i+8]
            compressed_text_bytes.append(int(byte, 2))
        return compressed_text_bytes, int(pad_amount)

    def __map_to_bytearray(self):
        map_bytes = bytearray(json.dumps(self.get_decoding_map()), "utf-8")
        return map_bytes, len(map_bytes)

    def compress_to_file(self, filename):
        text_bytes, pad_amount = self.__text_to_bytearray()
        map_bytes, map_size = self.__map_to_bytearray()
        pad_amount_bytes = pad_amount.to_bytes(1, "big")
        map_size_bytes = map_size.to_bytes(4, "big")
        with open(filename, "wb") as f:
            f.write(pad_amount_bytes)
            f.write(map_size_bytes)
            f.write(map_bytes)
            f.write(text_bytes)

def compress_file(input_filename, output_filename):
    with open(input_filename, "rt") as f:
        string = f.read()
    huffman_tree = HuffmanCoding(string)
    huffman_tree.compress_to_file(output_filename)

def decompress_file(input_filename, output_filename):
    with open(input_filename, "rb") as f:
        pad_amount_read = int.from_bytes(f.read(1), "big")
        map_size_read = f.read(4)
        map_bytes_read = f.read(int.from_bytes(map_size_read, "big"))
        compressed_text_bytes_read = f.read()

    r = ""
    for i in compressed_text_bytes_read:
        r += format(i, '08b')
    r = r[pad_amount_read::]

    inv_map = json.loads(map_bytes_read)
    temp = ""
    output = ""
    for i in r:
        temp += i
        if (temp in inv_map):
            output += inv_map[temp]
            temp = ""

    with open(output_filename, "wt") as f:
        f.write(output)

if __name__ == '__main__':
    with open("example_texts\example1", "rt") as f:
        string = f.read()
    huffman = HuffmanCoding(string)
    hmap = huffman.get_encoding_map()
    print(hmap)
