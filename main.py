# This is a sample Python script.
from server.DNSServer import XlogfDNS
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    XlogfDNS().setUP(int(os.environ.get('LISTEN_PORT', 53)))
