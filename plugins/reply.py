from typing import Optional
from nonebot import on_command, CommandSession, on_notice
from nonebot import on_natural_language, NLPSession, IntentCommand
import os
import time
import jieba
jieba.load_userdict(os.path.dirname(__file__)+'/dict.txt')
import MySQLdb
db = MySQLdb.connect("localhost", "root", "Abcd520025@", "study", charset='utf8')
cursor = db.cursor()

EXPR_DONT_UNDERSTAND = '您说什么我不明白！您可以美事扫工位二维码提单哦！'

@on_command('reply')
async def reply(session: CommandSession):
    message = session.state.get('message')
    reply = await database_search(session, message)
    msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(os.path.dirname(__file__)+'/'+'QQ_msg_log.txt', 'a') as qq:
        qq.write('{}{}{}'.format(msg_time + '\n', 'From:' + message, '\n' + 'To:' + reply + '\n'))
    if reply == EXPR_DONT_UNDERSTAND:
        pass
    else:
        await session.send(reply)


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(60.0, 'reply', args={'message': session.msg_text})


async def database_search(session: CommandSession, msg: str)-> Optional[str]:
    try:
        cursor.execute('select * from robot where keyword LIKE "%s"' % msg)
        a = cursor.fetchall()
        text = a[0][2]
        return text
    except:
        try:
            seg_list = jieba.cut(msg, cut_all=True)
            t = True
            while t:
                cursor.execute('select * from robot where keyword LIKE "%{}%"'.format(next(seg_list)))
                a = cursor.fetchall()
                if a != ():
                    text = a[0][2]
                    t = False
            return text
        except:
            text = EXPR_DONT_UNDERSTAND
            return text
        # return None





