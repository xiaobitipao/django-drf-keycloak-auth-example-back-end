import os
import shutil
import sys


def copy_sitecustomize():
    """Copy sitecustomize.py to the virtual environment's site-packages directory.

    sitecustomize.py is a special file in Python.

    if it exists in Python's site-packages, it will be automatically executed every time Python starts.

    It is often used to automatically execute some initialization logic when all programs start, such as:

        Setting default encoding;

        Modifying sys.path;

        Injecting debugging or logging logic;

        Configuring global environment variables.
    """

    # Get the path to the virtual environment
    project_root = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(project_root, ".venv")
    if not os.path.exists(venv_path):
        raise FileNotFoundError(f"Virtual environment not found at {venv_path}")

    # Get the path to the site-packages directory in the virtual environment
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    site_packages_path = os.path.join(venv_path, "lib", python_version, "site-packages")

    # Specify the path to sitecustomize.py
    sitecustomize_dir = os.path.dirname(os.path.abspath(__file__))
    sitecustomize_src = os.path.join(sitecustomize_dir, "sitecustomize.py")
    sitecustomize_dst = os.path.join(site_packages_path, "sitecustomize.py")

    # Copy sitecustomize.py
    shutil.copyfile(sitecustomize_src, sitecustomize_dst)
    print(f"sitecustomize.py has been copied to {sitecustomize_dst}")


if __name__ == "__main__":
    copy_sitecustomize()
