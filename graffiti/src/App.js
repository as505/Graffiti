import logo from './logo.svg';
import './App.css';

var pixels_x = 0;
var pixels_y = 0;

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <canvas id="canvas" className="canvas"></canvas>
        <div className="cube">
          <p id="resolution_text">
          </p>
        </div>
      </header>
    </div>
  );
}



get_canvas_resolution()
get_canvas_pixels()
//draw_rect(0, 0, canvas_width, canvas_height)

// Get canvas information from backend
async function get_canvas_resolution(){
  await fetch("/get_canvas_resolution", {
    method: "GET"
  })
    .then((response) => response.json())
    .then((response) => {
      let paragraph = document.getElementById("resolution_text");
      let string = "X: " + response.x + "\nY: " + response.y;
      const text = document.createTextNode(string);
      pixels_x = response.x;
      pixels_y = response.y;
      paragraph.appendChild(text);
    })
}

// Fetch pixels from backend, then call draw to render
async function get_canvas_pixels(params) {
  const response = await fetch("get_canvas_pixels", {
    method: "GET"
  })
    .then((response) => response.json())
    .then((response) => draw_canvas(response))
}

// Render canvas for client
function draw_canvas(pixels){
  const canvas = document.getElementById("canvas");
  let i = 0;
  // Create row for all pixels on this y axis
  const pixel_row = document.createElement("div")
  pixel_row.setAttribute("id", "r "+0)
  pixel_row.setAttribute("Class", "pixel_row");

  canvas.appendChild(pixel_row)

  while (i < pixels_x){
    //console.log(pixels)
    const pixel = document.createElement("div");
    // ID is pixel coordinate
    pixel.setAttribute("id", i+", 0");
    pixel.setAttribute("Class", "pixel");
    pixel_row.appendChild(pixel);
    i += 1;
  }
}


function draw_rect(x, y, w, h){
  const canvas = document.getElementById("canvas");
  const context = canvas.getContext("2d");
  context.beginPath();
  context.rect(x, y, w, h);
  context.stroke();
  context.closePath();
  console.log("rect drawn");
  console.log(w, h);
}


export default App;
