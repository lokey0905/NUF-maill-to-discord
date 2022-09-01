import poplib
import os.path
import mimetypes
from email.parser import BytesParser, Parser
from email.policy import default
from bs4 import BeautifulSoup

import imaplib
import ssl
ctx = ssl.create_default_context()
ctx.set_ciphers('DEFAULT')

txt=[]
file = []



    
# 輸入郵件地址, 口令和POP3服務器地址
mail = ''
password = ''

pop3_server = 'mail.nfu.edu.tw'

# 連接pop3服務器
# conn = poplib.POP3(pop3_server)
conn = poplib.POP3_SSL(pop3_server,context=ctx)

# 打開調試信息
conn.set_debuglevel(1)
# 可選:打印POP 3服務器的歡迎文字
print(conn.getwelcome().decode('utf-8'))

# 輸入用戶密碼
conn.user(mail)
conn.pass_(password)




def catch(num):
    file = []
    # 獲取服務器上的郵件列表，相當於發送POP 3的list命令
    # resp保存服務器的響應碼
    # mails列表保存每封郵件的編號、大小
    resp, mails, octets = conn.list()
    print(resp, mails)

    # 獲取指定郵件的內容（此處傳入總長度，也就是獲取最後一封郵件）
    # 相當於發送POP 3的retr命令
    # resp保存服務器的響應碼
    # data保存該郵件的內容
    resp, data, octets = conn.retr(num)
    # 將data的所有數據（原本是一個字節列表）拼接在一起
    msg_data = b'\r\n'.join(data)

    # 將字符串內容解析成郵件，需指定解析策略
    msg = BytesParser(policy=default).parsebytes(msg_data)
    print(type(msg))

    print('寄件人:' + msg['from'])
    print('主旨:' + msg['subject'])
    #print('第一個收件人名字:' + msg['to'].addresses[0].username)
    #print('第一個發件人名字:' + msg['from'].addresses[0].username)
    flag=True
    for part in msg.walk():
        counter = 1
        # 如果maintype是multipart，說明是容器（用於包含正文、附件等）
        if part.get_content_maintype() == 'multipart':
            continue
        elif part.get_content_maintype() == 'text':
            
            if flag:
                #print(part.get_content())
                txt=part.get_content()
                flag=False
           
            
        # 處理附件
        else:
            filename = part.get_filename()
            #print(filename)
            file.append(filename)
            if not filename:
                # 根據附件的contnet_type來推測它的後綴名
                ext = mimetypes.guess_extension(part.get_content_type())
                if not ext:
                    ext = '.bin'
                # 程序爲附件來生成文件名
                filename = 'part-%03d%s' % (counter, ext)
            counter += 1
            # 將附件寫入本地文件
            with open(os.path.join('.', filename), 'wb') as fp:
                fp.write(part.get_payload(decode=True))

    # 退出服務器，相當於發送POP 3的quit命令
    # conn.quit()
    txt = '\nNO.'+str(num)+'\n寄件人:'+msg['from']+'\n主旨:'+msg['subject']+'\n'+txt
    txt = [txt[i: i + 2000] for i in range(0, len(txt), 2000)]
    print(txt)
    return (num,txt,file)


def check():

    # 獲取郵件的統計信息，相當於發送pop3的stat命令
    message_num, total_size = conn.stat()
    print('郵件數：%s, 總大小：%s' % (message_num, total_size))

    resp, mails, octets = conn.list()
    print(resp, mails)

    return len(mails)