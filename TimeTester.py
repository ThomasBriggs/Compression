import timeit
import Huffman

def time_huffman():
    Huffman.compress_file("example_texts/bee_movie", "output.comp")

time = timeit.timeit(time_huffman, number=10)
print(time)