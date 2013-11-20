import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.header import Header
from traceback import print_exc

def send_mail(from_address,to_address_list,subject,content,attach_list=[],subtype='html'):
    message = MIMEMultipart()
    for file_name in  attach_list:
        attach = MIMEText(open(file_name).read(),'base64','utf8')
        attach['Content-Type'] = 'application/octet-stream'
        attname = '/' in file_name and file_name[file_name.rfind('/')+1:] or file_name
        attach['Content-Disposition'] = 'attachment; filename="%s"'% attname
        message.attach(attach)

    try:
        message.attach(MIMEText(content,subtype))
    except :
        print_exc()
        return

    message['From:']=from_address
    message['To:'] = ','.join(to_address_list)
    message['Subject'] = Header(subject, 'utf8')

    #mail_host = 'smtp.163.com'
    mail_host = 'mail host'

    smtp = smtplib.SMTP()
    smtp.connect(mail_host)
    smtp.login('you user name', 'you mail password')  
    
    print 'sending mail to %s' % to_address_list
    smtp.sendmail(from_address, to_address_list, message.as_string())
    smtp.quit()


if __name__ == '__main__':
    send_mail('flykos@163.com' , 'flykos@163.com' , 'Will' , 'No King Rules Forever')

