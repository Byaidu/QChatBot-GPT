import logging
import os
import openai
import asyncio
import json
import textwrap
import pickle
from copy import deepcopy
from functools import wraps, partial
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import config
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.event.mirai import NewFriendRequestEvent, BotInvitedJoinGroupRequestEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend
from graia.broadcast import Broadcast
from graia.ariadne.message.parser.base import *
from graia.ariadne.message.element import Image
from transformers import GPT2TokenizerFast

logging.basicConfig(level=logging.NOTSET)

default_api_key = os.getenv("OPENAI_API_KEY")

default_group_config = {
    'preset':'',
    'api_key':'',
    'enable_context':True,
    'context':'',
    'openai':{
        'model':'text-davinci-003',
        'temperature':0.9,
        'max_tokens':3000,
        'top_p':1,
        'echo': False,
        'presence_penalty':0,
        'frequency_penalty':0,
    }
}

bcc = create(Broadcast)
app = Ariadne(connection=config(int(os.getenv("BOT_ACCOUNT")),"GraiaxVerifyKey"))

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run

@async_wrap
def get_chat(prompt,group_config):
    try:
        if not group_config['api_key']:
            openai.api_key = default_api_key
        else:
            openai.api_key = group_config['api_key']
        resp = openai.Completion.create(**group_config['openai'],prompt=prompt)
        resp = resp['choices'][0]['text']
    except openai.OpenAIError as e:
        resp = str(e)
    return resp

def get_group_config(id):
    if not id in chat_config:
        chat_config[id] = deepcopy(default_group_config)
    return chat_config[id]

def save_chat_config():
    with open('chat_config.pkl','wb') as f:
        pickle.dump(chat_config,f)

def read_chat_config():
    try:
        with open('chat_config.pkl','rb') as f:
            resp = pickle.load(f)
        for k in resp:
            t = deepcopy(default_group_config)
            t.update(resp[k])
            resp[k] = t
    except IOError:
        resp = {}
    return resp

async def send_message_proxy(app: Ariadne, group: Union[Group, Friend], resp: MessageChain, quote: Union[bool, MessageChain]=False):
    msg = await app.send_message(group,resp,quote=quote)
    if msg.source.id < 0:
        txt = '\n'.join([textwrap.fill(i) for i in resp.display.splitlines()])
        with open('in.txt','wb') as f:
            f.write(txt.encode('utf-8'))
        os.system('silicon.exe in.txt -o out.png -f "微软雅黑" -l c --no-window-controls --background "#fff0" --pad-horiz 0 --pad-vert 0 --no-line-number --no-round-corner 2>nul')
        with open('out.png','rb') as f:
            pic = f.read()
        await app.send_message(group,MessageChain(Image(data_bytes=pic)),quote=quote)
    return

@bcc.receiver(GroupMessage)
async def chat(app: Ariadne, group: Group, event: MessageEvent, message: MessageChain = DetectPrefix("/chat")):
    prompt = message.display
    group_config = get_group_config(group.id)
    # 加载上下文
    if group_config['enable_context']:
        group_context = group_config['context']
    else:
        group_context = ''
    # 计算可发送的 token 数量
    token_limit = 4096 - group_config['openai']['max_tokens'] - len(tokenizer.encode(group_config["preset"])) - 3
    group_context = f'{group_context}Q:{prompt}\nA:'
    ids = tokenizer.encode(group_context)
    tokens = tokenizer.decode(ids[-token_limit:])
    # 计算可发送的字符数量
    char_limit = len(''.join(tokens))
    group_context = group_context[-char_limit:]
    # 从最早的提问开始截取
    pos = group_context.find('Q:')
    group_context = group_context[pos:]
    # 加载预设
    query = f'{group_config["preset"]}\n\n{group_context}'
    print(f'>>>{query}')
    resp = await get_chat(query,group_config)
    resp = resp.strip()
    # 更新上下文
    if group_config['enable_context']:
        group_config['context'] = f'{group_context}{resp}\n\n'
    else:
        group_config['context'] = ''
    print(f'<<<{resp}')
    save_chat_config()
    await send_message_proxy(app,group,MessageChain(resp),event.source.id)

