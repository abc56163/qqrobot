from typing import Optional
from nonebot import on_command, CommandSession, on_notice
from nonebot import on_natural_language, NLPSession, IntentCommand
import os
import time
import MySQLdb
import jieba
jieba.load_userdict(os.path.dirname(__file__)+'/dict.txt')

db = MySQLdb.connect("localhost", "root", "Abcd520025@", "58dh", charset='utf8')

# 保持mysql长连接
def mysql_connection():
    global db
    try:
        db.ping()
    except:
        db = MySQLdb.connect("localhost", "root", "Abcd520025@", "58dh", charset='utf8')
    return db


cursor = mysql_connection().cursor()

EXPR_DONT_UNDERSTAND = '未匹配到关键词'


@on_command('reply')
async def reply(session: CommandSession):
    message = session.state.get('message').replace(' ', '')
    if message in ('h电话', 'h电脑', 'h网络'):
        table = '58_robot_1'
        reply = await database_search(session, table, message)
        des = ''
    else:
        table = '58_robot_2'
        reply = await database_search(session, table, message)
        des = "\n\n更对解决方案可以输入下列关键词：h电话,h电脑,h网络来获取更多帮助\n您也可以直接美式扫工位二维码或online在线提单来快速联系IT"
    msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(os.path.dirname(__file__)+'/'+'QQ_msg_log.txt', 'a') as qq:
        qq.write('{}{}{}'.format(msg_time + '\n', 'From:' + message, '\n' + 'To:' + reply + '\n'))
    # if reply == EXPR_DONT_UNDERSTAND:
    #     pass
    # else:
    #     await session.send(reply+'\n'+des)



@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(60.0, 'reply', args={'message': session.msg_text})


async def database_search(session: CommandSession, table,msg: str)-> Optional[str]:
    cursor.execute('select * from {} where keyword LIKE "{}";'.format(table, msg))
    a = cursor.fetchall()
    # print(a)
    if a != ():
        text = a[0][2]
        return text
    else:
        try:
            seg_list = jieba.cut(msg, cut_all=False)
            # print(jieba.lcut(msg, cut_all=False))
            t = True
            while t:
                cursor.execute('select * from {} where keyword LIKE "%{}%";'.format(table, next(seg_list)))
                a = cursor.fetchall()
                if a != ():
                    text = a[0][2]
                    t = False
            return text
        except StopIteration:
            text = EXPR_DONT_UNDERSTAND
            return text
        # return None





