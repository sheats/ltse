# LTSE Coding Challenge

### Setup

Run the following commands to get your local environment setup.  I use [pyenv](https://github.com/pyenv/pyenv) to manage different versions of python on my machine.

NOTE: Sourcing the activate script once the virtual environment is created should be enough but I was running into some `PATH` conflicts so am suggesting `./.env/bin/python` vs just `python` just to be sure.

```bash
python3.7 -m venv ./.env
source ./.env/bin/activate
./.env/bin/pip install -r requirements.txt
./.env/bin/python main.py
```

### Running Tests

```bash
./.env/bin/py.test
```

### Notes:

I noticed after awhile that a huge focus of my code and testing started to be focused on data validation.  Since the data being used is known I decided to stop focusing on data validation since it seems to be over-engineering for this excercise.  In a real system we'd def want validate all data coming in before sending it off to the trading system.