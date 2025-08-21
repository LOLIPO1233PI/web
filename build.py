import subprocess

try:
    print("=> Starting Process!")
    subprocess.run(["python", "-m", "setup", "sdist", "bdist_wheel"], check=True)
    print("=> Process finished!")
except subprocess.CalledProcessError:
    print("=> Packaging process didn't finish succesfully :(")
