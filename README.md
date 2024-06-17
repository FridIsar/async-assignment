# Large CSV asynchronous processing

**This app is using Flask 3.0.3 and Python 3.12.3**.

## Tech stack

### Back-end

- [Redis](https://redis.io/)
- [Celery](https://github.com/celery/celery)

### Front-end

- [esbuild](https://esbuild.github.io/)
- [TailwindCSS](https://tailwindcss.com/)
- [Heroicons](https://heroicons.com/)

## Running this app

You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux.

You'll also need to enable Docker Compose v2 support if you're using Docker
Desktop. On native Linux without Docker Desktop you can [install it as a plugin
to Docker](https://docs.docker.com/compose/install/linux/). 

If you're using Windows, it will be expected that you're inside of WSL or WSL 2.

#### Clone this repo anywhere you want and move into the directory:

```sh
git clone https://github.com/fridisar/docker-flask-project project
cd project

# Optionally checkout a specific tag, such as: git checkout 0.11.0
```

#### Copy an project .env file because the real one is git ignored:

```sh
cp .env.project .env
```

#### Build everything:

*The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + Yarn dependencies.*

```sh
docker compose up --build
```

Now that everything is built and running we can treat it like any other Flask 
app.

Did you receive a `depends_on` "Additional property required is not allowed"
error? Please update to at least Docker Compose v2.20.2+ or Docker Desktop
4.22.0+.

Did you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. Check out the docs
in the `.env` file for the `DOCKER_WEB_PORT_FORWARD` variable to fix this.

Did you receive a permission denied error? Chances are you're running native
Linux and your `uid:gid` aren't `1000:1000` (you can verify this by running
`id`). Check out the docs in the `.env` file to customize the `UID` and `GID`
variables to fix this.

#### Setup the initial database:

```sh
# You can run this from a 2nd terminal. It will create both a development and
# test database with the proper user / password credentials.
./run flask db reset --with-testdb
```

#### Check it out in a browser:

Visit <http://localhost:8000> in your favorite browser.

#### Linting the code base:

```sh
# You should get no output (that means everything is operational).
./run lint
```

#### Sorting Python imports in the code base:

```sh
# You should see that everything is unchanged (imports are already formatted).
./run format:imports
```

#### Formatting the code base:

```sh
# You should see that everything is unchanged (it's all already formatted).
./run format
```

*There's also a `./run quality` command to run the above 3 commands together.*

#### Running the test suite:

```sh
# You should see all passing tests. Warnings are typically ok.
./run test
```

#### Stopping everything:

```sh
# Stop the containers and remove a few Docker related resources associated to this project.
docker compose down
```

You can start things up again with `docker compose up` and unlike the first
time it should only take seconds.

### `.env`

This file is ignored from version control so it will never be commit. There's a
number of environment variables defined here that control certain options and
behavior of the application. Everything is documented there.

### `run`

You can run `./run` to get a list of commands and each command has
documentation in the `run` file itself.

It's a shell script that has a number of functions defined to help you interact
with this project. 

## Running a script to automate renaming the project

The app is named `project` right now but chances are your app will be a different
name. Since the app is already created we'll need to do a find / replace on a
few variants of the string "project" and update a few Docker related resources.

And by we I mean I created a zero dependency shell script that does all of the
heavy lifting for you. All you have to do is run the script below.

## Notable opinions and extensions

- **Packages and extensions**:
    - *[gunicorn](https://gunicorn.org/)* for an app server in both development and production
    - *[Flask-DebugToolbar](https://github.com/flask-debugtoolbar/flask-debugtoolbar)* to show useful information for debugging
- **Linting, formatting and testing**:
    - *[flake8](https://github.com/PyCQA/flake8)* is used to lint the code base
    - *[isort](https://github.com/PyCQA/isort)* is used to auto-sort Python imports
    - *[black](https://github.com/psf/black)* is used to format the code base
    - *[pytest](https://github.com/pytest-dev/pytest)* and *pytest-cov* for writing tests and reporting test coverage
- **Blueprints**:
    - Add `page` blueprint to render a `/` page
    - Add `up` blueprint to provide a few health check pages
- **Config**:
    - Log to STDOUT so that Docker can consume and deal with log output 
    - Extract a bunch of configuration settings into environment variables
    - `config/settings.py` and the `.env` file handles configuration in all environments
- **Front-end assets**:
    - `assets/` contains all the CSS, JS, images, fonts, etc. and is managed by esbuild
- **Flask defaults that are changed**:
    - `public/` is the static directory where Flask will serve static files from
    - `static_url_path` is set to `""` to remove the `/static` URL prefix for static files
    - `ProxyFix` middleware is enabled (check `project/app.py`)

#### Run the rename-project script included in this repo:

```sh
# The script takes 2 arguments.
#
# The first one is the lower case version of your app's name, such as myapp or
# my_app depending on your preference.
#
# The second one is used for your app's module name. For project if you used
# myapp or my_app for the first argument you would want to use MyApp here.
bin/rename-project myapp MyApp
```

The [bin/rename-project
script](https://github.com/nickjj/docker-flask-project/blob/main/bin/rename-project)
is going to:

- Remove any Docker resources for your current project
- Perform a number of find / replace actions
- Optionally initialize a new git repo for you

*Afterwards you can delete this script because its only purpose is to assist in
helping you change this project's name without depending on any complicated
project generator tools or 3rd party dependencies.*

If you're not comfy running the script or it doesn't work for whatever reasons
you can [check it
out](https://github.com/nickjj/docker-flask-project/blob/main/bin/rename-project)
and perform the actions manually. It's mostly running a find / replace across
files and then renaming a few directories and files.

#### Start and setup the project:

This won't take as long as before because Docker can re-use most things. We'll
also need to setup our database since a new one will be created for us by
Docker.

```sh
docker compose up --build

# Then in a 2nd terminal once it's up and ready.
./run flask db reset --with-testdb
```

#### Sanity check to make sure the tests still pass:

It's always a good idea to make sure things are in a working state before
adding custom changes.

```sh
# You can run this from the same terminal as before.
./run quality
./run test
```

If everything passes now you can optionally `git add -A && git commit -m
"Initial commit"` and start customizing your app. Alternatively you can wait
until you develop more of your app before committing anything. It's up to you!


#### Official documentation 

- <https://docs.docker.com/>
- <https://flask.palletsprojects.com/>


#### Big thanks to Nick Janetakis <https://nickjanetakis.com> for the Docker + Flask template
