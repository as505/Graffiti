from flask import Flask, request, render_template, session, make_response
from PIL import Image, ImageColor
import json
import datetime
import db
import sqlite3
import uuid
import pathlib


app = Flask(__name__)

SCREEN_RESOLUTION = (1920, 1080)
CANVAS_RESOLUTION = (16, 7)

IMAGE_URL = pathlib.Path("static/wall.png")
# Create blank canvas
image = Image.new("RGB", CANVAS_RESOLUTION, (155, 155, 155))
image.save(IMAGE_URL, "PNG")

# Convert cursor position to canvas pixel
def screen_to_canvas_coords(x, y):
    ratio = SCREEN_RESOLUTION[0] / CANVAS_RESOLUTION[0]

    x2 = int(x/ratio)
    y2 = int(y/ratio)
    
    return (x2, y2)

db.init_app(app)

# Number of secconds until client can draw again
USER_COOLDOWN_THRESHOLD = datetime.timedelta(seconds=2)

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    response = make_response(render_template('index.html'))
    db_connection = sqlite3.connect('database.db')

    # Get client ID
    client_token = request.cookies.get('client_token')
    # Make new client if no id is present
    if client_token is None:
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
        assert client_token is not None
        query = f"SELECT id from idTable WHERE token Is '{client_token}'"
        assert query is not None

        client_id = db_connection.execute(query).fetchone()
        client_id = int(client_id[0])

        # Check timestamp of last action, if any
        query = f"SELECT last_action_ts FROM users WHERE id IS {client_id}"
        last_action = db_connection.execute(query).fetchone()
        
        # Allow user to draw if no actions are registered
        if last_action is None:
            client_cooldown = USER_COOLDOWN_THRESHOLD
        else:
            last_action = last_action[0]
            last_action = datetime.datetime.strptime(last_action, "%Y-%m-%d %H:%M:%S.%f")
            client_cooldown = (current_time - last_action)
        
        # Abort draw request if user has not waited long enough
        if client_cooldown < USER_COOLDOWN_THRESHOLD:
            return response

        # Get drawing coordinates from client
        data = request.get_json()
        x = data["x"]
        y = data["y"]
        color = data["color"]
        # Convert from hex to rgb tuple
        color = ImageColor.getcolor(color, "RGB")

        x, y = screen_to_canvas_coords(x=x, y=y)
        # Perform draw
        draw(x, y, color)
        # Store client timestamp in database
        query = f"UPDATE users SET last_action_ts=('{current_time}') WHERE id is {client_id}"
        db_connection.execute(query)
        db_connection.commit()

    return response

# Change a pixel on the canvas at a specified coordinate
def draw(x, y, color):
    with Image.open(IMAGE_URL) as image:
        image.putpixel((x, y), color)
        image.save(IMAGE_URL, "PNG")

    return True


if __name__ == '__main__':
    app.run()