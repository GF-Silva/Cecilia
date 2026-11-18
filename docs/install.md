# How to install and prepare the environment

**WARNING:** My computer is CachyOS (Arch) and do not have much RAM, so I was unable to validate the commands in windows practical tests, and their uses may be incorrect. Consult the application documentation in case of errors.

If you encounter errors or bugs during installation, please search for tutorials on the web on how to resolve them.

## Requirements

- Python v3.14 (Other versions have not been tested)
- LibMagic
- Git (Used only to install the repo; you can install directly from GitHub if you want)
- Web browser

## Preparing the environment

### Linux

#### Arch

``` bash
# Install libmagic, if it is not on your SO
sudo pacman -S file

# Install Git if you dont have it:
sudo pacman -S git

# Install with paru:
paru -S python314 uv

# Or Install with yay:
yay -S python314 uv

# Copy the repo:
git clone https://github.com/GF-Silva/Cecilia.git
cd Cecilia

# Install python
python3.14 -m venv .venv

# If using fish as a terminal:
source ./.venv/bin/activate.fish

# Otherwise:
source ./.venv/bin/activate

uv sync
```

#### Ubuntu / derivatives

``` bash
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.14 python3.14-venv git curl ca-certificates less -y
sudo apt-get install libmagic-dev
curl -LsSf https://astral.sh/uv/install.sh | sh 
source "$HOME/.local/bin/env"  

git clone https://github.com/GF-Silva/Cecilia.git
cd Cecilia

python3.14 -m venv .venv
source ./.venv/bin/activate
uv sync
```

### Windows

Open a new PowerShell terminal and type the commands:

``` PowerShell
# Install Python 3.14
winget install --id Python.Python.3.14 -e --source winget

# Install Git
winget install --id Git.Git -e --source winget

# Install the repository
git clone https://github.com/GF-Silva/Cecilia.git
cd Cecilia

# Prepare the .venv file with Python
py -3.14 -m venv .venv

# Necessary to prevent script execution errors
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned .\.venv\Scripts\Activate.ps1` `
pip install . 
pip install python-magic-bin
```
