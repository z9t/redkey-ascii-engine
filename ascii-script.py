#!/usr/bin/env python3
"""
Multi-script ASCII art generator with colour mapping, threshold controls, and exclusions.
Usage: ascii-script.py [--cli|--web] [--width 80] [--threshold 128] [--max-colors 3]
"""
import sys, os, json, random, argparse, math
from pathlib import Path

SCRIPTS_DB = os.path.join(os.path.dirname(__file__), "..", "references", "character-database.json")

# All scripts with glyphs
SCRIPTS = {
    "arabic":   ["بسم الله","الحمد لله","ما شاء الله","سلام","نور","حياة","قلم","علم"],
    "japanese": ["夢","風","月","花","空","星","海","心","光","影","桜","雪","炎"],
    "korean":   ["달","별","꽃","바다","하늘","숲","빛","소리","길","봄"],
    "chinese":  ["龍","鳳","山","水","天","地","道","禪","雲","霧","虎","鶴","竹","梅"],
    "hindi":    ["प्रेम","शांति","ज्ञान","शक्ति","आकाश","अग्नि","जल","पृथ्वी"],
    "tamil":    ["காதல்","அமைதி","ஞானம்","சக்தி","வானம்","நெருப்பு","நீர்"],
    "cyrillic": ["мир","свет","душа","сила","небо","огонь","вода","земля","ветер"],
    "greek":    ["ψυχή","λόγος","ἀλήθεια","σοφία","χάος","κόσμος","φύσις","πνεῦμα"],
    "thai":     ["ฝัน","ฟ้า","จันทร์","ดาว","น้ำ","ไฟ","ลม","ดิน"],
    "hebrew":   ["שלום","אמת","חכמה","אור","חיים","אהבה","רוח","מים"],
    "georgian": ["მზე","მთვარე","ვარსკვლავი","ზღვა","ცეცხლი","ქარი","დედამიწა"],
    "armenian": ["սեր","լույս","կյանք","ուժ","հույս","հավատ","արև","լուսին"],
    "burmese":  ["အိပ်မက်","ကြယ်","လ","နေ","မီး","ရေ","လေ"],
    "khmer":    ["សុបិន","ផ្កាយ","ព្រះចន្ទ","ព្រះអាទិត្យ","ភ្លើង","ទឹក"],
    "lao":      ["ຝັນ","ດາວ","ເດືອນ","ຕາເວັນ","ນໍ້າ","ໄຟ","ລົມ"],
    "mongolian":["нар","сар","од","гал","ус","тэнгэр","салхи","газар"],
    "tibetan":  ["རྨི་ལམ།","སྐར་མ།","ཟླ་བ།","ཉི་མ།","མེ།","ཆུ།","རླུང་།"],
    "amharic":  ["ፍቅር","ሰላም","ብርሃን","ኃይል","ሕይወት","ውሃ","እሳት"],
    "yiddish":  ["שלום","אמת","ליכט","לעבן","ליבע","האָפענונג","שטערן"],
    "uyghur":   ["ئارزۇ","يۇلتۇز","ئاي","كۈن","ئوت","سۇ","شامال","يەر"],
}

EMOJI_POOL = ["✨","⭐","🌟","💫","🔥","💧","🌊","🌙","☀️","🌍","🌿","🕊️","⚡","🪐","💎","🌈","🎨","🫧","🌀","💀","🧿","🪬","🎭","🪷","🪶","🗿","🏔️","🌋"]

# Colour → script/emoji mapping
COLOR_MAP = {
    "red":    ("chinese", "🔥"),
    "orange": ("arabic", "🧡"),
    "gold":   ("tibetan", "🌟"),
    "yellow": ("mongolian","☀️"),
    "green":  ("arabic", "🌿"),
    "teal":   ("thai", "🫧"),
    "blue":   ("korean", "💧"),
    "purple": ("hindi", "🪷"),
    "pink":   ("japanese", "💎"),
    "white":  ("greek", "🕊️"),
    "grey":   ("georgian","🗿"),
    "black":  ("amharic","🌑"),
}

# Hex → colour name
def hex_to_color(hex_str):
    r, g, b = int(hex_str[1:3],16), int(hex_str[3:5],16), int(hex_str[5:7],16)
    if r > 180 and g < 100 and b < 100: return "red"
    if r > 180 and g > 100 and b < 60:  return "orange"
    if r > 180 and g > 150 and b < 80:  return "gold"
    if r > 180 and g > 180 and b < 100: return "yellow"
    if r < 100 and g > 150 and b < 100: return "green"
    if r < 100 and g > 150 and b > 150: return "teal"
    if r < 100 and g < 150 and b > 180: return "blue"
    if r > 100 and g < 100 and b > 150: return "purple"
    if r > 200 and g > 150 and b > 200: return "pink"
    if r > 180 and g > 180 and b > 180: return "white"
    if 80 < r < 180 and 80 < g < 180 and 80 < b < 180: return "grey"
    return "black"


