from bookman.controller.proxy_controller import ProxyController
import logging
import sys


def setup_logging():
    logfmt = '%(asctime)s %(name)s %(funcName)s %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=logfmt,
                        filename='bookman.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(logfmt)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def main():
    setup_logging()
    proxy = ProxyController()
    proxy.run(sys.argv[1:])

if __name__ == '__main__':
    main()
