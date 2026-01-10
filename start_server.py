import subprocess
import sys
import time

print("Starting Django development server...")
try:
    proc = subprocess.Popen(
        [sys.executable, "manage.py", "runserver"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Read first few lines to check if started
    for _ in range(5):
        line = proc.stdout.readline()
        if line:
            print(line.strip())
            if "Starting development server" in line:
                print("✅ Server started successfully!")
                break
    
    # Keep server running
    time.sleep(3600)  # Keep for 1 hour
except Exception as e:
    print(f"Error: {e}")
