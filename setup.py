import argparse
import ctypes

from install import Install
from uninstall import Uninstall
from util import Util

class Setup:
	"""adb quick innstaller / uninstaller"""

	def __init__(self) -> None:
		self.util = Util(bool(ctypes.windll.shell32.IsUserAnAdmin()))

		self.parser = argparse.ArgumentParser(description=self.__doc__)
		self.parser.add_argument(
			"-s", "--silent",
			action="store_true",
			help="No dialogue required.",
			default=False
		)

		self.parser.add_argument(
			"-y", "--yes",
			action="store_true",
			help="Automatic Acceptance of Prompts",
			default=False
		)

		self.subparsers = self.parser.add_subparsers()
		install = self.subparsers.add_parser('install',
			help="install adb command",
		)
		install.set_defaults(handler=Install(install, self.util).run)


		uninstall = self.subparsers.add_parser('uninstall',
			help="uninstall adb command",
		)
		uninstall.set_defaults(handler=Uninstall(uninstall, self.util).run)

	def run(self):
		args = self.parser.parse_args()
		self.util.setOps(args.silent, args.yes)
		if hasattr(args, 'handler'):
			args.handler(args)
		else:
			self.parser.print_help()


if __name__ == "__main__":
	try:
		Setup().run()
	except KeyboardInterrupt:
		print("canceled by user")


