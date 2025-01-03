# qrcode-lego
# Copyright (C) 2025 jgfh2
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import pyqrcode
from pyqrcode import QRCode
from pprint import pprint
import json
from PIL import Image, ImageDraw, ImageFont
import argparse

def parse_arguments():
    # Known valid security options
    VALID_SECURITY_TYPES = ['WEP', 'WPA', 'nopass']
    VALID_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    # Create ArgumentParser
    parser = argparse.ArgumentParser(
        description="Lego QR Code Generator",
        add_help=False  # Disable default help to customize it
    )

    # Help flag (custom implementation)
    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help="Show this help message and exit."
    )

    # Required arguments
    parser.add_argument(
        '-s', '--ssid',
        type=str,
        required=True,
        help="The SSID of the WiFi network (required)."
    )
    parser.add_argument(
        '-p', '--password',
        type=str,
        required=True,
        help="The WiFi password (required)."
    )

    # Optional arguments
    parser.add_argument(
        '-S', '--security',
        type=str,
        choices=VALID_SECURITY_TYPES,
        default='WPA',
        help="The security type of the WiFi network (default: WPA). Options: WEP, WPA, nopass."
    )
    parser.add_argument(
        '-H', '--hidden',
        action='store_true',
        default=False,
        help="Flag indicating if the WiFi network is hidden (default: False)."
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help="The output file name (must be an image file: .jpg, .jpeg, .png, .gif, .bmp)."
    )

    # Parse arguments
    args = parser.parse_args()

    return args

def qr_to_array(qr_text):
    """
    Generate a QR code from the input text and output a 2D array of 1s and 0s representing QR code cells.

    Parameters:
        qr_text (str): The text to encode in the QR code.

    Returns:
        list of list of int: 2D array representation of the QR code cells.
    """
    # Generate the QR code
    qr = pyqrcode.create(qr_text, error='L')

    # Convert the QR code to a 2D array
    qr_array = [[1 if cell else 0 for cell in row] for row in qr.code]

    return qr_array

def all1(iteralble):
    for element in iteralble:
        if element != 1:
            return False
    return True

def all0(iterable):
    for element in iterable:
        if element != 0:
            return False
    return True

def minimize_lego_pieces(qr_array, lego_pieces):
    # Sort LEGO pieces by price per area (ppa) ascending
    lego_pieces = sorted(lego_pieces, key=lambda piece: piece['area'], reverse=True)

    parts = []

    qr_size = len(qr_array)

    for lego_piece in lego_pieces:
        for i in range(qr_size):
            for j in range(qr_size):
                # test normal orientation
                fits_normal_black = True
                fits_normal_white = True
                if i + lego_piece['width'] <= qr_size and j + lego_piece['length'] <= qr_size: # Check we're not going off the right side or bottom.
                    for x in range(lego_piece['width']):
                        if not all1(qr_array[i+x][j:j+lego_piece['length']]):
                            fits_normal_black = False
                        if not all0(qr_array[i+x][j:j+lego_piece['length']]):
                            fits_normal_white = False
                    if fits_normal_black:
                        # add the piece to the parts list.
                        parts.append({
                            "id": lego_piece['id'],
                            "row": i,
                            "col": j,
                            "width": lego_piece['width'],
                            "length": lego_piece['length'],
                            "orientation": "normal",
                            "colour": "black"
                        })
                        # zero the qr_array 'under' the piece, so we don't overlap another piece.
                        for x in range(lego_piece['width']):
                            for y in range(lego_piece['length']):
                                qr_array[x+i][j+y] = 2
                    if fits_normal_white:
                        # add the piece to the parts list.
                        parts.append({
                            "id": lego_piece['id'],
                            "row": i,
                            "col": j,
                            "width": lego_piece['width'],
                            "length": lego_piece['length'],
                            "orientation": "normal",
                            "colour": "white"
                        })
                        # zero the qr_array 'under' the piece, so we don't overlap another piece.
                        for x in range(lego_piece['width']):
                            for y in range(lego_piece['length']):
                                qr_array[x+i][j+y] = 2
                fits_rotated_black = True
                fits_rotated_white = True
                if i + lego_piece['length'] <= qr_size and j + lego_piece['width'] <= qr_size: # Check we're not going off the right side or bottom.
                    for x in range(lego_piece['length']):
                        if not all1(qr_array[i+x][j:j+lego_piece['width']]):
                            fits_rotated_black = False
                        if not all0(qr_array[i+x][j:j+lego_piece['width']]):
                            fits_rotated_white = False
                    if fits_rotated_black:
                        # add the piece to the parts list.
                        parts.append({
                            "id": lego_piece['id'],
                            "row": i,
                            "col": j,
                            "width": lego_piece['length'],
                            "length": lego_piece['width'],
                            "orientation": "normal",
                            "colour": "black"
                        })
                        # zero the qr_array 'under' the piece, so we don't overlap another piece.
                        for x in range(lego_piece['length']):
                            for y in range(lego_piece['width']):
                                qr_array[x+i][j+y] = 2
                    if fits_rotated_white:
                        # add the piece to the parts list.
                        parts.append({
                            "id": lego_piece['id'],
                            "row": i,
                            "col": j,
                            "width": lego_piece['length'],
                            "length": lego_piece['width'],
                            "orientation": "normal",
                            "colour": "white"
                        })
                        # zero the qr_array 'under' the piece, so we don't overlap another piece.
                        for x in range(lego_piece['length']):
                            for y in range(lego_piece['width']):
                                qr_array[x+i][j+y] = 2

    return parts

