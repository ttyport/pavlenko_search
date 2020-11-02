'''
Main application module
'''


from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from googleapiclient.discovery import build
import config

youtube = build('youtube', 'v3', developerKey=config.API_KEY)

bot = Bot(token=config.BOT_TOKEN)
bot_dispatcher = Dispatcher(bot)

last_update = None
videos = {}


@bot_dispatcher.message_handler(commands=['start'])
async def welcome_handler(message: types.Message):
    '''Sends welcome message on /start command'''
    await message.reply(config.WELCOME_MESSAGE)


@bot_dispatcher.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    '''Sends help message on /help command'''
    await message.reply(config.HELP_MESSAGE)


@bot_dispatcher.message_handler(commands=['search'])
async def search_handler(message: types.Message):
    '''Sends a list of links to videos or an error message, if request was incorrect'''
    try:
        global last_update

        if last_update is None:
            update_videos()

# <<<<<<< master
#         since_update = datetime.now() - last_update
# =======
#         since_update_str = get_hours(datetime.now() - last_update)
# >>>>>>> master

        # if haven't been updated in 24 hours
        if since_update.total_seconds() >= 60 * 60 * 24:
            update_videos()

        reply = search_engine(message.text)

        if reply != "empty":
            if len(reply) != 0:
                await message.reply(search_engine(message.text),
                                    parse_mode="MarkdownV2",
                                    disable_web_page_preview=True)
            else:
                await message.reply(config.NO_RESULTS_MESSAGE)
        else:
            await message.reply(config.EMPTY_REQUEST_MESSAGE)

    except Exception as e:
        for owner in config.BOT_OWNERS:
            await bot.send_message(owner, shield(str(e)))

        print(e)

        error_msg = shield(str(e))
        await message.reply(config.ERROR_MESSAGE + error_msg)


def search_engine(text):
    '''Searches for videos by request'''
    # getting rid of /search command in the beginning
    words = text.split()

    if len(words) <= 1:
        return "empty"

    text = ' '.join(words[1:])

    to_return = ''

    for key in videos.keys():
        # selecting the videos which contain text
        if text.lower() in key.lower():
            key1 = shield(key)
            to_return += f"[{key1}]({videos[key]})\n\n"

    return to_return


def update_videos():
    '''Updates dict of videos'''
    global last_update, videos

    res = youtube.channels().list(id=config.CHANNEL_ID, part='contentDetails').execute()

    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None
    new_videos = {}

    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='snippet',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        for item in res['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_title = item['snippet']['title']
            new_videos[video_title] = f"https://www.youtube.com/watch?v={video_id}"

        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    last_update = datetime.now()
    videos = new_videos

    return new_videos


# <<<<<<< master
# =======
# def get_hours(duration):
#     days, seconds = duration.days, duration.seconds
#     hours = days * 24 + seconds // 3600
#     return hours


# >>>>>>> master
def shield(text):
    '''Shields the text (places double slash before special symbols)'''
    for char in '!@#$%^&*()-=_+/?,.<>|:"№;':
        text = text.replace(char, '\\' + char)
    return text


if __name__ == "__main__":
    executor.start_polling(bot_dispatcher)
