import http.server
import functools
import pathlib
import argparse
import ssl
import dataclasses
import pathlib

@dataclasses.dataclass
class HttpsArgs:
    cert_path: pathlib.Path
    privatekey_path: pathlib.Path


def run_test_server(site_directory: str, port: int, https_args: HttpsArgs|None):
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=site_directory)

    Handler.extensions_map={
            '.manifest': 'text/cache-manifest',
            '.html': 'text/html',
            '.png': 'image/png',
            '.jpg': 'image/jpg',
            '.svg': 'image/svg+xml',
            '.css': 'text/css',
            '.js': 'application/x-javascript',
            '': 'application/octet-stream', # Default
        }

    # global server
    server_address = ("", port)
    server = http.server.HTTPServer(server_address, Handler)

    protocol = None
    if https_args is not None:
        ssl_ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
        ssl_ctx.load_cert_chain(certfile=https_args.cert_path, keyfile=https_args.privatekey_path)
        server.socket = ssl_ctx.wrap_socket(server.socket, server_side=True)
        protocol = "https"
    else:
        protocol = "http"

    print(f"serving at: {protocol}://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=None)
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("-c", "--https-cert", type=str)
    parser.add_argument("-k", "--https-priv-key", type=str)

    args = parser.parse_args()

    served_directory = None
    if args.directory is not None:
        served_directory = pathlib.Path(args.directory).resolve()
        print(f"serving {served_directory}")
    else:
        served_directory = pathlib.Path(".").resolve()
        print(f"serving default directory: {served_directory}")

    https_args = None
    if (args.https_cert is None) != (args.https_priv_key is None):
        parser.error("must provide both or neither --https-cert and --https-priv-key args")
    elif args.https_cert is not None:
        https_args = HttpsArgs(cert_path=args.https_cert, privatekey_path=args.https_priv_key)

    run_test_server(str(served_directory), args.port, https_args)

if __name__ == '__main__':
    main()
