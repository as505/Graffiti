import logo from './logo.svg';
import './App.css';


var canvas_width = 200
var canvas_height = 100


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <canvas id="canvas" width={canvas_width} height={canvas_height}></canvas>
        <div className="cube">
          <p>
            test ing text
          </p>
        </div>
      </header>
    </div>
  );
}


hello_world()
draw_rect(0, 0, canvas_width, canvas_height)

function hello_world(){
  console.log("Hello world react!");
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
