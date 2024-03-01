from bcps import server

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Battle Cats Private Server - A private server for The Battle Cats"
    )
    parser.add_argument(
        "--host",
        help="The host to run the server on",
        default="0.0.0.0",
    )
    parser.add_argument(
        "--port",
        help="The port to run the server on",
        default=5000,
    )
    parser.add_argument(
        "--regexes",
        help="The urls to redirect to the private server",
        nargs="*",
        default=[".*"],
    )
    args = parser.parse_args()

    server.start(args.host, args.port, args.regexes)


if __name__ == "__main__":
    main()
