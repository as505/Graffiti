from flask import Flask, request, render_template, session, make_response
from PIL import Image
import json
import datetime
import db
import sqlite3
import uuid


app = Flask(__name__)

# Create blank canvas
image = Image.new("RGB", [1920, 1080], (155, 155, 155))
image.save('static\\wall.png', "PNG")

db.init_app(app)

#db_connection = sqlite3.connect('database.db')

# Number of secconds until client can draw again
USER_COOLDOWN_THRESHOLD = 1

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    response = make_response(render_template('index.html'))
    db_connection = sqlite3.connect('database.db')
    # This authentication is entirely client sided, and can be easily fooled by deleting/editing cookies.
    # Add DB for sever-side auth later

    # Get client ID
    client_token = request.cookies.get('client_token')
    # Make new client if no id is present
    if client_token == None:
        # Create randomized token for user id
        client_token = str(uuid.uuid4())

        # Add to database
        query = f"INSERT INTO idTable (token) VALUES ('{client_token}')"
        db_connection.execute(query)

        db_connection.commit()
        response.set_cookie('client_token', str(client_token))


    if request.method == 'POST':
        current_time = datetime.datetime.now()

        assert client_token != None
        query = f"SELECT id from idTable WHERE token Is '{client_token}'"
        query = "SELECT * from idTable"
        db_result = db_connection.execute(query)
        print(db_result.fetchall())

        # By default we assume user has not waited long enough to draw again
        client_cooldown = 0

            
        # Allow client to draw if user cooldown is high enough
        if client_cooldown > USER_COOLDOWN_THRESHOLD:
            data = request.get_json()
            x = data["x"]
            y = data["y"]

            draw(x, y)
        

    return response

# Change a pixel on the canvas at a specified coordinate
def draw(x, y):
    with Image.open('static\\wall.png') as image:
        image.putpixel((x, y), (255, 255, 255))
        image.save('static\\wall.png', "PNG")
    return True

# Not sure if this does anything
@app.after_request
def add_header(response):
    response.cache_control.max_age = 1
    return response


if __name__ == '__main__':
    app.run()