@bcc.receiver(GroupMessage)
async def clear(app: Ariadne, group: Group, message: MessageChain = DetectPrefix("/clear")):
    group_config = get_group_config(group.id)
    group_config['context'] = ''
    save_chat_config()
    await send_message_proxy(app,group,MessageChain('已重置对话'))

@bcc.receiver(GroupMessage)
async def get(app: Ariadne, group: Group, message: MessageChain = DetectPrefix("/get")):
    if message.display=='global':
        await send_message_proxy(app,group,MessageChain(json.dumps(chat_config,ensure_ascii=False)))
    else:
        group_config = get_group_config(group.id)
        await send_message_proxy(app,group,MessageChain(json.dumps(group_config,ensure_ascii=False)))

@bcc.receiver(GroupMessage)
async def set(app: Ariadne, group: Group, message: MessageChain = DetectPrefix("/set")):
    try:
        group_config = get_group_config(group.id)
        group_config.update(json.loads(message.display))
        save_chat_config()
        await send_message_proxy(app,group,MessageChain('已修改设置'))
    except json.decoder.JSONDecodeError as e:
        await send_message_proxy(app,group,MessageChain(str(e)))

@bcc.receiver(GroupMessage)
async def reset(app: Ariadne, group: Group, message: MessageChain = DetectPrefix("/reset")):
    chat_config[group.id] = deepcopy(default_group_config)
    save_chat_config()
    await send_message_proxy(app,group,MessageChain('已重置设置'))

@bcc.receiver(GroupMessage)
async def preset(app: Ariadne, group: Group, message: MessageChain = DetectPrefix("/preset")):
    group_config = get_group_config(group.id)
    group_config['preset'] = message.display
    group_config['context'] = ''
    save_chat_config()
    await send_message_proxy(app,group,MessageChain('已修改预设'))

@bcc.receiver(GroupMessage)
async def key(app: Ariadne, group: Group, message: MessageChain = DetectPrefix("/key")):
    group_config = get_group_config(group.id)
    group_config['api_key'] = message.display
    save_chat_config()
    await send_message_proxy(app,group,MessageChain('已设置 OpenAI API Key'))

@bcc.receiver(GroupMessage)
async def mem(app: Ariadne, group: Group, message: MessageChain = DetectPrefix("/mem")):
    group_config = get_group_config(group.id)
    group_config['openai']['max_tokens'] = 4096 - int(message.display)
    save_chat_config()
    await send_message_proxy(app,group,MessageChain('已设置记忆长度'))

@bcc.receiver(GroupMessage)
async def help(app: Ariadne, group: Group, message: MessageChain = DetectPrefix("/help")):
    await send_message_proxy(app,group,MessageChain('''\
QChatBot-GPT 指令列表

/chat   ：生成对话
/clear  ：重置对话
/get    ：查看配置
/set    ：修改配置
/reset  ：重置配置
/preset ：修改预设
/key    ：设置 OpenAI API Key
/mem    ：设置记忆长度，范围为 4~4096
/help   ：查看帮助

注：预设+记忆+回答 共同占用长度为 4096 tokens 的区域
'''))
    await send_message_proxy(app,group,MessageChain('配置参考：https://beta.openai.com/docs/api-reference/completions/create'))
    await send_message_proxy(app,group,MessageChain('项目地址：https://github.com/Byaidu/QChatBot-GPT'))

@bcc.receiver(BotInvitedJoinGroupRequestEvent)
async def help(app: Ariadne, event: BotInvitedJoinGroupRequestEvent):
    logging.info('BotInvitedJoinGroupRequestEvent')
    await event.accept()

@bcc.receiver(NewFriendRequestEvent)
async def help(app: Ariadne, event: NewFriendRequestEvent):
    logging.info('NewFriendRequestEvent')
    await event.accept()

@bcc.receiver(FriendMessage)
async def hello(app: Ariadne, friend: Friend, message: MessageChain):
    await send_message_proxy(app,friend,MessageChain('要添加 bot 到群聊中才能使用哦'))

chat_config = read_chat_config()

app.launch_blocking()
