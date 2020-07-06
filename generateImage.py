from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io


def generate(matrix):
    if matrix is None:
        raise Exception("Need matrix input")
    text_size = 32
    cell_size = 40
    border_size = 40
    font = ImageFont.truetype("Courier New.ttf", text_size)
    # font = ImageFont.load_default()
    img = Image.new('RGB', (cell_size * 9 + border_size * 2, cell_size * 9 + border_size * 2))
    d = ImageDraw.Draw(img)
    text_width, text_height = d.textsize("0", font)
    black = (0, 0, 0)
    light_gray = (240, 240, 240)
    dark_gray = (180, 180, 180)
    white = (255, 255, 255)
    line_width = 1
    # draw the rectangular grid
    d.rectangle((0, 0, cell_size * 9 + border_size * 2, cell_size * 9 + border_size * 2), outline=white, fill=white)
    d.rectangle((border_size, border_size, cell_size * 9 + border_size, cell_size * 9 + border_size), outline=light_gray, fill=light_gray)
    d.rectangle((cell_size * 3 + border_size, border_size, cell_size * 6 + border_size, cell_size * 3 + border_size), outline=dark_gray, fill=dark_gray)
    d.rectangle((border_size, cell_size * 3 + border_size, cell_size * 3 + border_size, cell_size * 6 + border_size), outline=dark_gray, fill=dark_gray)
    d.rectangle((cell_size * 6 + border_size, cell_size * 3 + border_size, cell_size * 9 + border_size, cell_size * 6 + border_size), outline=dark_gray, fill=dark_gray)
    d.rectangle((cell_size * 3 + border_size, cell_size * 6 + border_size, cell_size * 6 + border_size, cell_size * 9 + border_size), outline=dark_gray, fill=dark_gray)

    # draw the numbers
    # computing where to start to draw the number. The text_height/6 factor is toi adjust for the4 fact that the
    # number is not centered vertically
    y_coord = cell_size / 2 - text_height / 2 - text_height / 6 + border_size
    for row in matrix:
        x_coord = cell_size / 2 - text_width / 2 + border_size
        for element in row:
            if element != 0:
                d.text((x_coord, y_coord), str(element), fill=black, font=font)
            x_coord += cell_size
        y_coord += cell_size

    # add the vertical lines
    for i in range(0, 10):
        if i == 0:
            d.line((i * cell_size + border_size, border_size, i * cell_size + border_size, cell_size * 9 + border_size), fill=black, width=line_width * 2)
        elif i == 9:
            d.line((i * cell_size - line_width + border_size, border_size, i * cell_size - line_width + border_size, cell_size * 9 + border_size), fill=black,
                   width=line_width * 2)
        else:
            d.line((i * cell_size + border_size, border_size, i * cell_size + border_size, cell_size * 9 + border_size), fill=black, width=line_width)

    # add the horizontal lines
    for i in range(0, 10):
        if i == 0:
            d.line((border_size, i * cell_size + border_size, cell_size * 9 + border_size, i * cell_size + border_size), fill=black, width=line_width * 2)
        elif i == 9:
            d.line((border_size, i * cell_size - line_width + border_size, cell_size * 9 + border_size, i * cell_size - line_width + border_size), fill=black,
                   width=line_width * 2)
        else:
            d.line((border_size, i * cell_size + border_size, cell_size * 9 + border_size, i * cell_size + border_size), fill=black, width=line_width)
    s = io.BytesIO()
    img.save(s, 'png')
    return s
