# 🎬 AMC AI STUDIOS - QUICK FIX GUIDE

## ⚡ Application Not Opening? Follow These Steps:

### For Windows Users:

1. **Make sure Python is installed**
   - Download from: https://www.python.org/downloads/
   - Version 3.10 or higher required
   - ✅ Check "Add Python to PATH" during installation

2. **Double-click `launch.bat`**
   - This will automatically:
     - Create virtual environment
     - Install all dependencies
     - Start the application
   
3. **Open your browser**
   - Go to: http://localhost:5000
   - If browser doesn't open automatically, just type this URL manually

### For Linux/Mac Users (or Manual Start):

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python3 main.py
   ```
   
   OR use the simple launcher:
   ```bash
   python3 start.py
   ```

3. **Open browser:**
   - Go to: http://localhost:5000

### Common Issues:

❌ **"Port 5000 already in use"**
- Solution 1: Close other applications using port 5000
- Solution 2: Edit `.env` file and change `FLASK_PORT=5000` to `FLASK_PORT=5001`

❌ **"Module not found" errors**
- Solution: Run `pip3 install -r requirements.txt`

❌ **Browser doesn't open**
- This is normal! Just manually open: http://localhost:5000

❌ **"Python not found"**
- Solution: Install Python 3.10+ from python.org
- Make sure to check "Add to PATH"

### ✅ Success Indicators:

When the app is running correctly, you'll see:
```
🎬 AMC AI STUDIOS - READY!
✅ Server running at: http://127.0.0.1:5000
```

Then just open that URL in your browser!

### 🎮 Using the Application:

1. **Create Tab** - Make new movies/shows
2. **Projects Tab** - View your productions
3. **Theater Tab** - See the virtual AMC cinema with NPCs

---

**Still having issues?** Check the console output for error messages.
