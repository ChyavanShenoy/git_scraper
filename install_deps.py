#! /usr/bin/env python3
# Function: Install dependencies for the project

import sys
import subprocess
import pkg_resources

required_packages = {
    'pip', 'requests', 'passlib',  'datetime', 'gitpython'
}


def install(missing_packages):
    if missing_packages:
        print(F"Missing packages: {missing_packages}")
        print("Installing missing packages...")
        python = sys.executable
        subprocess.check_call(
            [python, '-m', 'pip', 'install', *missing_packages], stdout=subprocess.DEVNULL)
        print("Done.")
    else:
        print("All packages are installed.")
        print("Updating packages...")
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install',
                              '--upgrade', *required_packages], stdout=subprocess.DEVNULL)
        print("Done.")


def main():
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = required_packages - installed_packages
    install(missing_packages=missing_packages)


if __name__ == "__main__":
    main()
