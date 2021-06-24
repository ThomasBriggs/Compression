from random import randint
import timeit

with open("example_texts\\bible.txt", 'rt') as f:
    string = f.read()

huffman = Huffman.HuffmanCoding(string)
encoded_string = huffman.encode()


