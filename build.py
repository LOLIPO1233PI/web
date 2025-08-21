import subprocess

try:
    subprocess.Popen(["python", "setup.py", "sdist", "bdist_wheel"])
except subprocess.SubprocessError:
    print("packaging process didn't finish succesfully")
