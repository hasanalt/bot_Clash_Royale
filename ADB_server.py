import os
from ppadb.client import Client as AdbClient
from loguru import logger


class AdbBase:
    def __init__(self, port):
        self.port = self._get_adb_port(port)
        self.client = self._get_adb_client()
        self.device = self._get_device()

    def _get_adb_port(self, port):
        if port.lower() == "bluestacks" or port == "":
            with open(r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf", "r") as f:
                lines = f.readlines()
                for l in lines:
                    if "bst.instance.Nougat64.status.adb_port=" in l:
                        return int(l.split("=")[-1][1:-2])
        return int(port)

    def _get_adb_client(self):
        os.system(r'"adb\adb kill-server"')
        os.system(r'"adb\adb start-server"')
        os.system(fr'"adb\adb connect 127.0.0.1:{self.port}"')
        return AdbClient(host="127.0.0.1", port=5037)

    def _get_device(self):
        devices = self.client.devices()
        return devices[0]

    def check_install_cr(self):
        logger.debug("check_install_cr")
        packages = self.device.shell("pm list packages").split("\r\n")[0].split("\n")
        for package in packages:
            if package == "package:com.supercell.clashroyale":
                logger.debug("check_install_cr -> True")
                return True
        logger.debug("check_install_cr -> False")
        return False

    def check_run_cr(self):
        logger.debug("check_run_cr")
        if self.device.get_pid("com.supercell.clashroyale"):
            logger.debug("check_run_cr -> True")
            return True
        logger.debug("check_run_cr -> False")
        return False

    def open_cr(self):
        logger.debug("open_cr")
        self.device.shell("monkey -p com.supercell.clashroyale -v 15")

    def close_cr(self):
        logger.debug("close_cr")
        self.device.shell("am force-stop com.supercell.clashroyale")

    def click(self, x: int, y: int):
        logger.debug(f"click x = {x} y = {y}")
        self.device.shell(f"input tap {str(x)} {(str(y))}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int):
        logger.debug(f"swipe x1 = {x1} y1 = {y1} x2 = {x2} y2 = {y2}")
        self.device.shell(f"input swipe {str(x1)} {(str(y1))} {str(x2)} {(str(y2))} 2000")

    def get_screen(self):
        logger.debug("get_screen")
        return self.device.screencap()


class AdbServer(AdbBase):
    def __init__(self, port):
        super().__init__(port)

    def add_client(self, port):
        os.system(fr'"adb\adb connect 127.0.0.1:{port}"')
        self.devices = self.client.devices()
        device = self.devices[-1]
        return device

    def reboot(self):
        self.device.shell("reboot")


class AdbClient(AdbBase):
    def __init__(self, port: int):
        super().__init__(port)

    def add_client(self, port):
        pass