def generate_art(width=80, height=20, colors=None, threshold_min=20, threshold_max=200, exclude=None):
    """Generate multi-script ASCII art."""
    if not colors:
        colors = ["#FF4444", "#44AAFF", "#FFD700"]
    if not exclude:
        exclude = set()
    
    color_names = [hex_to_color(c) for c in colors[:3]]
    scripts_used = []
    for cn in color_names:
        script, emoji = COLOR_MAP.get(cn, ("japanese", "✨"))
        scripts_used.append((script, emoji, cn))
    
    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            # Perlin-ish noise function
            noise = (math.sin(x * 0.3 + y * 0.5) * math.cos(x * 0.7 - y * 0.3) + 1) * 128
            
            # Threshold clipping
            if noise < threshold_min or noise > threshold_max:
                line += " "
                continue
            
            # Pick colour band based on noise
            noise_norm = noise / 255.0
            band = int(noise_norm * len(scripts_used))
            band = min(band, len(scripts_used) - 1)
            
            script, emoji, col = scripts_used[band]
            
            # Pick glyph
            glyph = random.choice(SCRIPTS.get(script, ["◆"]))
            if random.random() < 0.3:
                glyph = emoji
            
            if glyph in exclude:
                glyph = " "
            
            line += glyph
        
        lines.append(line)
    
    return "\n".join(lines)


def generate_header(width=80, colors=None, title="ASCII SCRIPT"):
    """Generate a multi-script header banner."""
    if not colors:
        colors = ["#FF4444", "#44AAFF", "#FFD700"]
    
    all_glyphs = []
    for script_name in random.sample(list(SCRIPTS.keys()), min(5, len(SCRIPTS))):
        all_glyphs.append(random.choice(SCRIPTS[script_name]))
    
    header = "  ".join(all_glyphs) + "\n"
    header += f"{'=' * width}\n"
    header += f"  {title}\n"
    header += f"{'=' * width}\n\n"
    
    # Colour mapping legend
    color_names = [hex_to_color(c) for c in colors[:3]]
    for cn in color_names:
        script, emoji = COLOR_MAP.get(cn, ("japanese", "✨"))
        sample_glyphs = " ".join(random.sample(SCRIPTS.get(script, ["◆"]), min(3, len(SCRIPTS.get(script, [])))))
        header += f"  {cn:8s} → {script:10s} {emoji}  {sample_glyphs}\n"
    
    header += f"\n{'-' * width}\n"
    return header


