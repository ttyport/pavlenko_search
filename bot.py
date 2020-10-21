from aiogram import Bot, Dispatcher, executor, types
from googleapiclient.discovery import build
from datetime import datetime

API_TOKEN = "token"
youtube = build('youtube', 'v3', developerKey=API_TOKEN)

bot = Bot(token="token")
bot_dispatcher = Dispatcher(bot)

last_update = None
videos = {}


@bot_dispatcher.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, напиши мне пару слов из названия видео, а я отправлю тебе ссылку на него.")


@bot_dispatcher.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply("Привет, напиши мне пару слов из названия видео, а я отправлю тебе ссылку на него.\n"
                        "Использование:\n"
                        "/search <то, что хотите найти>\n"
                        "@Zhoprozhag - админ")


@bot_dispatcher.message_handler(commands=['search'])
async def search(message: types.Message):
    try:
        global last_update

        if last_update is None:
            update_videos()

        since_update_str = str(datetime.now() - last_update)

        if int(since_update_str[:since_update_str.index(":")]) >= 1:
            update_videos()

        reply = search_engine(message.text)

        if reply != "empty":
            if len(reply) != 0 and reply != "empty":
                await message.reply(search_engine(message.text), parse_mode="MarkdownV2", disable_web_page_preview=True)
            else:
                await message.reply("К сожалению, ничего не нашлось...")
        else:
            await message.reply("Вы отправили пустое сообщение.")

    except Exception as e:
        await bot.send_message("473513901", shield(str(e)))
        await bot.send_message("391043684", shield(str(e)))
        print(e)
        await message.reply(f"У нас что-то сломалось, попробуйте позже.\nP.S. я уже пнул админа)\nЕсли интересно, "
                            f"то ошибка - {shield(str(e))}")


def search_engine(text):
    if "/search" in text and "/search@pavlenko_search_bot" not in text:
        text = text[8:]
    elif "/search@pavlenko_search_bot" in text:
        text = text[28:]

    if len(text) > 0:
        str_to_return = str()
        for key in videos.keys():
            if text.lower() in key.lower():
                key1 = key

                for char in '!@#$%^&*()-=_+/?,.<>|:"№;':
                    if char in key:
                        key_list = key1.split(char)
                        key1 = f'\\{char}'.join(_ for _ in key_list)

                str_to_return = str_to_return + \
                    f"[{key1}]" + f"({videos[key]})" + "\n\n"
        return str_to_return
    return "empty"


def update_videos():
    global last_update, videos

    res = youtube.channels().list(id="UC_hvS-IJ_SY04Op14v3l4Lg",
                                  part='contentDetails').execute()

    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None
    new_videos = {}

    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='snippet',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        for i in range(len(res["items"])):
            video_id = res["items"][i]["snippet"]["resourceId"]["videoId"]
            video_name = res["items"][i]['snippet']['title']
            new_videos[video_name] = f"https://www.youtube.com/watch?v={video_id}"

        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    last_update = datetime.now()
    videos = new_videos

    return new_videos


def shield(text):
    for char in '!@#$%^&*()-=_+/?,.<>|:"№;':
        if char in text:
            key_list = text.split(char)
            text = f'\\{char}'.join(_ for _ in key_list)
    return text


if __name__ == "__main__":
    executor.start_polling(bot_dispatcher)
