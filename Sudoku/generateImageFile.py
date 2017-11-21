import json
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io

def main(input_dict):

    try:
        print("input dictionary:")
        print(json.dumps(input_dict))
        matrix = input_dict.get('matrix', None)

        if matrix  is None:
            raise Exception("Need matrix input")
        else:
            matrix = [[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]
            # text = "1 2 3 4 5 6 7 8 9\n2 3 4 5 6 7 8 9 1\n3 4 5 6 7 8 9 1 2\n4 5 6 7 8 9 1 2 3\n5 6 7 8 9 1 2 3 4\n6 7 8 9 1 2 3 4 5\n7 8 9 1 2 3 4 5 6\n8 9 1 2 3 4 5 6 7\n9 1 2 3 4 5 6 7 8"
            # text = "1 2 3 4 5 6 7 8 9"
            text_size = 36
            font = ImageFont.truetype("CourierNew.ttf", text_size)
            img = Image.new('RGB', (text_size*9, text_size*9))
            d = ImageDraw.Draw(img)
            text_width, text_height = d.textsize("0",font)
            black = (0,0,0)
            light_gray = (240,240,240)
            dark_gray = (180,180,180)
            line_width = 1
            # draw the rectangular grid
            d.rectangle((0, 0, text_size*9, text_size*9), outline=light_gray, fill=light_gray)
            d.rectangle((text_size*3, 0, text_size*6, text_size*3), outline=dark_gray, fill=dark_gray)
            d.rectangle((0, text_size*3, text_size*3, text_size*6), outline=dark_gray, fill=dark_gray)
            d.rectangle((text_size*6, text_size*3, text_size*9, text_size*6), outline=dark_gray, fill=dark_gray)
            d.rectangle((text_size*3, text_size*6, text_size*6, text_size*9), outline=dark_gray, fill=dark_gray)

            # draw the numbers
            # computing where to start to draw the number. The text_height/6 factor is toi adjust for the4 fact that the number is not centered
            # vertically
            y_coord = text_size/2 - text_height/2 - text_height/6
            for row in matrix:
                x_coord = text_size/2 - text_width/2
                for element in row:
                    d.text((x_coord, y_coord), str(element), fill=black, font=font)
                    x_coord += text_size
                y_coord += text_size

            # add the vertical lines
            for i in range(0,10):
                if i == 0:
                    d.line((i * text_size, 0, i * text_size, text_size * 9), fill=black, width=line_width*2)
                elif i == 9:
                    d.line((i * text_size - line_width*2, 0, i * text_size - line_width*2, text_size * 9), fill=black,
                           width=line_width*2)
                else:
                    d.line((i * text_size, 0, i * text_size, text_size * 9), fill=black, width=line_width)

            # add the horizontal lines
            for i in range(0,10):
                if i == 0:
                    d.line((0, i * text_size, text_size * 9, i * text_size), fill=black, width=line_width)
                elif i == 9:
                    d.line((0, i * text_size-line_width*2, text_size * 9, i * text_size-line_width*2), fill=black, width=line_width*2)
                else:
                    d.line((0, i * text_size, text_size * 9, i * text_size), fill=black, width=line_width)

            img.save("matrix.png")

            s = io.BytesIO()
            img.save(s, 'png')
            png = s.getvalue()

            return_results = {"headers": {"Content-Type": "image/png"},
             "statusCode": 200,
             "body": png}
            print("return:")
            print(return_results)
            return return_results
    except Exception as error:
        error = {"statusCode": 500, "body": str(error)}
        print(error)
        return error

# This invocation does not happen in Whisk, only outside
if __name__ == '__main__':
    if len(sys.argv) == 2:
        main({"matrix": sys.argv[1]})
    else:
        raise Exception("Need matrix input")
