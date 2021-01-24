# apiv3
Refactored version of the backend using django

## TODOs
- Readme
- Setup the project
- Setup user apis and user types
- Refactoring panel apis
- Refactoring app apis
- Migrate db


-------------------



Local Development
----------------------------------

### Installing Dependencies

    Make sure u have postgres11+ and redis

    $ sudo apt-get install libpq-dev postgresql redis-server redis-tools

### Setup Python environment
    - Make sure you have python3.8+
    - Install poerty: https://python-poetry.org/docs/#installation
    - (optional but recomended) Enable tab completion: https://python-poetry.org/docs/#enable-tab-completion-for-bash-fish-or-zsh

#### Activating virtual environment
    
    $ poetry shell

#### Upgrade pip and poetry to the latest version

    $ pip install -U pip
    $ poetry self update
  
### Installing dependencies

    $ poetry install

#### For development
    
    $ poetry install --dev

### Migrate DB

    $ poetry run python api/manage.py migrate

### Running locally

    $ poetry run python api/manage.py runserver