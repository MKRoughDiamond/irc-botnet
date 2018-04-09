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
                        self.send_message(channel,self.dotGen()+'무슨'+self.dotGen()+'일? 안 바쁘면'+self.dotGen()+'게임'+self.dotGen()+'할까?')
                    elif tension > 50:
                        self.send_message(channel,self.dotGen()+'?')
                    else:
                        self.send_message(channel,self.dotGen())
                    return
                content = content[3:].strip(' ')
                if content=='쓰담' or content=='쓰다듬기':
                    if tension > 70:
                        self.send_message(channel, '시로'+self.dotGen()+'행복'+self.dotGen(3)+'!')
                    elif tension > 50:
                        self.send_message(channel, '나쁘지'+self.dotGen()+'않을지도'+self.dotGen())
                    else:
                        self.send_message(channel,self.dotGen())
                    self.modifyTension(channel[1:],tension+random.randrange(100,150)/10)
                elif content=='공백':
                    self.send_message(channel,'「　　」은 절대로 지지 않아'+self.dotGen()+'!')
                elif content[0:2]=='뽑기':
                    
                    if tension <=50:
                        self.send_message(channel,self.dotGen())
                        return
                    content = content[3:].strip(' ')
                    num = 1
                    try:
                        if content!='' and content is not None:
                            for i in content:
                                if i < '0' or i> '9':
                                    raise ValueError
                            num = int(content)
                            if num<1:
                                raise ValueError
                            if num>5:
                                self.send_message(channel,'너무'+self.dotGen()+'많아'+self.dotGen()+'5장만')
                                num=5
                    except ValueError:
                        self.send_message(channel,'장난'+self.dotGen()+'치지마')
                        self.modifyTension(channel[1:],tension-10.0)
                        return
                    self.send_message(channel,'뽑은 카드는'+self.dotGen()+draw(num))
                    if tension <= 70:
                        self.send_message(channel,'조금'+self.dotGen()+'졸린걸')
                    self.modifyTension(channel[1:],tension-random.randrange(10,30)/10)
                elif content[0:2]=='확률':
                    content = content[3:].strip(' ')
                    if content is None or content =='':
                        self.send_message(channel,'대상'+self.dotGen()+'없어'+self.dotGen()+'계산'+self.dotGen()+'불가?')
                        return
                    if '오늘' in content:
                        random.seed(str(datetime.now().date())+content)
                    else:
                        random.seed(content)
                    prob = '{:.2f}'.format(random.random()*100)
                    if tension > 70:
                        self.send_message(channel,'계산'+self.dotGen()+'완료. 확률'+self.dotGen()+prob+'%')
                    elif tension > 50:
                        self.send_message(channel,'확률'+self.dotGen()+prob+'%'+self.dotGen()+'조금'+self.dotGen()+'졸린걸')
                    else:
                        self.send_message(channel,self.dotGen())
                        return
                    self.modifyTension(channel[1:],tension-random.randrange(50,100)/10)
                    random.seed()
                elif content[0:2]=='위키':
                    target = (content[3:].strip(' ')).lower().title()
                    target = re.sub('\s+','_',target)
                    banlist = ['Main_Page',':','.php','=']
                    for i in banlist:
                        if i in target:
                            self.send_message(channel,'제대로'+self.dotGen()+'검색'+self.dotGen()+'해줘')
                    url,summary = wiki_crawler(target)
                    if tension <= 50:
                        self.send_message(channel,'...')
                        return
                    if url is None or 'not exist. You can' in summary:
                        self.send_message(channel,'정확한'+self.dotGen()+'결과'+self.dotGen()+'없음. 실수'+self.dotGen(3)+'아냐?')
                    else:
                        if summary is None:
                            self.send_message(channel,url)
                        else:
                            self.send_message(channel,url)
                            self.send_message(channel,summary+'...')
                    if tension > 50 and tension < 70:
                        self.send_message(channel,self.dotGen(4)+'조금'+self.dotGen()+'졸린걸')
                    self.modifyTension(channel[1:],tension-random.randrange(50,100)/10)
                elif content=='소라':
                    self.send_message(channel,'빠~~!♡')
                    self.modifyTension(channel[1:],100.0)
                elif content=='-help' or content=='-도움말':
                    self.send_message(channel,'시로'+self.dotGen()+'기계아냐'+self.dotGen())
                    self.send_message(channel,'<system> (!시로) 쓰담, 쓰다듬기, 공백, 소라, 확률 (내용), 뽑기 (5 이하 자연수), 위키 (검색), -help(-도움말)이 가능합니다.')
                    self.send_message(channel,'<system> 시로의 기분을 좋게 해주세요. 일을 하면 피곤해 합니다.')
                    self.send_message(channel,self.dotGen(4)+'? 방금'+self.dotGen()+'누구?')
        elif message.command == 'INVITE':
            channel = message.params[1]
            self.join_channel(channel)
            self.send_message(channel,'시로'+self.dotGen()+channel[1:]+'에'+self.dotGen()+'빠'+self.dotGen()+'는 어디?')
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
                    self.send_message(channel,nick+self.dotGen()+'심술쟁이'+self.dotGen())
                    self.modifyTension(channel[1:],tension-30.0)


    def modifyTension(self,channel, value):
        print(channel)
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

    def dotGen(self,value=None):
        if value is None:
            value=5
        n = random.randint(2,value)
        return '.'*n

export_handler = ShiroHandler
