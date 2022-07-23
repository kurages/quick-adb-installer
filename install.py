import argparse
import os
import sys
import re
import subprocess
import shutil

from util import Util

class Install:
	GOOGLE_USB_DRIVER_URL = "https://dl.google.com/android/repository/usb_driver_r13-windows.zip"
	PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
	SYSTEM_DEFAULT_INSTALL_DIR = os.environ["ProgramW6432"] + r"\platform-tools"
	USER_DEFAULT_INSTALL_DIR = os.environ["APPDATA"] + r"\platform-tools"

	def __init__(self, parser:argparse.ArgumentParser, util:Util) -> None:
		self.parser = parser
		self.util = util
		parser.add_argument(
			"--prefix",
			help="Specifying the installation directory"
		)

	def _downloadFiles(self):
		self.util.log("Downloading drivers now...")
		self.util.downloadFile(self.GOOGLE_USB_DRIVER_URL, "usb_driver.zip")

		self.util.log("Downloading platform tools now...")
		self.util.downloadFile(self.PLATFORM_TOOLS_URL, "platform-tools.zip")

	def _installDriver(self):
		self.util.log("Driver deployment now...")
		self.util.unzip("usb_driver.zip", ".")

		self.util.log("Installing driver...")
		subprocess.run("PNPUTIL /add-driver usb_driver\\android_winusb.inf /install", shell=True)

	def _installTools(self):
		# zipの解凍とpathに追加
		if os.path.exists(self.prefix):
			shutil.rmtree(self.prefix)
		self.util.log("Driver deployment now...")
		self.util.unzip("platform-tools.zip", ".")
		self.util.log("Installing tools...")
		shutil.move(r".\platform-tools", self.prefix)

		self.util.log("Adds a install dir to the path")
		self.util.addPath(self.prefix)


	def confirm(self):
		# インストール確認
		self.util.log(f"innstall dir: {self.prefix}")
		if not self.util.isAllow(
			"Have you checked the terms of use and installation directory for the drivers and "
			+ "toolsHave you checked the terms of use and installation directory for the usb drivers and platform tools?"
			+ "[y/n]"
		):
			sys.exit(1)

	def clean(self):
		# dlしたファイル類の削除
		self.util.log("Temporary files are deleted.")
		shutil.rmtree("usb_driver")
		for i in ["usb_driver.zip", "platform-tools.zip"]:
			os.remove(i)


	def run(self, args):
		if args.prefix == None:
			if self.util.isSuperUser:
				self.prefix = self.SYSTEM_DEFAULT_INSTALL_DIR
			else:
				self.prefix = self.USER_DEFAULT_INSTALL_DIR
		else:
				self.prefix = args.prefix

		self.confirm()
		self._downloadFiles()
		self._installDriver()
		self._installTools()
		self.clean()
		self.util.log("ok. all complete!")