def generate_lego_image(parts, qr_size, outfile):
    """
    Generate a PNG image displaying the LEGO pieces on the QR code grid.

    Parameters:
        parts (list of dict): List of LEGO parts and their positions.
        qr_size (int): Size of the QR code grid (number of cells).

    Returns:
        None: Saves the image as 'lego_qr_code.png'.
    """
    parts_list = f"""QR size: {qr_size}
You need a base plate at least {qr_size+6} x {qr_size+6} studs in size.
This ensures you have a sufficient quiet area around the qr code.

"""
    parts_list += print_shopping_list(parts)

    parts_list_length = parts_list.count('\n') * 24

    cell_size = 20  # Size of each cell in pixels
    image_width = (qr_size+6) * cell_size
    image_height = (qr_size+9) * cell_size + parts_list_length

    # Create a white background image
    img = Image.new("RGB", (image_width, image_height), "lightblue")
    draw = ImageDraw.Draw(img)

    # Draw each LEGO piece
    for part in parts:
        x1 = (part['col'] + 3) * cell_size
        y1 = (part['row'] + 3) * cell_size
        x2 = x1 + part['length'] * cell_size if part['orientation'] == "normal" else x1 + part['width'] * cell_size
        y2 = y1 + part['width'] * cell_size if part['orientation'] == "normal" else y1 + part['length'] * cell_size

        # Draw the piece (border and fill)
        draw.rectangle([x1, y1, x2, y2], fill=part['colour'], outline="grey")
        for i in range(part['length']):
            for j in range(part['width']):
                draw.circle((x1+(cell_size/2)+(i*cell_size),y1+(cell_size/2)+(j*cell_size)), cell_size * 2/6,fill=part['colour'], outline="grey", width=1)

    font = ImageFont.load_default(20)
    draw.multiline_text((3 * cell_size, (qr_size+6) * cell_size),parts_list,font=font, fill='black', spacing=4)

    # Save the image
    img.save(outfile)
    print(f"Image saved as '{outfile}'")
    img.show()

def print_shopping_list(parts):
    shopping_list = {
        'black': {},
        'white': {}
    }
    for part in parts:
        if part['id'] in shopping_list[part['colour']]:
            shopping_list[part['colour']][part['id']] += 1
        else:
            shopping_list[part['colour']][part['id']] = 1

    output = 'BLACK PARTS\n'
    for key, value in shopping_list['black'].items():
        output +=f'Part Number: {key} x {value}\n'
    output += '\n'
    output +='WHITE PARTS\n'
    for key, value in shopping_list['white'].items():
        output +=f'Part Number: {key} x {value}\n'

    output += '\n'
    output +='Consider buying using brickowl to minimise costs:\n'
    output +='https://www.brickowl.com/\n'

    return output
    



def print_qr_code(qr_array):
    blank_line = ""
    for i in range(len(qr_array)+4):
        blank_line += "██"

    print(blank_line)
    print(blank_line)
    for i in range(len(qr_array)):
        line = "████"
        for j in range(len(qr_array)):
            if qr_array[i][j]:
                line += "  "
            else:
                line += "██"
        line += "████"
        print(line)
    print(blank_line)
    print(blank_line)
    print()
    print("If this looks janky, increase the size of your terminal!")


def main():

    args = parse_arguments()

    # Create the Wi-Fi string
    wifi_string = f"WIFI:S:{args.ssid};T:{args.security};P:{args.password};H:{args.hidden};;"

    # load the available plates
    with open('plates.json','r',encoding='utf-8') as f:
        plates = json.load(f)

    qr_array = qr_to_array(wifi_string)

    # print(f"QR Code is {len(qr_array)} cells in size.")


    # Minimize LEGO pieces
    parts = minimize_lego_pieces(qr_array, plates)

    # Generate PNG
    generate_lego_image(parts, len(qr_array),args.output)

    # print the shopping list
    print_shopping_list(parts)


if __name__ == "__main__":
    main()