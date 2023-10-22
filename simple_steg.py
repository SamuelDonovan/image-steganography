import argparse
import PIL.Image
import io
import os

# This file was inspired from:
# https://www.youtube.com/watch?v=r-7d3w5xerY


def encode(args):
    # Can accept a file or a string as data to encode.
    if os.path.exists(os.path.dirname(args.data)):
        with open(args.data, "rb") as encode_data:
            args.data = encode_data.read()

    # If data is a string convert to bytes.
    if isinstance(args.data, str):
        args.data = str.encode(args.data)

    # Append data to file.
    with open(args.image, "rb") as image, open(args.output, "wb") as output:
        output.write(image.read())
        output.write(args.data)


def decode(args):
    with open(args.image, "rb") as image, open(args.output, "wb") as output:
        content = image.read()
        # JPG/PNG images end with the two bytes FFD9.
        offset = content.index(bytes.fromhex("FFD9"))
        image.seek(offset + 2)
        output.write(image.read())


def main():
    parser = argparse.ArgumentParser(description="JPG Steganography Tool")

    subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")

    # Subcommand for encoding
    encode_parser = subparsers.add_parser("encode", help="Encode data into an image")
    encode_parser.add_argument("--image", help="Input image file", type=str)
    encode_parser.add_argument(
        "--data", help="Data file to hide in the image", type=str
    )
    encode_parser.add_argument("--output", help="Output image file", type=str)

    # Subcommand for decoding
    decode_parser = subparsers.add_parser("decode", help="Decode data from an image")
    decode_parser.add_argument("--image", help="Input image file", type=str)
    decode_parser.add_argument("--output", help="Output data file", type=str)

    args = parser.parse_args()

    if args.subcommand == "encode":
        encode(args)
    elif args.subcommand == "decode":
        decode(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
