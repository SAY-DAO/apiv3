# apiv3
Refactored version of the backend using django

## TODOs
- Readme
- Setup the project
- **User stories**
    - ✅ As a `logged-out user`, I can `login` to the system and get my `access token`.
    - ✅ As a `user`, I can `renew` my `access token` using `refresh token`.
    - ☐ As a `user`, I can `logout` using my `access/refresh token` so my token will be `blacklisted`.
    - ✅ As an `anon user`, I can `request to veirfy` my `email/phonenumber`, an `otp code` will sent to me.
    - ✅ As an `anon user`, I can `veirfy` my `email/phonenumber` using `otp code`.
    - ☐ As an `anon user`, I can `register` as an `app user` using my `verified email/phonenumber`.
    - ☐ As a `logged-out user`, I can `reset` my `password` using `otp code` sent to my `email/phone`.
    - ☐ As a `logged-out user`, I can `reset` my `password` using `otp code` sent to my `email/phone`.
    - ✅ As an `anon user`, I can `search` for `childs`.

    - ...

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
