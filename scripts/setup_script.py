from typing import Optional
import tbcml
import argparse


def setup(
    cc: tbcml.CC,
    gv: tbcml.GV,
    server_url: str,
    url_regexes: Optional[list[str]] = None,
    apk_path: Optional[str] = None,
    adb: bool = False,
    adb_run_game: bool = False,
):
    if adb_run_game and not adb:
        raise ValueError("adb_run_game can only be True if adb is True")

    if url_regexes is None:
        url_regexes = []

    loader = tbcml.ModLoader(cc, gv)

    print("Initializing mod loader...")
    loader.initialize(apk_path=apk_path)

    script_path = tbcml.Path(__file__).parent().add("ps_script.js")
    script_content = script_path.read().to_str()

    script_content = script_content.replace("{{URL}}", server_url)

    url_regexes_str = "["
    for regex in url_regexes:
        url_regexes_str += f'"{regex}", '
    url_regexes_str = url_regexes_str.strip(", ")
    url_regexes_str += "]"

    script_content = script_content.replace('"{{URL_REGEXES}}"', url_regexes_str)

    script = tbcml.FridaScript(
        "Private Server",
        script_content,
        "all",
        "Hooks into newHttpRequest and replaces the normal url with a custom one",
    )

    mod = tbcml.Mod(
        "Battle Cats Private Server",
        "fieryhenry",
        "Hooks into newHttpRequest to allow you to redirect https requests to your server",
    )

    mod.add_script(script)

    print("Applying mod...")
    loader.apply(mod)

    if adb:
        print("Initializing adb...")
        loader.initialize_adb()

        print("Installing mod...")
        loader.install_adb(run_game=adb_run_game)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--cc",
        help="The country code to use",
        default="en",
        choices=["en", "jp", "kr", "tw"],
    )
    ap.add_argument(
        "--gv",
        help="The game version to use",
        default="13.1.1",
    )
    ap.add_argument("--apk", help="The apk path to use")
    ap.add_argument("--url", help="The server url to use")
    ap.add_argument(
        "--regexes", help="The url regexes to filter for", nargs="*", default=[".*"]
    )
    ap.add_argument(
        "--adb", help="If the apk should be installed with adb", action="store_true"
    )
    ap.add_argument(
        "--adb_run_game",
        help="If the game should be run after installing with adb",
        action="store_true",
    )

    args = ap.parse_args()
    if args.url is None:
        raise ValueError("server_url is required")

    setup(
        args.cc,
        args.gv,
        args.url,
        args.regexes,
        args.apk,
        args.adb,
        args.adb_run_game,
    )


if __name__ == "__main__":
    main()
