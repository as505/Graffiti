from flask import Flask, request, render_template, session, make_response
from PIL import Image
import json
import time

app = Flask(__name__)

image = Image.new("RGB", [1920, 1080], (155, 155, 155))

image.save('static\\wall.png', "PNG")

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    response = make_response(render_template('index.html'))
    client = request.cookies.get('client_id')

    if client == None:
        response.set_cookie('client_id', str(time.time()))
        print("NO COOKIE")
    else:
        print(client)

    if request.method == 'POST':
        data = request.get_json()
        x = data["x"]
        y = data["y"]

        draw(x, y)

    return response

def draw(x, y):
    with Image.open('static\\wall.png') as image:
        image.putpixel((x, y), (255, 255, 255))
        image.save('static\\wall.png', "PNG")
    return True

@app.after_request
def add_header(response):
    response.cache_control.max_age = 1
    return response


if __name__ == '__main__':
    app.run()