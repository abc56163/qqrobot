from typing import Optional
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import os
import sys
import time
import jieba
sys.path.append('../')
from config import databases


base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# jieba.load_userdict(base_dir+'/dict.txt')
jieba.set_dictionary(base_dir+'/dict.txt')


# 保持mysql长连接
# db = MySQLdb.connect("localhost", "*********", "*********", "*********", charset='utf8')
#
#
# def mysql_connection(db):
#     try:
#         db.ping()
#     except:
#         db = MySQLdb.connect("localhost", "*********", "*********", "*********", charset='utf8')
#     return db


EXPR_DONT_UNDERSTAND = '未匹配到关键词'
supplement = "\n更多解决方案可以输入下列关键词:电话问题,电脑问题,网络问题来获取更多帮助!\n您也可以直接美式扫工位二维码或online在线提单来快速联系IT!"
cursor = databases().cursor()
db = databases()


@on_command('reply')
async def reply(session: CommandSession):
    message = session.state.get('message').replace(' ', '')
    if message in ('电话问题', '电脑问题', '网络问题'):
        table = '58_robot_1'
        answer = await database_search(session, table, message)
    elif 'add-' in message:
        key = message.split('-')[1]
        if key != '':
            with open(base_dir+'/dict.txt', 'a') as k:
                k.write(key + ' ' + '10' + '\n')
            jieba.add_word(key)
            answer = '关键词已经激活'
        else:
            answer = '请按照此格式激活:add-关键词'
    elif 'del-' in message:
        dict_txt = []
        key = message.split('-')[1]
        if key != '':
            fp = open(base_dir+'/dict.txt', 'r')
            txt = fp.readlines()
            for i in txt:
                if key in i:
                    jieba.del_word(key)
                else:
                    dict_txt.append(i)
            fp.close()

            with open(base_dir+'/dict.txt', 'w+') as fp:
                for i in dict_txt:
                    fp.write(i)
            answer = '关键词已经删除'
        else:
            answer = '请按照此格式删除:del-关键词'
    else:
        table = '58_robot_2'
        des = supplement
        answer = await database_search(session, table, message) + '\n'+des

    if EXPR_DONT_UNDERSTAND not in answer:
        print(answer)
        await session.send(answer)
        msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 聊天记录写入数据库

        try:
            cursor.execute('insert into 58_robot_3 (im, time, question, answer) values ("QQ", "{}", "{}", "{}")'
                           .format(msg_time, message, answer))
            db.commit()
        except:
            db.rollback()

    # 聊天记录写入文件
    # with open(os.path.dirname(__file__)+'/'+'QQ_msg_log1.txt', 'a') as qq:
    #     qq.write('{}{}{}'.format(msg_time + '\n', 'From:' + message, '\n' + 'To:' + reply + '\n'))


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(60.0, 'reply', args={'message': session.msg_text})


async def database_search(session: CommandSession, table,msg: str)-> Optional[str]:
    cursor.execute('select * from {} where keyword LIKE "{}";'.format(table, msg))
    a = cursor.fetchone()
    if a is not None:
        text = a[2]
        return text
    else:
        dict_list = []
        for x in jieba.lcut(msg, cut_all=False, HMM=False):
            dict_list.append(x)
        print(dict_list)
        num_list = [len(o) for o in dict_list]
        if max(num_list, default=0) in [0, 1]:
            a = None
        else:
            seg = dict_list[num_list.index(max(num_list))]
            cursor.execute('select * from {} where keyword LIKE "{}";'.format(table, seg))
            a = cursor.fetchone()
        print(a)
        if a is not None:
            text = a[2]
            return text
        else:
            text = EXPR_DONT_UNDERSTAND
            return text

        # try:
        #
        #     seg_list = jieba.cut(msg, cut_all=False, HMM=False)
        #     print(jieba.lcut(msg, cut_all=False))
        #     t = True
        #     while t:
        #         cursor.execute('select * from {} where keyword LIKE "{}";'.format(table, next(seg_list)))
        #         a = cursor.fetchone()
        #         print(a)
        #         if a is not None:
        #             text = a[2]
        #             t = False
        #     return text
        # except StopIteration:
        #     text = EXPR_DONT_UNDERSTAND
        #     return text

