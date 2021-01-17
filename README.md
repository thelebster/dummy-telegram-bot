# Dummy Telegram Bot

Built on top of [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

## Usage

Follow [instructions](https://core.telegram.org/bots#3-how-do-i-create-a-bot) to obtain a token, then paste token to `.env` file in form of `TELEGRAM_API_TOKEN=XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`.

```
docker-compose up -d --build
```

## Deploying on Heroku

1. Create an account on [Heroku](https://www.heroku.com/) and install [Heroku Cli](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).
2. Login in to your account by running the following command in terminal `heroku login`.
3. Create the Heroku application using the following command `heroku create appname`.
4. Set environment (config) variables.
```
heroku config:set TELEGRAM_API_TOKEN=XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
heroku config:set BOT_RUN_MODE=webhook
heroku config:set WEBHOOK_HOST=0.0.0.0
heroku config:set WEBHOOK_URL=https://appname.herokuapp.com/
```
5. Deploy changes to Heroku using the following command `git subtree push --prefix dummy_bot heroku master`.
