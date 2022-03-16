# Cosmostation Fetch.ai tx extractor
***
### Requirements:
- #### Python 3
- #### Poetry
  - Uses `pyproject.toml` to build a virtual environment and installs all necessary packages
  - Follow installation documentation to configure Poetry for Windows https://python-poetry.org/docs/
- #### Google Chrome
  - IMPORTANT - Chrome must be installed in the default installation folder.
    - For `x86` Chrome should be located at `C:\Program Files (x86)\Google\Chrome` 
    - For `x64` Chrome should be located at `C:\Program Files\Google\Chrome` 
- #### Chrome Driver
  - Find the driver to match your Chrome Browser version. In Chrome menu `Help -> About Google Chrome`
  - Download the correct driver from https://chromedriver.chromium.org/downloads
  - IMPORTANT - Extract the executable file to the root of your Google Chrome installation folder. 
    - e.g. `C:\Program Files\Google\Chrome\chromedriver.exe`

### Installation:
- Open a terminal in root folder and run command `poetry install`
- This will install a virtual environment to a path that looks like this `C:\Users\Username\AppData\Local\pypoetry\Cache\virtualenvs`. Alternatively, run command `poetry env info` in the folder containing `pyproject.toml` and this will display where the virtual environment was installed.

### Run:
- Run program using `poetry run app`


