# This is a copy of welcome.py in JKsTwilioApp project

import os
from flask import Flask, jsonify, request, redirect
from twilio.twiml.messaging_response import MessagingResponse, Message, Body, Redirect
import json
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io

def gen_image():
    matrix = [[0, 7, 0, 6, 0, 9, 0, 8, 0], [4, 0, 2, 0, 0, 0, 0, 0, 3], [0, 0, 9, 4, 1, 0, 2, 5, 0],
              [8, 0, 0, 0, 9, 0, 3, 0, 5], [0, 0, 4, 8, 0, 5, 6, 0, 0], [5, 0, 1, 0, 7, 0, 0, 0, 9],
              [0, 6, 8, 0, 5, 2, 4, 0, 0], [1, 0, 0, 0, 0, 0, 7, 0, 6], [0, 4, 0, 3, 0, 1, 0, 9, 0]]
    # text = "1 2 3 4 5 6 7 8 9\n2 3 4 5 6 7 8 9 1\n3 4 5 6 7 8 9 1 2\n4 5 6 7 8 9 1 2 3\n5 6 7 8 9 1 2 3 4\n6 7 8 9 1 2 3 4 5\n7 8 9 1 2 3 4 5 6\n8 9 1 2 3 4 5 6 7\n9 1 2 3 4 5 6 7 8"
    # text = "1 2 3 4 5 6 7 8 9"
    text_size = 36
    font = ImageFont.truetype("CourierNew.ttf", text_size)
    img = Image.new('RGB', (text_size * 9, text_size * 9))
    d = ImageDraw.Draw(img)
    text_width, text_height = d.textsize("0", font)
    black = (0, 0, 0)
    light_gray = (240, 240, 240)
    dark_gray = (180, 180, 180)
    line_width = 1
    # draw the rectangular grid
    d.rectangle((0, 0, text_size * 9, text_size * 9), outline=light_gray, fill=light_gray)
    d.rectangle((text_size * 3, 0, text_size * 6, text_size * 3), outline=dark_gray, fill=dark_gray)
    d.rectangle((0, text_size * 3, text_size * 3, text_size * 6), outline=dark_gray, fill=dark_gray)
    d.rectangle((text_size * 6, text_size * 3, text_size * 9, text_size * 6), outline=dark_gray, fill=dark_gray)
    d.rectangle((text_size * 3, text_size * 6, text_size * 6, text_size * 9), outline=dark_gray, fill=dark_gray)

    # draw the numbers
    # computing where to start to draw the number. The text_height/6 factor is toi adjust for the4 fact that the number is not centered
    # vertically
    y_coord = text_size / 2 - text_height / 2 - text_height / 6
    for row in matrix:
        x_coord = text_size / 2 - text_width / 2
        for element in row:
            d.text((x_coord, y_coord), str(element), fill=black, font=font)
            x_coord += text_size
        y_coord += text_size

    # add the vertical lines
    for i in range(0, 10):
        if i == 0:
            d.line((i * text_size, 0, i * text_size, text_size * 9), fill=black, width=line_width * 2)
        elif i == 9:
            d.line((i * text_size - line_width * 2, 0, i * text_size - line_width * 2, text_size * 9), fill=black,
                   width=line_width * 2)
        else:
            d.line((i * text_size, 0, i * text_size, text_size * 9), fill=black, width=line_width)

    # add the horizontal lines
    for i in range(0, 10):
        if i == 0:
            d.line((0, i * text_size, text_size * 9, i * text_size), fill=black, width=line_width)
        elif i == 9:
            d.line((0, i * text_size - line_width * 2, text_size * 9, i * text_size - line_width * 2), fill=black,
                   width=line_width * 2)
        else:
            d.line((0, i * text_size, text_size * 9, i * text_size), fill=black, width=line_width)

    # img.save("matrix.png")
    s = io.BytesIO()
    img.save(s, 'png')
    png = s.getvalue()
    return png


app = Flask(__name__)

@app.route('/')
def welcomeToMyapp():
    return 'Welcome again to my Twilio app running on Bluemix!'

@app.route('/test')
def test():
    png = gen_image()
    print(str(png))
    return str(png)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    try:
        account_sid = "ACefa1096c033ccd122b24a0480cfb21c5"
        auth_token = "4d965a0c6fd26c27070ccf849f817ac4"

        request_headers = str(request.headers)
        request_data = str(request.data)
        incoming_number = request.form['From']
        incoming_message = request.form['Body']

        print('Request data: \n%s\n' % request_data)
        print('Request headers: \n%s\n' % request_headers)

        response = MessagingResponse()
        response.message('%s from %s' % (incoming_message, incoming_number))
        print(response)

        png = gen_image()
        print(str(png))

        return str(response)
    except Exception as error:
        return {"error": str(error)}

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
