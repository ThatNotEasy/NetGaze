from modules.netgaze import NETGAZE
from modules.banners import banners

if __name__ == "__main__":
    banners()
    netgaze = NETGAZE()
    netgaze.check_device()
    netgaze.convert_cert()
    netgaze.setup_proxy()