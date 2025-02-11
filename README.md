## Trading platform based on Telegram bot functionality

### 1. Description

This project is a trading platform based on Telegram bot functionality. The main goal of the project is to provide a platform for trading cryptocurrencies. The platform will allow users to buy and sell currencies using a Telegram bot. 

### 2. Setting

To set up the project, you need to follow these steps:
1. Clone the repository
2. Create a bot in Telegram using @BotFather and copy API token
3. Create a .env file in the root directory and add the following line:
```
TELEGRAM_API_TOKEN is the token you got from @BotFather. 

MANAGERS_CHAT is the chat ids of the chat where you want to receive notifications about the trades (it is managers who will be handling this process")
Example: MESSAGES_CHAT=[-123456789]
```
4. Install requirements and python if it is needed
```
pip install -r requirements.txt
```

5. Running of the bot
a. Docker way:
```
docker build -t bot-image .

docker run -d --name bot-container bot-image
```
b. Local way:
```
python run_bot.py
```

