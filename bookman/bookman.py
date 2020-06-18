from bookman.controller.proxy_controller import ProxyController
import sys

def main():
    proxy = ProxyController()
    proxy.run(sys.argv[1:])

if __name__ == '__main__':
    main()
