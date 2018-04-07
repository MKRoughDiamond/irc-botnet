from bot.handler.base import BaseMessageHandler
import hashlib
from datetime import date, datetime
import functools
import random
from bot.utils.crawler import wiki_crawler
from bot.utils.card import draw
import re


class ShiroHandler(BaseMessageHandler):
    def __init__(self, transport, loop, settings=None):
        super(ShiroHandler, self).__init__(transport, loop, settings)

    def handle(self, message):
        super(ShiroHandler, self).handle(message)
        if message.command == 'PRIVMSG':
            channel = message.params[0]
            content = message.params[1]
            if content[0:3]=='!시로':
                tension = self.getTension(channel)
                if content.replace(" ","")=='!시로':
                    if tension > 70:
                        self.send_message(channel,'...무슨..일? 안 바쁘면...게임..할까?')
                    elif tension > 50:
                        self.send_message(channel,'...?')
                    else:
                        self.send_message(channel,'...')
                    return
                content = content[3:].strip(' ')
                if content=='쓰담' or content=='쓰다듬기':
                    if tension > 70:
                        self.send_message(channel, '시로......행복..!')
                    elif tension > 50:
                        self.send_message(channel, '나쁘지...않을지도..')
                    else:
                        self.send_message(channel,'...')
                    self.modifyTension(channel[1:],tension+random.randrange(250,300)/10)
                elif content=='공백':
                    self.send_message(channel,'「　　」은 절대로 지지 않아..!')
                elif content[0:2]=='뽑기':
                    
                    if tension <=50:
                        self.send_message(channel,'...')
                        return
                    content = content[3:].strip(' ')
                    num = 1
                    try:
                        if content!='' or content is not None:
                            for i in content:
                                if i < '0' or i> '9':
                                    raise ValueError
                            num = int(content)
                            if num<1:
                                raise ValueError
                            if num>5:
                                self.send_message(channel,'너무...많아..5장만')
                                num=5
                    except ValueError:
                        self.send_message(channel,'장난...치지마')
                        self.modifyTension(channel[1:],tension-10.0)
                        return
                    self.send_message(channel,'뽑은 카드는...'+draw(num))
                    if tension <= 70:
                        self.send_message(channel,'조금...졸린걸')
                    self.modifyTension(channel[1:],tension-random.randrange(10,30)/10)
                elif content[0:2]=='확률':
                    content = content[3:].strip(' ')
                    if content is None or content =='':
                        self.send_message(channel,'대상...없어...계산..불가?')
                        return
                    prob = '{:.2f}'.format(random.random()*100)
                    if tension > 70:
                        self.send_message(channel,'계산.....완료. 확률..'+prob+'%')
                    elif tension > 50:
                        self.send_message(channel,'확률...'+prob+'%...조금..졸린걸')
                    else:
                        self.send_message(channel,'...')
                        return
                    self.modifyTension(channel[1:],tension-random.randrange(10,100)/10)
                elif content[0:2]=='위키':
                    target = (content[3:].strip(' ')).lower().title()
                    target = re.sub('\s+','_',target)
                    banlist = ['Main_Page',':','.php','=']
                    for i in banlist:
                        if i in target:
                            self.send_message(channel,'제대로‥.검색..해줘')
                    url,summary = wiki_crawler(target)
                    if tension <= 50:
                        self.send_message(channel,'...')
                        return
                    if url is None or 'not exist. You can' in summary:
                        self.send_message(channel,'정확한...결과...없음. 실수......아냐?')
                    else:
                        if summary is None:
                            self.send_message(channel,url)
                        else:
                            self.send_message(channel,url)
                            self.send_message(channel,summary+'...')
                    if tension > 50 and tension < 70:
                        self.send_message(channel,'...조금...졸린걸')
                    self.modifyTension(channel[1:],tension-random.randrange(10,100)/10)
                elif content=='소라':
                    self.send_message(channel,'빠~~!♡')
                    self.modifyTension(channel[1:],100.0)
                elif content=='-help':
                    self.send_message(channel,'시로....기계아냐..')
                    self.send_message(channel,'<system> (!시로) 쓰담, 쓰다듬기, 공백, 소라, 확률 (내용), 뽑기 (5 이하 자연수), 위키 (검색)이 가능합니다.')
                    self.send_message(channel,'<system> 시로의 기분을 좋게 해주세요. 일을 하면 피곤해 합니다.')
                    self.send_message(channel,'..? 방금.....누구?')
        elif message.command == 'INVITE':
            channel = message.params[1]
            self.join_channel(channel)
            self.send_message(channel,'시로...'+channel[1:]+'에...빠...는 어디?')
            self.modifyTension(channel[1:],100.0)
        elif message.command == 'MODE':
            nick = message.nick
            channel = message.params[0]
            mode = message.params[1]
            to = message.params[2:]
            tension = self.getTension(channel)
            if mode[0:2] == '+o':
                if 'Shiro' in to:
                    self.send_message(channel,nick+', Good Job!')
                    self.modifyTension(channel[1:],tension+20.0)
            elif mode[0:2] == '-o':
                if 'Shiro' in to:
                    self.send_message(channel,nick+'.....심술쟁이..')
                    self.modifyTension(channel[1:],tension-30.0)


    def modifyTension(self,channel, value):
        fw = open("./bot/data/"+channel+".shiro",'w')
        if value>100:
            fw.write('{:.1f}'.format(100.0))
        elif value<0:
            fw.write('{:.1f}'.format(0.0))
        else:
            fw.write('{:.1f}'.format(value))
        fw.close()

    def getTension(self,channel):
        fr = open("./bot/data/"+channel[1:]+".shiro",'r')
        tension = float(fr.readline())
        fr.close()
        return tension

export_handler = ShiroHandler
