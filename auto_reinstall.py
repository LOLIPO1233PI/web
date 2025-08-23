import subprocess

try:
    print("=> Starting Process!")
    subprocess.run(
        [
            "python",
            "-m",
            "pip",
            "install",
            "--forcereinstall",
            "dist/web-0.1-py3-none-any.whl ",
        ],
        check=True,
    )
    print("=> Process finished!")
except subprocess.CalledProcessError:
    print("=> Packaging process didn't finish succesfully :(")
