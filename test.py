import Huffman

with open("./example_texts/example1", "rt") as f:
    string = f.read()
    huffmanTree = Huffman.HuffmanCoding(string)
    print(huffmanTree.get_encoding_map())