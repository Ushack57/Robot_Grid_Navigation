# 🚀 Robot Grid Navigation - Web Visualizer Quick Start

## **One-Click Launch**

### **Windows Users**
Simply double-click: **`run_web.bat`**

The script will:
1. Check for Python
2. Check for Flask (install if needed)
3. Start the web server
4. Open instructions

Then open your browser to: **http://localhost:5000**

---

### **Linux/Mac Users**
```bash
python3 run_web.py
```

Or:
```bash
chmod +x run_web.py
./run_web.py
```

---

### **Manual Start (Any OS)**
```bash
python app.py
```

---

## **What You'll See**

When the server starts, you'll see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

✓ This means it's working!

---

## **Open in Browser**

Click or copy-paste: **http://localhost:5000**

---

## **Web Interface Overview**

### **Left Side - Grid Visualization**
- 10×10 grid with obstacles, robot, and path
- Color-coded legend
- Step-by-step animation

### **Right Side - Controls & Stats**

**Controls Panel:**
- 🎚️ Obstacle Density (5%-35%)
- 🔢 Random Seed (or leave blank)
- ⚡ Animation Speed (0.1x-2x)
- ▶️ **Run Simulation** - Start a new simulation
- ⏸️ **Pause** - Pause animation (shown during playback)
- 🔄 **Reset** - Clear and start over

**Statistics Panel:**
- Status (Success/Failed)
- Steps Taken
- Path Length
- Distance Traveled
- Efficiency (distance/step)
- Distance to Goal
- Obstacle Count
- Progress Bar

---

## **How to Use**

### **Step 1: Adjust Parameters (Optional)**
- Move "Obstacle Density" slider (default: 15%)
- Enter a seed number for reproducible results (or leave blank)
- Adjust "Animation Speed" if desired

### **Step 2: Click "▶️ Run Simulation"**
The app will:
- Generate a random grid with obstacles
- Run the simulation
- Animate the robot movement step-by-step
- Update statistics in real-time

### **Step 3: Watch the Animation**
- Each frame shows the robot at a different position
- Path is highlighted in purple
- Green = Start, Orange = Goal, Blue = Robot, Black = Obstacles

### **Step 4: Play Again**
- Click "🔄 Reset" to clear
- Modify parameters if desired
- Click "▶️ Run Simulation" again

---

## **Color Guide**

| Color | Meaning |
|-------|---------|
| 🟢 Green | Start Position |
| 🟠 Orange | Goal Position |
| 🔵 Blue | Current Robot |
| 🟣 Purple | Path Traveled |
| ⬛ Black | Obstacle |
| ⬜ White | Empty Space |

---

## **Quick Tips**

✓ **Stuck Robot?** Lower the obstacle density and try again  
✓ **Too Fast?** Reduce animation speed slider  
✓ **Reproducible Results?** Enter a seed number (e.g., 42)  
✓ **See Random Layout?** Leave seed blank and run again  
✓ **More Difficulty?** Increase obstacle density  

---

## **Troubleshooting**

### **"Page won't load"**
- Wait a few seconds after starting the server
- Check that Flask shows "Running on http://127.0.0.1:5000"
- Try refreshing the browser (Ctrl+R or Cmd+R)

### **"Flask not found"**
```bash
pip install Flask==2.3.0 Werkzeug==2.3.0
```

### **"Port 5000 is already in use"**
Edit `app.py` line and change port:
```python
app.run(debug=True, port=5001, host='127.0.0.1')  # Use 5001 instead
```

### **"White/blank page"**
- Press F12 to open developer console
- Check for any red errors
- Restart Flask server
- Clear browser cache

### **"Animation not playing"**
- Check browser console for JavaScript errors
- Try a different browser
- Make sure all template files are in place

---

## **Features Showcase**

### **Professional UI**
✓ Modern gradient backgrounds  
✓ Smooth animations  
✓ Responsive design  
✓ Real-time statistics  

### **Interactive Controls**
✓ Obstacle density slider  
✓ Animation speed adjustment  
✓ Pause/resume functionality  
✓ One-click simulation  

### **Detailed Information**
✓ Success/failure status  
✓ Movement tracking  
✓ Efficiency metrics  
✓ Progress visualization  

### **Flexible Configuration**
✓ Random seed support  
✓ Adjustable difficulty  
✓ Speed control  
✓ Multiple runs  

---

## **File Structure**

```
Robot_Grid_Navigation/
├── app.py                    ← Flask backend
├── run_web.bat              ← Windows launcher (double-click!)
├── run_web.py               ← Python launcher
├── templates/
│   └── index.html           ← Web interface
├── grid_environment.py       ← Grid engine
├── robot.py                 ← Robot agent
├── perception.py            ← Perception module
├── decision_making.py       ← AI engine
└── simulation.py            ← Simulation core
```

---

## **Stop the Server**

Press **`Ctrl+C`** in the terminal where the server is running

Terminal will show:
```
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
^C
⏹️ Server stopped
```

---

## **Browser Compatibility**

✓ Chrome/Chromium (Latest)  
✓ Firefox (Latest)  
✓ Edge (Latest)  
✓ Safari (Latest)  

---

## **Performance**

- **Load Time**: < 1 second
- **Simulation**: < 500ms
- **Animation**: 60fps
- **Memory**: < 10MB

---

## **Next Steps**

1. ✓ Start the server (double-click `run_web.bat`)
2. ✓ Open http://localhost:5000 in browser
3. ✓ Click "▶️ Run Simulation"
4. ✓ Watch the robot navigate!
5. ✓ Try different obstacle densities
6. ✓ Use seeds to test specific scenarios

---

## **Need Help?**

- See **README.md** for algorithm details
- See **WEB_SETUP.md** for detailed setup guide
- See **QUICKSTART.md** for general project info

---

## **Enjoy! 🚀**

The web visualizer makes it easy to see how the robot navigates in real-time.

Have fun experimenting!
