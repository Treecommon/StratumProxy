import sys
from src.Proxy.server import StratumServer
from src.Helper.config_reader import ConfigReader
import time
import socket
from src.Model.logger import Logger
from src.Api.api import Api

if __name__ == '__main__':
    arg = sys.argv[1]
    print('Mining using ' + arg)

    list_conns = []
    setting = ConfigReader(arg)
    api = Api(arg, setting.get_coins())

    port = setting.get_server_port()

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server.bind(("0.0.0.0", port))
        server.listen(5)

        while True:
            list_conns.append(StratumServer(arg, server, api).run())

            list_conns = [conn for conn in list_conns if not conn.exit_signal]
            Logger.warning('list_conns' + str(len(list_conns)))

    except Exception as e:
        print('Error', e)
        sys.exit()
