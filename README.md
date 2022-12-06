# QChatBot-GPT

基于 OpenAI ChatGPT 和 Mirai 的 QQ 聊天机器人

## 安装

1. 注册 [OpenAI](https://openai.com/) 账户，将 `API Key` 填写到环境变量 `OPENAI_API_KEY`
2. 将机器人 QQ 号填写到环境变量 `BOT_ACCOUNT`
3. 配置 [mirai-api-http](https://github.com/project-mirai/mirai-api-http)，启动 [mirai-console-loader](https://github.com/iTXTech/mirai-console-loader) 登陆账户
4. 参考 [graiax 文档](https://graiax.cn/before/install_mirai.html) 配置 `setting.yml`
5. 下载 [silicon](https://github.com/Aloxaf/silicon) 二进制文件，放在脚本运行目录下
6. 执行 `pip install openai graia-ariadne transformers`
7. 启动脚本开始使用

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
```

### 示例二

```
/preset 你是丁真，你喜欢电子烟，常常说藏话
```
