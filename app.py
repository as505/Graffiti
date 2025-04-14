from flask import Flask, request, render_template, session, make_response
from PIL import Image
import json
import time

app = Flask(__name__)

# Create blank canvas
image = Image.new("RGB", [1920, 1080], (155, 155, 155))
image.save('static\\wall.png', "PNG")

# Number of secconds until client can draw again
USER_COOLDOWN_THRESHOLD = 5


@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    response = make_response(render_template('index.html'))

    # This authentication is entirely client sided, and can be easily fooled by deleting/editing cookies.
    # Add DB for sever-side auth later

    # Get client ID
    client = request.cookies.get('client_id')
    # Make new client if no id is present
    if client == None:
        response.set_cookie('client_id', str(time.time()))


    if request.method == 'POST':
        current_time = time.time()
        # By default we assume user has not waited long enough to draw again
        client_cooldown = 0

        # Check when user last clicked
        last_client_action_ts = float(request.cookies.get('last_client_action_ts'))
        #print(last_client_action_ts)
        if last_client_action_ts == None:
            # User has not drawn before, client side auth only
            client_cooldown = USER_COOLDOWN_THRESHOLD
        else:
            # Try/except since cookie might hold corrupt value
            print(int(current_time - last_client_action_ts))
            try:
                client_cooldown = current_time - last_client_action_ts
            except:
                # Reset client cooldown if anything goes wrong
                client_cooldown = 0
        #print(client_cooldown, "COOLDOWN")
        # Allow client to draw if user cooldown is high enough
        if client_cooldown > USER_COOLDOWN_THRESHOLD:
            data = request.get_json()
            x = data["x"]
            y = data["y"]

            draw(x, y)

        response.set_cookie('last_client_action_ts', str(time.time()))
        

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