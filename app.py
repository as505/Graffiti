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
USER_COOLDOWN_THRESHOLD = datetime.timedelta(seconds=2)

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
        # By default we assume user has not waited long enough to draw again
        client_cooldown = 0
        current_time = datetime.datetime.now()

        # Fetch client ID
        assert client_token != None
        query = f"SELECT id from idTable WHERE token Is '{client_token}'"
        client_id = db_connection.execute(query).fetchone()
        client_id = int(client_id[0])

        # Check timestamp of last action, if any
        query = f"SELECT last_action_ts FROM users WHERE id IS {client_id}"
        last_action = db_connection.execute(query).fetchone()[0]
        
        # Allow user to draw if no actions are registered
        if last_action == None:
            client_cooldown = USER_COOLDOWN_THRESHOLD
        else:
            last_action = datetime.datetime.strptime(last_action, "%Y-%m-%d %H:%M:%S.%f")
            client_cooldown = (current_time - last_action)
        
        # Abort draw request if user has not waited long enough
        if client_cooldown < USER_COOLDOWN_THRESHOLD:
            return response

        # Get drawing coordinates from client
        data = request.get_json()
        x = data["x"]
        y = data["y"]
        # Perform draw
        draw(x, y)
        # Store client timestamp in database
        query = f"UPDATE users SET last_action_ts=('{current_time}') WHERE id is {client_id}"
        db_connection.execute(query)
        db_connection.commit()

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