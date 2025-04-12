from flask import Flask, request, render_template
from PIL import Image
import json

app = Flask(__name__)

image = Image.new("RGB", [1920, 1080], (155, 155, 155))

image.save('static\wall.png', "PNG")

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        data = request.get_json()
        x = data["x"]
        y = data["y"]

        draw(x, y)

        return render_template('index.html')
    
    elif request.method == 'GET':

        return render_template('index.html')

def draw(x, y):
    with Image.open('static\wall.png') as image:
        image.putpixel((x, y), (255, 255, 255))
        image.save('static\wall.png', "PNG")
    return True

@app.after_request
def add_header(response):
    response.cache_control.max_age = 1
    return response