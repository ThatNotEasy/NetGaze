from modules.logging import setup_logging
from colorama import Fore, Style, init
from pathlib import Path
import subprocess

init()

class NETGAZE:
    def __init__(self):
        self.logging = setup_logging()
        self.host = "127.0.0.1"
        self.port = "8000"
        self.cert_file = "certificate/mitmproxy-ca-cert.cer.crt"
        self.output_file = "certificate/mitmproxy-ca.pem"

    def check_device(self):
        self.logging.info(f"{Fore.YELLOW}🔍 Checking connected devices...{Style.RESET_ALL}")
        
        try:
            result = subprocess.run(
                ["adb", "devices", "-l"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                device_list = result.stdout.strip().split("\n")[1:]
                if device_list:
                    self.logging.info(f"{Fore.GREEN}📱 Connected devices:{Style.RESET_ALL}")
                    self.logging.info(f"{Fore.YELLOW}───────────────────────────────────────────────{Fore.RESET}")
                    for device in device_list:
                        if device.strip():
                            device_info = device.strip().split()
                            device_id = device_info[0]
                            device_details = " ".join(device_info[2:])
                            self.logging.info(f"{Fore.CYAN}➤  Device  : {Fore.WHITE}{device_id}{Style.RESET_ALL}")
                            self.logging.info(f"{Fore.CYAN}➤  Details : {Fore.WHITE}{device_details}{Style.RESET_ALL}")
                            self.logging.info(f"{Fore.YELLOW}───────────────────────────────────────────────{Fore.RESET}")
                else:
                    self.logging.warning(f"{Fore.RED}⚠️ No devices found. Please connect an Android device.{Style.RESET_ALL}")
            else:
                self.logging.error(f"{Fore.RED}❌ ADB command failed: {result.stderr.strip()}{Style.RESET_ALL}")

        except FileNotFoundError:
            self.logging.error(f"{Fore.RED}❌ ADB not found. Please ensure ADB is installed and added to your PATH.{Style.RESET_ALL}")
        except Exception as e:
            self.logging.error(f"{Fore.RED}❌ An error occurred while checking devices: {e}{Style.RESET_ALL}")

    def reverse_proxy(self):
        self.logging.info(f"{Fore.YELLOW}🔧 Setting up reverse proxy on port {self.port}...{Style.RESET_ALL}")
        try:
            result = subprocess.run(
                ["adb", "reverse", f"tcp:{self.port}", f"tcp:{self.port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                self.logging.info(f"{Fore.GREEN}✅ Reverse proxy set up successfully on port {self.port}.{Style.RESET_ALL}")
            else:
                self.logging.error(f"{Fore.RED}❌ Failed to set up reverse proxy: {result.stderr.strip()}{Style.RESET_ALL}")
        except FileNotFoundError:
            self.logging.error(f"{Fore.RED}❌ ADB not found. Please ensure ADB is installed and added to your PATH.{Style.RESET_ALL}")
        except Exception as e:
            self.logging.error(f"{Fore.RED}❌ An error occurred while setting up reverse proxy: {e}{Style.RESET_ALL}")

    def set_proxy(self):
        self.logging.info(f"{Fore.YELLOW}🔧 Setting proxy to {self.host}:{self.port}...{Style.RESET_ALL}")
        try:
            result = subprocess.run(
                ["adb", "shell", "settings", "put", "global", "http_proxy", f"{self.host}:{self.port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                self.logging.info(f"{Fore.GREEN}✅ Proxy set successfully to {self.host}:{self.port}.{Style.RESET_ALL}")
            else:
                self.logging.error(f"{Fore.RED}❌ Failed to set proxy: {result.stderr.strip()}{Style.RESET_ALL}")
        except FileNotFoundError:
            self.logging.error(f"{Fore.RED}❌ ADB not found. Please ensure ADB is installed and added to your PATH.{Style.RESET_ALL}")
        except Exception as e:
            self.logging.error(f"{Fore.RED}❌ An error occurred while setting proxy: {e}{Style.RESET_ALL}")

    def clear_proxy(self):
        self.logging.info(f"{Fore.YELLOW}🔧 Clearing proxy...{Style.RESET_ALL}")
        try:
            result = subprocess.run(
                ["adb", "shell", "settings", "put", "global", "http_proxy", ":0"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                self.logging.info(f"{Fore.GREEN}✅ Proxy cleared successfully.{Style.RESET_ALL}")
            else:
                self.logging.error(f"{Fore.RED}❌ Failed to clear proxy: {result.stderr.strip()}{Style.RESET_ALL}")
        except FileNotFoundError:
            self.logging.error(f"{Fore.RED}❌ ADB not found. Please ensure ADB is installed and added to your PATH.{Style.RESET_ALL}")
        except Exception as e:
            self.logging.error(f"{Fore.RED}❌ An error occurred while clearing proxy: {e}{Style.RESET_ALL}")
            
    def convert_cert(self):
        try:
            if not Path(self.cert_file).exists():
                self.logging.info(f"{Fore.RED}❌ Certificate file '{self.cert_file}' not found.{Style.RESET_ALL}")
                return

            subprocess.run(
                ["openssl", "x509", "-in", self.cert_file, "-out", self.output_file, "-outform", "PEM"],
                check=True
            )
            self.logging.info(f"{Fore.GREEN}✅ Certificate converted successfully: {self.output_file}{Style.RESET_ALL}")

        except subprocess.CalledProcessError as e:
            self.logging.info(f"{Fore.RED}❌ Failed to convert certificate: {e}{Style.RESET_ALL}")
        except Exception as e:
            self.logging.info(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")

    def setup_proxy(self):
        self.reverse_proxy()
        self.set_proxy()
        self.logging.info(f"{Fore.GREEN}All has been set, Start capturing now :P")
        self.logging.info(f"{Fore.YELLOW}───────────────────────────────────────────────{Fore.RESET}")

        try:
            process = subprocess.Popen(
                ["mitmweb", "--listen-port", "8000", "--mode", "regular", "--showhost"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.logging.info(output.strip())

            process.wait()

        except KeyboardInterrupt:
            self.logging.info(f"{Fore.YELLOW}🛑 mitmweb stopped by user.{Style.RESET_ALL}")

        except Exception as e:
            self.logging.error(f"{Fore.RED}❌ An error occurred while running mitmweb: {e}{Style.RESET_ALL}")

        finally:
            self.clear_proxy()
            self.logging.info(f"{Fore.GREEN}Proxy has been cleared.{Style.RESET_ALL}")