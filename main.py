from datetime import datetime, timedelta
from PIL import Image

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from conf import TOKEN, DB_NAME
from db_helper import DBHelper


STATE_REGION = 1
STATE_CALENDAR = 2

user_region = dict()
db = DBHelper(DB_NAME)


BTN_TODAY, BTN_TOMORROW, BTN_MONTH, BTN_REGION, BTN_DUA, RESTART = '⏳ Bugun', '🕰 Ertaga', '📆 To`liq taqvim', '🇺🇿 Mintaqa tanlash', '🤲 Ruzadagi Duolar', '🔄 Yangilash'

main_buttons = ReplyKeyboardMarkup([
    [BTN_TODAY], [BTN_TOMORROW, BTN_MONTH], [BTN_DUA], [RESTART]
], resize_keyboard=True)


def region_button():
    regions = db.get_regions()
    buttons = []
    tmp_b = []
    for region in regions:
        tmp_b.append(InlineKeyboardButton(region['region'], callback_data=region['id']))
        if len(tmp_b) == 2:
            buttons.append(tmp_b)
            tmp_b = []
    return buttons


def start(update, context):
    user = update.message.from_user
    user_region[user.id] = None
    buttons = region_button()

    update.message.reply_html(
        f'Assalomu Alaykum, <b>{user.first_name}!</b>\n\nRamazon oyi muborak bo`lsin!\n\nMintaqani tanlang!',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return STATE_REGION


def inline_callback(update, context):
    try:
        query = update.callback_query
        user_id = query.from_user.id
        user_region[user_id] = int(query.data)
        query.message.delete()
        query.message.reply_html(
            text='<b>Ramazon taqvimi 2022🌙1443 </b>\n\nQuidagilardan birini tanlang!👇',
            reply_markup=main_buttons
        )
        return STATE_CALENDAR
    except Exception as e:
        print('Error: ', e)


def calendar_today(update, context):
    try:
        user_id = update.message.from_user.id
        if not user_region[user_id]:
            return STATE_REGION
        region_id = user_region[user_id]
        region = db.get_region(region_id)
        today = str(datetime.now().date())
        if db.get_calendar(today):
            calendar = db.get_calendar(today)
            time_str = str(calendar['saharlik'])
            time_str2 = str(calendar['iftorlik'])
            date_format = '%H:%M'
            given_time = datetime.strptime(time_str, date_format)
            given_time2 = datetime.strptime(time_str2, date_format)
            inter = int(region['interval'])
            if str(region['interval']) in '-':
                final_time = given_time - timedelta(minutes=inter)
                final_time2 = given_time2 - timedelta(minutes=inter)
            else:
                final_time = given_time + timedelta(minutes=inter)
                final_time2 = given_time2 + timedelta(minutes=inter)

            final_time_str = final_time.strftime('%H:%M')
            final_time_str2 = final_time2.strftime('%H:%M')
            message = f"✨Ramazon taqvimi🌙\n\n{today} kungi <b>{region['region']}</b> hududi uchun\n\n\nSaharlik:\t  <b>{final_time_str}</b>\n\nIftorlik:\t   <b>{final_time_str2}</b>\n\n\n||@ramazon_taqvimi_ruza_bot||"
            update.message.reply_text(message, parse_mode='HTML', reply_markup=main_buttons)
        else:
            message = f"✨Ramazon taqvimi🌙\n\nBugungi sana <b>{today}</b>\n\n\n🙃Hozir Ramazon oyi emas🙃\nTaqvimni to`liq olishingiz mumkin!\n\n\n||@ramazon_taqvimi_ruza_bot||"
            update.message.reply_text(message, parse_mode='HTML', reply_markup=main_buttons)
    except Exception as e:
        print('Calendar today function error: ', str(e))


def calendar_tomorow(update, context):
    try:
        user_id = update.message.from_user.id
        if not user_region[user_id]:
            return STATE_REGION
        region_id = user_region[user_id]
        region = db.get_region(region_id)
        today = str(datetime.now().date() + timedelta(days=1))
        if db.get_calendar(today):
            calendar = db.get_calendar(today)
            time_str = str(calendar['saharlik'])
            time_str2 = str(calendar['iftorlik'])
            date_format = '%H:%M'
            given_time = datetime.strptime(time_str, date_format)
            given_time2 = datetime.strptime(time_str2, date_format)
            inter = int(region['interval'])
            if str(region['interval']) in '-':
                final_time = given_time - timedelta(minutes=inter)
                final_time2 = given_time2 - timedelta(minutes=inter)
            else:
                final_time = given_time + timedelta(minutes=inter)
                final_time2 = given_time2 + timedelta(minutes=inter)

            final_time_str = final_time.strftime('%H:%M')
            final_time_str2 = final_time2.strftime('%H:%M')

            message = f"✨Ramazon taqvimi🌙\n\n{today} kungi <b>{region['region']}</b> hududi uchun\n\n\nSaharlik:\t<b>{final_time_str}</b>\n\nIftorlik:\t  <b>{final_time_str2}</b>\n\n\n||@ramazon_taqvimi_ruza_bot||"
            update.message.reply_text(message, parse_mode='HTML', reply_markup=main_buttons)
        else:
            message = f"✨Ramazon taqvimi🌙\n\nErtangi sana <b>{today}</b>\n\n\n🙃Bu kun Ramazon oyi emas🙃\nTaqvimni to`liq olishingiz mumkin!\n\n\n||@ramazon_taqvimi_ruza_bot||"
            update.message.reply_text(message, parse_mode='HTML', reply_markup=main_buttons)
    except Exception as e:
        print('Calendar tomorrow function error: ', str(e))


def calendar_month(update, context):
    try:
        user_id = update.message.from_user.id
        if not user_region[user_id]:
            return STATE_REGION
        region_id = user_region[user_id]
        region = db.get_region(region_id)

        photo_url = f"taqvim/{region['id']}.jpg"
        message = f"✨Ramazon taqvimi🌙\n\n<b>{region['region']}</b> uchun taqvim 2022\n\n||@ramazon_taqvimi_ruza_bot||"

        update.message.reply_photo(open(photo_url, 'rb'), caption=message, parse_mode='HTML', reply_markup=main_buttons)

    except Exception as e:
        print('Calendar month function error: ', str(e))


def select_dua(update, context):
    try:
        photo_path = "taqvim/dua/dua.jpg"
        message = f"✨Ramazon taqvimi🌙\n\n<b> 🌞 saharlik va 🌚 iftorlik duolari 🤲</b>\n\n||@ramazon_taqvimi_ruza_bot||"

        update.message.reply_photo(open(photo_path, 'rb'), caption=message, parse_mode='HTML',
                                   reply_markup=main_buttons)

    except Exception as e:
        print('Select_dua function error: ', str(e))


def main():
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE_REGION: [
                CallbackQueryHandler(inline_callback),
                MessageHandler(Filters.regex('^(' + BTN_TODAY + ')$'), calendar_today),
                MessageHandler(Filters.regex('^(' + BTN_TOMORROW + ')$'), calendar_tomorow),
                MessageHandler(Filters.regex('^(' + BTN_MONTH + ')$'), calendar_month),
                MessageHandler(Filters.regex('^(' + BTN_DUA + ')$'), select_dua),
                MessageHandler(Filters.regex('^(' + RESTART + ')$'), start),
            ],
            STATE_CALENDAR: [
                MessageHandler(Filters.regex('^(' + BTN_TODAY + ')$'), calendar_today),
                MessageHandler(Filters.regex('^(' + BTN_TOMORROW + ')$'), calendar_tomorow),
                MessageHandler(Filters.regex('^(' + BTN_MONTH + ')$'), calendar_month),
                MessageHandler(Filters.regex('^(' + BTN_DUA + ')$'), select_dua),
                MessageHandler(Filters.regex('^(' + RESTART + ')$'), start),
            ],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
