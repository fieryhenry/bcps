from typing import Optional
import tbcml
import argparse


def setup(
    cc: tbcml.CC,
    gv: tbcml.GV,
    server_url: str,
    apk_path: Optional[str] = None,
    package_name: Optional[str] = None,
    app_name: Optional[str] = None,
    adb: bool = False,
    adb_run_game: bool = False,
):
    if adb_run_game and not adb:
        raise ValueError("adb_run_game can only be True if adb is True")

    loader = tbcml.ModLoader(cc, gv)

    print("Initializing mod loader...")
    loader.initialize(apk_path=apk_path)

    script_path = tbcml.Path(__file__).parent().add("ps_script.js")
    script_content = script_path.read().to_str()

    script_content = script_content.replace("{{URL}}", server_url)

    script = tbcml.FridaScript(
        "Private Server",
        script_content,
        "all",
        "Hooks into newHttpRequest and replaces the normal url with a custom one",
    )

    mod = tbcml.Mod(
        "Battle Cats Private Server",
        "fieryhenry",
        description="A mod that redirects all matching urls to a custom server",
    )

    mod.add_script(script)

    apk = loader.get_apk()
    if package_name is not None:
        apk.set_package_name(package_name)
    if app_name is not None:
        apk.set_app_name(app_name)

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
        help="The country code of the apk",
        default="en",
        choices=["en", "jp", "kr", "tw"],
    )
    ap.add_argument(
        "--gv",
        help="The game version of the apk",
        default="13.1.1",
    )
    ap.add_argument("--apk", help="The apk path to use if you already have one")
    ap.add_argument("--url", help="The server url to send requests to", required=True)
    ap.add_argument(
        "--package-name",
        help="Set the package name of the apk. If blank, it will not be modified",
    )
    ap.add_argument(
        "--app-name",
        help="Set the app name of the apk. If blank, it will not be modified",
    )
    ap.add_argument(
        "--adb", help="If the apk should be installed with adb", action="store_true"
    )
    ap.add_argument(
        "--adb-run-game",
        help="If the game should be run after installing with adb",
        action="store_true",
    )

    args = ap.parse_args()
    setup(
        args.cc,
        args.gv,
        args.url,
        args.apk,
        args.package_name,
        args.app_name,
        args.adb,
        args.adb_run_game,
    )


if __name__ == "__main__":
    main()
