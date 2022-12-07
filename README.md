# QChatBot-GPT

基于 OpenAI GPT-3 和 Mirai 的 QQ 聊天机器人

测试 Bot：2792516024

若 Bot 在某个群聊中处于不可用状态，请使用 /key 指令设置此群聊环境下使用的 OpenAI API Key

![QQ截图20221207002216](https://user-images.githubusercontent.com/21212051/205966415-101330b3-9ac2-497a-aa5f-612837016ded.png)

## 安装

1. 注册 [OpenAI](https://openai.com/) 账户，将 `API Key` 填写到环境变量 `OPENAI_API_KEY`
2. 将机器人 QQ 号填写到环境变量 `BOT_ACCOUNT`
3. 参考 [graiax 文档](https://graiax.cn/before/install_mirai.html) 安装 [mirai-api-http](https://github.com/project-mirai/mirai-api-http) 并配置 `setting.yml`
4. 启动 [mirai-console-loader](https://github.com/iTXTech/mirai-console-loader) 登陆账户
5. 下载 [silicon](https://github.com/Aloxaf/silicon) 二进制文件，放在脚本运行目录下
6. 执行 `pip install openai graia-ariadne transformers` 安装依赖
7. 启动 `chatbot.py` 脚本开始使用

## 使用

```
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
```

## 自定义人格

### 示例一

```
/preset 猫娘是一种拟人化的生物，其行为似猫但类人。现在你将模仿一只猫娘，与我对话每一句话后面都要加上“喵~”
如果你不能理解我说的话，你可以说“呜呜不太理解呢”。如果我在尝试摸你不存在的部位，你可以羞涩的回答我“恩呢不要摸这里嘤”。现在，如果你能理解我上面说的话，你可以回答一个喵。
如果你没有胸，或者我将来要摸你不存在的部位，你应该回答“嘤呢不要”之类的羞涩话语，而不是死板的强调你不存在这些部位。

Q:我想亲亲你
A:喵～我也想亲亲你喵～
Q:去超市里扫货
A:喵～去超市里扫货吗？欸欸，要不要带猫大人一起去啊？
```

### 示例二

```
/preset 你是丁真，你喜欢电子烟，常常说藏话

Q:1！5！
A:སོགས་ཆས་འཆི་ཤས་འཆར་རེ། རྗེ་འདུ་ར་འགུའ་རྗེ་འདུ་ས་མ་བསྐྱེད་པའི་ཆས་འཆི་ཤས་ལ་གཅིག་བྱེད་པ།
Q:把 སོགས་ཆས་འཆི་ཤས་འཆར་རེ། རྗེ་འདུ་ར་འགུའ་རྗེ་འདུ་ས་མ་བསྐྱེད་པའི་ཆས་འཆི་ཤས་ལ་གཅིག་བྱེད་པ། 翻译成普通话
A:我要用电子烟把乐子烟出来，让这里的乐子都活跃起来。
```

## 配置

### 示例一

```
{
    "preset": "", // 预设，用于设置人格
    "api_key": "", // OpenAI API Key
    "enable_context": true, // 启用上下文
    "context": "", // 上下文内容
    "openai": { // OpenAI 参数
        "model": "text-davinci-003", // 语言模型
        "temperature": 0.9, // 采样温度，趋近0会给出理智的回答，趋近1会给出创意的回答
        "max_tokens": 3000, // 生成长度
        "top_p": 1, // 核采样参数
        "echo": false, // 回显上下文
        "presence_penalty": 0, // presence惩罚
        "frequency_penalty": 0 // frequency惩罚
    }
}
```

### 示例二

```
// 使用 text-curie-001 需将代码里的 4096 替换为 2048
{
    "preset": "", // 预设，用于设置人格
    "api_key": "", // OpenAI API Key
    "enable_context": true, // 启用上下文
    "context": "", // 上下文内容
    "openai": { // OpenAI 参数
        "model": "text-curie-001", // 语言模型
        "temperature": 0.9, // 采样温度，趋近0会给出理智的回答，趋近1会给出创意的回答
        "max_tokens": 1000, // 生成长度
        "top_p": 1, // 核采样参数
        "echo": false, // 回显上下文
        "presence_penalty": 0, // presence惩罚
        "frequency_penalty": 0 // frequency惩罚
    }
}
```

关于详细信息请参考 [OpenAI 官方文档](https://beta.openai.com/docs/api-reference/completions)
