<div align="center"><strong>AmberAI 🤖</strong></div>
<div align="center">Simple Discord bot for generating pictures and text</div>

### Installation steps 🚩
**Step 1** 🎬 Git clone repository

```console 
git clone https://github.com/mkshustov/AmberAI.git
```

**Step 2** 📁 Changing directory to cloned directory

```😎
cd AmberAI
```

**Step 3** 💾 Install requirements

```console
pip install -r requirements.txt
```

**Step 4** 💻 Get information 

<a href="https://discord.com/developers" target="_blank">Discord token</a><br>

<a href="https://fusionbrain.ai/keys/" target="_blank">Sber keys</a><br>

<a href="https://mnnai.ru/" target="_blank">MNN data</a>

**Step 5** 😎 Customize bot

Open consts.py and fill it in 

```
Token="Your bot token"
SberKey = "Your Sber key"
SberSecretKey = "Your Sber secret key"
MNNKey="Your MNN key"
MNNId="Your MNN id"
ImageCommands=["create", "draw"] # Your commands for generating images
TextModel = "gpt-4o-mini" # Model for text generation
Activity = "Counter-Strike 2" # Bot activity
```

**Step 6** 🚀 Run the bot

```python
python bot.py
```
