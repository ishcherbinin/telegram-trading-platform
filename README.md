## Trading platform based on Telegram bot functionality

### 1. Description

This project is a trading platform based on Telegram bot functionality. The main goal of the project is to provide a platform for trading cryptocurrencies. The platform will allow users to buy and sell currencies using a Telegram bot. 

### 2. Features

The main features of the project are:
1. Ability to send orders for specified instruments (e.g. BTC/USD, ETH/USD, etc.)
2. Ability to cancel order
3. Ability to check current session on the instrument
4. Ability to request all order by user

The project is based on the following technologies:
1. Python
2. Telegram API (aiogram)
3. Docker

Text for the messages might be replaced in [text_storage.py](telegram_interface/text_storage.py) to what you need and language you use
By default all text are in English

### 3. Setting

To set up the project, you need to follow these steps:
1. Clone the repository
2. Create a bot in Telegram using @BotFather and copy API token
3. Create a .env file in the root directory and add the following line:

**NOTE: To get id of the chat, create chat with bot and use command /getid**
```
TELEGRAM_API_TOKEN is the token you got from @BotFather. 

MANAGERS_CHAT is the common chat ids of the chat where you want to receive notifications about the trades (it is managers who will be handling this process")
Example: MANAGERS_CHAT=-123456789

ALLOWED_IDS is chat ids as list for users are allowed to manage the bot and receive notification personally
Example: ALLOWED_IDS="['-123456789','-987654321']"

AVAILABLE_SYMBOLS is the list of available symbols for trading
Example: AVAILABLE_SYMBOLS="['RUB/USD','GEL/USD']"

REFPRICE_UPDATE_FREQUENCY=60 is the frequency of updating the reference price in seconds

REFERENCE_DATA_TABLES_PATH="./tables/" is the path to the folder where reference data tables are stored

```
4. Install requirements and python if it is needed
```
pip install -r requirements.txt
```

5. Running of the bot:

a. Docker way:
```
docker build -t bot-image .

docker run -d --name bot-container bot-image
```
b. Local way:
```
python run_bot.py
```

### 4. Usage

To use the bot, you need to follow these steps:
1. Create chat with bot
2. Use command /start or /help to start the bot
3. Use command /neworder to create new order
4. Use command /cancelorder to cancel order
5. Use command /currentsession to check current session on the instrument

**NOTE: Settlement of the trades are still on the managers of the application. SO it might require some time**

### 5. License

Apache License 2.0