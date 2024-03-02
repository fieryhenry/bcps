# Battle Cats Private Server

A private server for the mobile game The Battle Cats built with
[Flask](https://flask.palletsprojects.com),
[tbcml](https://github.com/fieryhenry/tbcml), and
[Frida](https://frida.re).

Note that if you just want to have a custom mailbox, I suggest that you use
[mailboxhack](https://github.com/fieryhenry/mailboxhack) instead as it doesn't
need a private server.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/fieryhenry)

## Installation

1. Clone the repository

   ```bash
   git clone https://github.com/fieryhenry/bcps.git
   cd bcps
   ```

1. Install with pip

   If pip is in your PATH:

   ```bash
   pip install -e .
   ```

   If pip is not in your PATH:

   Windows:

   ```bash
   py -m pip install -e .
   ```

   Everything else:

   ```bash
   python -m pip install -e .
   ```

To pull the latest changes from the repository you can run the following
command. Make sure you are in the bcps directory.

```bash
git pull
```

## Setting up the APK

1. Install [tbcml](https://github.com/fieryhenry/tbcml#from-source-recommended)
   including the scripting dependencies.

1. Run the setup script. Use the `--help` flag for more information about the
   available options. Such as country code, game version, and adb.

```bash
python scripts/setup_script.py --help
```

You need to specify the url to the server in the `--url` option. The url needs
to be https otherwise the game will not send the request. A way to get around
this is to use a reverse proxy such as [ngrok](https://ngrok.com/), or
[serveo](https://serveo.net/) to handle this for you. I have used serveo as you
can set a custom subdomain and it seems to work well.

```bash
ssh -R custom_subdomain:80:localhost:5000 serveo.net
```

This gives you a url like `https://custom_subdomain.serveo.net`. You can then
use this url in the `--url` option.

```bash
python scripts/setup_script.py --url https://custom_subdomain.serveo.net
```

You can also specify the country code and game version. The country code is
`en` by default and the game version is `13.1.1` by default. You can specify the
country code and game version with the `--cc` and `--gv` options respectively.

```bash
python scripts/setup_script.py --url https://custom_subdomain.serveo.net --cc "en" --gv "13.1.1"
```

The setup script does auto-download the apk for you, but if you already have an
apk you can specify the path to the apk with the `--apk` option.

```bash
python scripts/setup_script.py --url https://custom_subdomain.serveo.net --apk "path/to/apk"
```

If you have adb setup and want to install the apk to your device automatically
you can use the `--adb` option, and optionally the `--adb_run_game` flag to
start the game after the apk is installed.

```bash
python scripts/setup_script.py --url https://custom_subdomain.serveo.net --adb --adb_run_game
```

You can change the package name and app name with the `--package_name` and
`--app_name` options respectively. The default package name is
`jp.co.ponos.battlecatsen` and the default app name is `The Battle Cats` for en.

```bash
python scripts/setup_script.py --url https://custom_subdomain.serveo.net --package_name "jp.co.ponos.battlecatsen" --app_name "The Battle Cats" 
```

The game will log the url it is sending requests to. If you want to see this run
`adb logcat` with the tag `tbcml` if you have adb setup.

```bash
adb logcat -s tbcml
```

## Running the server

1. Run the server

```bash
python -m bcps
```

You should pass in `--regexes`, which is a list to specify which urls should be
redirected to the private server. The default is `.*` which is all urls.

```bash
python -m bcps --regexes "presents" "events"
```

You can pass in a specific host and port with the `--host` and `--port` options
respectively. The defaults are shown below.

```bash
python -m bcps --host 0.0.0.0 --port 5000
```

To run in debug mode you can use the `--debug` flag.

```bash
python -m bcps --debug
```

## Adding your own endpoints

The server comes with a mailbox example blueprint in
[`src/bcps/blueprints/presents`](src/bcps/blueprints/presents.py). You should
read the [Flask documentation](https://flask.palletsprojects.com) to understand
how to create your own endpoints.

Note that the frida script also forces the verification of the nyanko signture,
so as long as the Nyanko-Signature header is present, the server will accept the
request. (see present.py for an example of how to do this.)

Note that any url that is redirected to the private server always starts with a
prefix of `/api`.

You should place your blueprints in the
[`src/bcps/blueprints`](src/bcps/blueprints) directory. You can then add the
blueprint to the app in the
[`src/bcps/blueprints/__init__.py`](src/bcps/blueprints/__init__.py) file.

You can access the domain the game sent the original request to with
the domain query parameter.

```python
from flask import request
# ...
domain = request.args.get("domain")
```

You can also get the package name and version of the game with the
`package_name` and `package_version` query parameters.

```python
from flask import request
# ...
package_name = request.args.get("package_name")
package_version = request.args.get("package_version")
```

You can also get the game's request handle with the `req_handle` query
parameter. This is used by the game to determine what function should be run
after the request is completed. This probably isn't useful for most people, but
it is there if you need it.

```python
from flask import request
# ...
req_handle = request.args.get("req_handle")
```
