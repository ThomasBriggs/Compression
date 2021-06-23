import Huffman
import argparse

parser = argparse.ArgumentParser(
    description="Compress text files using a huffman tree.")
parser.add_argument('filename')
parser.add_argument('-c', '--compress', dest="compress", action="store_true")
parser.add_argument('-d', '--decompress',
                    dest="decompress", action="store_true")
parser.add_argument('-o', '--output', dest="output_filename", action="store")
args = parser.parse_args()

if args.compress:
    if args.output_filename:
        Huffman.compress_file(args.filename, args.output_filename)
    else:
        Huffman.compress_file(args.filename, "output")
elif args.decompress:
    if args.output_filename:
        Huffman.decompress_file(args.filename, args.output_filename)
    else:
        Huffman.decompress_file(args.filename, "output")
else:
    print(args.filename)
