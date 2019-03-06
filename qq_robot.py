from os import path
import nonebot
import config


print(path.join(path.dirname(__file__),'plugings'))
if __name__ == '__main__':
    nonebot.init(config)
    # loading built-in plug-ins
    nonebot.load_builtin_plugins()
    # loading custom plug-ins
    nonebot.load_plugins(
        path.join(path.dirname(__file__),'plugins'),
        'plugins'
    )
    nonebot.run()

