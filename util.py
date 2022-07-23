from getpass import getuser
import winreg
import re
from os import path
from zipfile import ZipFile

import requests

class Util:
	_silent = False
	_yes = False

	SYSTEM_PATH_REG = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
	USER_PATH_REG = r"Environment"

	def __init__(self, isSuperUser: bool) -> None:
		self.isSuperUser = isSuperUser

	def setOps(self, silent, yes):
		self._silent = silent
		self._yes = yes

	def unzip(self, filePath, outputDir=None) -> None:
		if outputDir==None:
			outputDir=path.basename(filePath)

		with ZipFile(filePath, 'r') as zip:
			zip.extractall(outputDir)

	def downloadFile(self, url, path) -> requests.Response:
		req = requests.get(url)
		if req.status_code == 200:
			content = req.content
			with open(path ,mode='wb') as f:
				f.write(content)
		return req

	def _getKeys(self):
		if self.isSuperUser:
			return (
				winreg.HKEY_LOCAL_MACHINE,
				self.SYSTEM_PATH_REG
			)
		else:
			return (
				winreg.HKEY_CURRENT_USER,
				self.USER_PATH_REG
			)

	def addPath(self, path:str) -> None:
		# 重複削除と追記
		existPath = self.getPath()
		if path[-1] != ";":
			path+=";"
		if path in existPath:
			existPath.replace(path, "")
		self.setPath(path+existPath)


	def setPath(self, path:str) -> None:
		with winreg.CreateKeyEx(*self._getKeys()) as key:
			winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, path)

	def getPath(self) -> str:
		path = None
		with winreg.OpenKeyEx(*self._getKeys()) as key:
			path, _ = winreg.QueryValueEx(key, 'Path')
		return path


	def log(self, msg) -> None:
		print(msg)

	def isAllow(self, string) -> bool:
		# y/n の判定
		if self._yes:
			return True
		while True:
			try:
				result = input(string).lower()
				if result in ["y", "yes"]:
					return True
				elif result in ["n", "no"]:
					return False
				else:
					continue
			except TypeError:
				pass