def web_server(port=8080):
    """Run a local web interface for visual tweaking."""
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>ASCII Script Generator</title>
<style>
body{font-family:monospace;background:#111;color:#ddd;padding:20px}
canvas{display:block;margin:10px 0}
.controls{display:flex;gap:20px;flex-wrap:wrap}
.control-group{background:#1a1a1a;padding:10px;border-radius:8px}
label{display:block;margin:5px 0;font-size:11px}
input[type="range"]{width:150px}
input[type="color"]{width:40px;height:30px}
#output{white-space:pre;font-size:8px;line-height:1;overflow:auto;max-height:400px;background:#000;padding:10px}
button{padding:8px 16px;background:#333;border:1px solid #555;color:#ddd;cursor:pointer;border-radius:4px}
button:hover{background:#444}
</style></head><body>
<h1>ASCII Script Generator</h1>
<div class="controls">
  <div class="control-group">
    <h3>Colours</h3>
    <label>Colour 1 <input type="color" id="c1" value="#FF4444"></label>
    <label>Colour 2 <input type="color" id="c2" value="#44AAFF"></label>
    <label>Colour 3 <input type="color" id="c3" value="#FFD700"></label>
  </div>
  <div class="control-group">
    <h3>Thresholds</h3>
    <label>Floor <input type="range" id="floor" min="0" max="255" value="30"></label>
    <label>Ceiling <input type="range" id="ceil" min="0" max="255" value="220"></label>
  </div>
  <div class="control-group">
    <h3>Size</h3>
    <label>Width <input type="range" id="w" min="40" max="200" value="100"></label>
    <label>Height <input type="range" id="h" min="10" max="40" value="20"></label>
  </div>
    <div class="control-group">
    <h3>Exclude</h3>
    <input type="text" id="exclude" placeholder="💀🔥 chars to skip" value="">
  </div>
  <div class="control-group">
    <h3>Mode</h3>
    <button onclick="switchMode('static')" id="btn-static" style="background:#555">Static</button>
    <button onclick="switchMode('realtime')" id="btn-realtime">Realtime (ISF)</button>
  </div>
</div>
<button onclick="generate()">Generate</button> <button onclick="saveSkillsHeader()">Save as Skills Header</button>
<canvas id="isfCanvas" width="800" height="400" style="display:none;width:100%;background:#000"></canvas>
<div id="output"></div>
<script>
async function generate(){
  const colors=[document.getElementById('c1').value,document.getElementById('c2').value,document.getElementById('c3').value];
  const floor=parseInt(document.getElementById('floor').value);
  const ceil=parseInt(document.getElementById('ceil').value);
  const w=parseInt(document.getElementById('w').value);
  const h=parseInt(document.getElementById('h').value);
  const ex=document.getElementById('exclude').value;
  const resp=await fetch('/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({colors,floor,ceil,width:w,height:h,exclude:ex})});
  const data=await resp.json();
  document.getElementById('output').innerHTML=data.art;
}
let currentMode='static';
let isfRunning=false;

function switchMode(mode){
  currentMode=mode;
  document.getElementById('btn-static').style.background=mode==='static'?'#555':'#333';
  document.getElementById('btn-realtime').style.background=mode==='realtime'?'#555':'#333';
  if(mode==='realtime'){
    document.getElementById('output').style.display='none';
    document.getElementById('isfCanvas').style.display='block';
    startISF();
  }else{
    document.getElementById('output').style.display='block';
    document.getElementById('isfCanvas').style.display='none';
    stopISF();
  }
}

function startISF(){
  if(isfRunning)return;
  isfRunning=true;
  const canvas=document.getElementById('isfCanvas');
  canvas.width=800; canvas.height=400;
  try{const gl=canvas.getContext('webgl')||canvas.getContext('experimental-webgl');
  if(!gl){console.log('No WebGL');return;}
  const vsSource='attribute vec4 aPos;void main(){gl_Position=aPos;}';
  const fsSource=document.getElementById('isfShader')?.textContent||
  `precision mediump float;uniform vec2 iResolution;uniform float iTime;uniform vec3 iColor1;uniform vec3 iColor2;uniform vec3 iColor3;uniform float iSpeed;uniform float iScale;uniform float iDensity;uniform float iThreshFloor;uniform float iThreshCeil;uniform float iWaves;
float rand(vec2 c){return fract(sin(dot(c,vec2(12.9898,78.233)))*43758.5453);}
float glyph(vec2 uv,float s){vec2 c=floor(uv);vec2 l=fract(uv);float g=rand(c+s);float h=smoothstep(0.2,0.25,l.y)*smoothstep(0.75,0.8,l.y)*step(0.3,g);float v=smoothstep(0.15,0.2,l.x)*smoothstep(0.85,0.9,l.x)*step(0.4,rand(c+s+0.5));float d=abs(l.x-l.y);float di=smoothstep(0.0,0.05,d)*step(0.5,g)*0.7;float cu=length(l-vec2(0.5,0.3))-0.2;float cv=smoothstep(0.0,0.03,abs(cu))*step(0.7,rand(c+s+0.3))*0.6;return max(max(h,v),max(di,cv));}
void main(){vec2 uv=gl_FragCoord.xy/iResolution.xy;float cells=iScale;vec2 cu=uv*cells*vec2(iResolution.x/iResolution.y,1.0);vec2 ci=floor(cu);float n=rand(ci*0.1+iTime*0.3*iSpeed);float w=sin(uv.y*10.0+iTime*0.5)*cos(uv.x*8.0-iTime*0.3)*0.05*iWaves;vec2 wu=cu+w;float g=glyph(wu,ci.x+ci.y*100.0);if(n<iThreshFloor||n>iThreshCeil){gl_FragColor=vec4(0.0);return;}vec3 col=n<0.33?iColor1:n<0.66?iColor2:iColor3;g*=1.0-rand(ci+iTime*0.5)*0.15*iDensity;gl_FragColor=vec4(col*g,g);}`;
  function compile(type,src){const s=gl.createShader(type);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){console.log(gl.getShaderInfoLog(s));gl.deleteShader(s);return null;}return s;}
  const vs=compile(gl.VERTEX_SHADER,vsSource);
  const fs=compile(gl.FRAGMENT_SHADER,fsSource);
  if(!vs||!fs)return;
  const prog=gl.createProgram();
  gl.attachShader(prog,vs);gl.attachShader(prog,fs);gl.linkProgram(prog);
  if(!gl.getProgramParameter(prog,gl.LINK_STATUS)){console.log('Link failed');return;}
  const buf=gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER,buf);
  gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
  const aPos=gl.getAttribLocation(prog,'aPos');
  gl.enableVertexAttribArray(aPos);
  gl.vertexAttribPointer(aPos,2,gl.FLOAT,false,0,0);
  function render(t){
    if(!isfRunning)return;
    gl.viewport(0,0,canvas.width,canvas.height);
    gl.useProgram(prog);
    gl.uniform2f(gl.getUniformLocation(prog,'iResolution'),canvas.width,canvas.height);
    gl.uniform1f(gl.getUniformLocation(prog,'iTime'),t*0.001);
    const c1=document.getElementById('c1');const c2=document.getElementById('c2');const c3=document.getElementById('c3');
    const hex=(c)=>[parseInt(c.value.slice(1,3),16)/255,parseInt(c.value.slice(3,5),16)/255,parseInt(c.value.slice(5,7),16)/255];
    gl.uniform3fv(gl.getUniformLocation(prog,'iColor1'),hex(c1));
    gl.uniform3fv(gl.getUniformLocation(prog,'iColor2'),hex(c2));
    gl.uniform3fv(gl.getUniformLocation(prog,'iColor3'),hex(c3));
    gl.uniform1f(gl.getUniformLocation(prog,'iSpeed'),1.0);
    gl.uniform1f(gl.getUniformLocation(prog,'iScale'),parseInt(document.getElementById('w').value)/10.0);
    gl.uniform1f(gl.getUniformLocation(prog,'iDensity'),0.5);
    gl.uniform1f(gl.getUniformLocation(prog,'iThreshFloor'),parseInt(document.getElementById('floor').value)/255.0);
    gl.uniform1f(gl.getUniformLocation(prog,'iThreshCeil'),parseInt(document.getElementById('ceil').value)/255.0);
    gl.uniform1f(gl.getUniformLocation(prog,'iWaves'),0.0);
    gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
    requestAnimationFrame(render);
  }
  requestAnimationFrame(render);
  }catch(e){console.log('WebGL error:',e);}
}

function stopISF(){isfRunning=false;}

async function saveSkillsHeader(){
  const colors=[document.getElementById('c1').value,document.getElementById('c2').value,document.getElementById('c3').value];
  const resp=await fetch('/save-header',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({colors})});
  alert('Header saved to skills header file');
}
generate();
switchMode('static');
</script></body></html>"""
    
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading
    
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode())
        
        def do_POST(self):
            import json
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            
            if self.path == "/generate":
                colors = body.get("colors", ["#FF4444", "#44AAFF", "#FFD700"])
                floor = body.get("floor", 30)
                ceil = body.get("ceil", 220)
                width = body.get("width", 100)
                height = body.get("height", 20)
                exclude = set(body.get("exclude", ""))
                
                art = generate_header(width, colors) + generate_art(width, height, colors, floor, ceil, exclude)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"art": art}).encode())
            
            elif self.path == "/save-header":
                header = generate_header(80, body.get("colors", ["#FF4444", "#44AAFF", "#FFD700"]))
                path = os.path.join(os.path.dirname(__file__), "..", "references", "ascii-header.txt")
                with open(path, "w") as f:
                    f.write(header)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "path": path}).encode())
    
    server = HTTPServer(("localhost", port), Handler)
    print(f"\n🖥️  ASCII Generator → http://localhost:{port}")
    print(f"   Adjust colours, thresholds, exclusions in real-time")
    print(f"   Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


def cli_mode(args):
    """CLI mode — output directly to terminal."""
    colors = [args.main, args.accent, getattr(args, 'third', args.main)]
    art = generate_header(args.width, colors, args.title or "ASCII SCRIPT")
    art += generate_art(args.width, args.height, colors, args.floor, args.ceiling, set(args.exclude or ""))
    print(art)
    
    if args.save:
        path = os.path.join(os.path.dirname(__file__), "..", "references", "ascii-header.txt")
        header = generate_header(args.width, colors, args.title or "ASCII SCRIPT")
        with open(path, "w") as f:
            f.write(header)
        print(f"\nHeader saved to {path}")


def main():
    parser = argparse.ArgumentParser(description="Multi-script ASCII art generator")
    parser.add_argument("--cli", action="store_true", help="CLI mode")
    parser.add_argument("--web", action="store_true", help="Web mode (default)")
    parser.add_argument("--port", type=int, default=8080, help="Web server port")
    parser.add_argument("--width", type=int, default=100, help="Art width")
    parser.add_argument("--height", type=int, default=20, help="Art height")
    parser.add_argument("--main", default="#FF4444", help="Main colour hex")
    parser.add_argument("--accent", default="#44AAFF", help="Accent colour hex")
    parser.add_argument("--third", help="Third colour hex")
    parser.add_argument("--floor", type=int, default=30, help="Threshold floor (0-255)")
    parser.add_argument("--ceiling", type=int, default=220, help="Threshold ceiling (0-255)")
    parser.add_argument("--exclude", help="Characters/emojis to exclude")
    parser.add_argument("--title", help="Header title")
    parser.add_argument("--save", action="store_true", help="Save header to references")
    args = parser.parse_args()
    
    if args.cli:
        cli_mode(args)
    else:
        web_server(args.port)


if __name__ == "__main__":
    main()
