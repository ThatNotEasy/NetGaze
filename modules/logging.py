import logging
from colorama import Fore, Style, init

init()

def setup_logging():
    log = logging.getLogger(f"{Fore.YELLOW}[+] {Fore.RED}NetGaze {Fore.YELLOW}[+]{Style.RESET_ALL}")
    log.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        f"{Fore.GREEN}%(asctime)s{Style.RESET_ALL} - "
        f"{Fore.CYAN}%(levelname)s{Style.RESET_ALL} - "
        f"{Fore.WHITE}%(message)s{Style.RESET_ALL}"
    )
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    return log