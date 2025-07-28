import subprocess
import sys
import os

# Clone the repository if not already cloned
if not os.path.isdir("pya3"):
    subprocess.run(["git", "clone", "https://github.com/jerokpradeep/pya3.git"], check=True)

# Change into the directory
os.chdir("pya3")

# Install the package
subprocess.run([sys.executable, "-m", "pip", "install", "."], check=True)
