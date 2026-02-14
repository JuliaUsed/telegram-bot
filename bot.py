import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("Please set TELEGRAM_TOKEN in Railway Variables")

# ------------------------
# БЛАГОДАРНОСТИ (без повторов)
# ------------------------
THANKS_ALL = [
    "Спасибо, что не зассал и написал 🥇",
    "Спасибо, что ты всегда пишешь/говоришь «я рядом», когда это нужно. Даже если я молчу или ушла в себя, ты всегда подходишь и говоришь это",
    "Спасибо, что ты слышишь меня и становишься моей точкой доверия",
    "Спасибо, что покупаешь в рандомный день голубику, dare, мою любимую водичку... Мелочь, а приятно!",
    "Спасибо за твой мозг и амбиции, благодаря твоим мыслям, мечтам и целям я чувствую общность и горжусь тем, что ты мой выбор, а я твой",
    "Спасибо, что показал мне какой еще может быть жизнь. Что подарил возможность строить ее заново в совершенно новой стране. Что сводил меня в столькие места, показал уже столько стран... Всего лишь за один год.... Ты крейзи",
    "Спасибо, что любишь меня, у тебя хороший вкус",
    "Спасибо, что кладешь носки в корзину (не всегда, но на 70% спасибо!)",
    "Спасибо, что думаешь о будущем. Твоя взрослоть - это очень секси",
    "Спасибо, что ты это ты, я люблю тебя",
    "Спасибо, что ты всегда остаешься собой. Верность себе важное качество, я ощущаю тебя как личность, которую иногда хочется убить, но в целом, жить можно",
    "Спасибо, что чавкаешь во сне, так мило жесть",
    "Спасибо за секс посреди ночи, это был спешл момент.... ахахахха",
    "Спасибо, что забираешь меня, если я прошу или сам предлагаешь подвезти, а еще, что всегда находишь момент заехать за кофе. Ты - чудо!",
    "Спасибо, что почти выкинул ковер",
    "Спасибо за то, что целуешь меня в татушки",
    "Спасибо за твою нежность и чувственность, обожаю твои руки",
]
thanks_bag = THANKS_ALL.copy()

def get_random_thanks(context: ContextTypes.DEFAULT_TYPE) -> str:
    global thanks_bag
    if not thanks_bag:
        thanks_bag = THANKS_ALL.copy()
    msg = random.choice(thanks_bag)
    thanks_bag.remove(msg)
    return msg

# ------------------------
# МОМЕНТЫ (рандом фото + подпись)
# ------------------------
moments = [
    {
        "photo": "AgACAgIAAxkBAAIBrmmQXFHpvSXiRxGTUmPDPEQkYibjAAL_FGsbQQiISGgwsBXsd-VeAQADAgADeQADOgQ",
        "caption": "2024 год, я проснулась от того, что какой-то парень в интернете заставил меня извиваться на постели и думать о нем с учащенным дыханием",
    },
    {
        "photo": "AgACAgIAAxkBAAIBsWmQXduqLI5X5oYYAAHtwnHFpQEYiQACBhVrG0EIiEgr1bLIn5m4OQEAAwIAA3kAAzoE",
        "caption": "День, когда я впервые поняла, что хочу сделать для тебя что-то особенное (живу с этим чувством по сей день), потому что твои чистые реакции - моя самая большая любовь! Чувстовала тогда себя просто суперхиро",
    },
    {
        "photo": "AgACAgIAAxkBAAIBs2mQXngHNKEOMz_JWx9n397hj6DLAAIMFWsbQQiISMeXyzVmVrKsAQADAgADeQADOgQ",
        "caption": "Дада, не удивляйтесь, это 2024, дело идет к новому году и я верю в чудо и что ты просто хитрец. В этом кружочке ты сказал вот эту иконическую фразу \"я хочу проговорить пару моментов\" и реально проговорил))) сказал, что прилететь к новому году не выйдет. Но я сохрнаила кружок и иногда пролистывала, пытаясь понять, есть ли такое место в Иркутске....",
    },
    {
        "photo": "AgACAgIAAxkBAAIBtWmQXyN3E3BHVBfNxut9o3iZbR47AAIOFWsbQQiISNbTP0CZOuZkAQADAgADeQADOgQ",
        "caption": "Мы с тобой лежим на берегу океана в классном бичклабике, где проведем день и будем в шоке от времени, которое нужно преодолеть и до и после посещения))) я просто фоткала тебя каждый момент, и подумала как тебе идет загар океан и вся эта легкость, все ще осознавая, что ты рядом",
    },
    {
        "photo": "AgACAgIAAxkBAAIBt2mQX8PgNebEAsC_3psUsrHYCuwQAAIVFWsbQQiISFBI3F2mSCpsAQADAgADeQADOgQ",
        "caption": "Ну это я просто не могу не добавить))) делаем ТВОЕ ПЕРВОЕ тату! Я беспокоюсь нормально ли они тебя забьют, а то был красивый мальчиу... ну и хочу тебя все больше",
    },
    {
        "photo": "AgACAgIAAxkBAAIBuWmQYD2N15a2eLGine79VC10tmnNAAIWFWsbQQiISN188Up3U3jzAQADAgADeQADOgQ",
        "caption": "Смотрю на тебя и думаю, хоть бы это не фейк хоть бы это не фейк, уже скучаю, ну и конечно ты без расшифровки уже поняла, что это мы прощаемся с тобой в аэропорту)",
    },
    {
        "photo": "AgACAgIAAxkBAAIBu2mQYTRqTx1is5hyUMd_BGj586b7AAIeFWsbQQiISA5hQ_--W38XAQADAgADeQADOgQ",
        "caption": "Ты прилетаешь ко мне в Иркутск, выглядишь как икона, мой брат думает, что ты маньяк, моя мама переживает о том, что ты будешь кушать... А я... а я в ахуе, ведь понимаю, что больше не хочу смотреть на тебя через экран...",
    },
    {
        "photo": "AgACAgIAAxkBAAIBvWmQYZMPhyVhkERDkm-XLs79FIFEAAIhFWsbQQiISL1ry_Pe2dgYAQADAgADeQADOgQ",
        "caption": "Везешь меня в свой гэнгста сити с советским вайбом и добрыми людьми... я в ахуе, но доверяю тебе",
    },
    {
        "photo": "AgACAgIAAxkBAAIBwWmQYh8HVUDv92v5uWS_TAeNG8otAAIqFWsbQQiISE-UkCBj35QGAQADAgADeQADOgQ",
        "caption": "Пока мама на работе, зять балуется",
    },
    {
        "photo": "AgACAgIAAxkBAAIBw2mQYpfH13kAAQx-LvYhY2Uv3c2b-gACMBVrG0EIiEiJKkFpHQwjhwEAAwIAA3kAAzoE",
        "caption": "Мартовские котики в шоке друг с друга, начинают знакомиться друг с другом в другом формате))) был весело (местами нет) но весь путь этого стоил, да? 🔫",
    },
    {
        "photo": "AgACAgIAAxkBAAIBxWmQY5HdpUcqFG4_ReZgqJ1H2tH0AAJEFWsbQQiISEFn8dXQrw6WAQADAgADeQADOgQ",
        "caption": "Балуюсь у тебя дома, пока ты на работе…",
    },
    {
        "photo": "AgACAgIAAxkBAAIBx2mQY83ypc8uCY5UrrHzXLqvmycCAAJHFWsbQQiISKIEM5f60kQYAQADAgADeQADOgQ",
        "caption": "Тоже март 2025, первое домашнее насилие",
    },
    {
        "photo": "AgACAgIAAxkBAAIByWmQZE0Jm_66ix6yV2uCawzDIa5rAAJLFWsbQQiISOAj6PYQeCUzAQADAgADeQADOgQ",
        "caption": "В новисадике в первый раз, пошли в красивый ресторан, зашли в местные сувенирки, посмеялись с отеля Пупина, попили кофе конечно же и погрешили в церквях",
    },
    {
        "photo": "AgACAgIAAxkBAAIBy2mQZPXr-V3UNvMx0aib6SYHFI2CAAJOFWsbQQiISJUwHX1VtLyuAQADAgADeQADOgQ",
        "caption": "Вы где? Мы в САРАЕВО ЕДЕМ 👩🏻‍❤️‍👨🏼 Это снова апрель 2025, и ты устраиваешь мне вот такие вот экспресс экскурсии и я рефлексирую о том, как же мне нравится смотреть на места где ты уже был и разделять эмоции",
    },
    {
        "photo": "AgACAgIAAxkBAAIBzWmQZW_5bjrPcC8zQ_AhJGSIKrFQAAJRFWsbQQiISEOTAS27B20EAQADAgADeQADOgQ",
        "caption": "Это апрель 2025, Валера тоже хочет со мной познакомиться…",
    },
    {
        "photo": "AgACAgIAAxkBAAIBz2mQZa85nE04dJa9Sc3cEhESpUZ1AAJTFWsbQQiISElaHez2gagnAQADAgADeQADOgQ",
        "caption": "Майские БЕЗбашенные путешествия)) рассматриваем владения с высоты авалы и примечаем красивый домик, на который ты положил глаз))) было классно!",
    },
    {
        "photo": "AgACAgIAAxkBAAIB0WmQZibgc8K1U7iPQFlkCz3kcGa0AAJWFWsbQQiISDegwijTaYHFAQADAgADeQADOgQ",
        "caption": "Снова тусуемся у какой-то заброшки в мае 2025",
    },
    {
        "photo": "AgACAgIAAxkBAAIB02mQZmlcMF6EHfPSR64JswABk-nu3AACWhVrG0EIiEiXQfi_GGstzQEAAwIAA3kAAzoE",
        "caption": "Дорогой дневник, почему у меня нет ни одной нормальной фотки с яхтинга… да 🙂‍↕️ ну зато было реально круто и совершенно ново! Это май 2025 года. И да, тебе очень идет быть капитаном…",
    },
    {
        "photo": "AgACAgIAAxkBAAIB1WmQZspYTAwNzAfI5ubuJzkyn77YAAJbFWsbQQiISJKcI1YwvypiAQADAgADeQADOgQ",
        "caption": "В июне совершаем в основном такие прогулочно-кофейные движения, сходили почитали в парке, радуемся солнышку но хотим на Баличку! Планируем Черногорию 🙂‍↕️",
    },
    {
        "photo": "AgACAgIAAxkBAAIB12mQZzEclneapSfp_LamV31phw-JAAJdFWsbQQiISDxdm8ctsRnvAQADAgADeQADOgQ",
        "caption": "В июле 2025 мы едем на ЕХИТ! Я узнала что всю жизнь произносила это слово не правильно, я клянусь, я не знала что реально правильно говорить экзит… страшно прикольно проводим время, устаем, но кайфуем",
    },
    {
        "photo": "AgACAgIAAxkBAAIB2WmQZ3-yLyWDa1onS6-aK2Ru9vE7AAJjFWsbQQiISOrYIdAa36wGAQADAgADeQADOgQ",
        "caption": "Еще одни движения 2025 года в июле ха-ха-ха, прости пожалуйста, но я почему то просто не могу с этого фото, пусть будет",
    },
    {
        "photo": "AgACAgIAAxkBAAIB22mQZ8CEllhch7NptXpTOtmi6p2xAAJpFWsbQQiISPYF3HGtyivfAQADAgADeQADOgQ",
        "caption": "Путешествуем по Черногории, этот момент сильно запомнился) было так клево съесть пиццу на дорожку, на берегу океана) так спонтанно. Люблю нас за такие классные моменты, которые можно создать в моменте",
    },
    {
        "photo": "AgACAgIAAxkBAAIB3WmQaBejMyxZNlZF1X8FLAABpi9EiQACbRVrG0EIiEgLHKPtnKOLjQEAAwIAA3kAAzoE",
        "caption": "Посещаем потрясающе красиво жабляк! Уставшие, еще даже не знаем какая крутая дорога будет впереди…",
    },
    {
        "photo": "AgACAgIAAxkBAAIB32mQaGKcHqU6y1pEiNHEWwpVgdPTAAJuFWsbQQiISOV0Rn6XZ4JrAQADAgADeQADOgQ",
        "caption": "Посещаем ну очень красивый макдональдс в субботтце! Было классно, я была в шоке) да и Субботица приятный город. Люблю с тобой такие поездки",
    },
    {
        "photo": "AgACAgIAAxkBAAIB4WmQaLd9YAY0kq6fFort7_2-xIq0AAJ1FWsbQQiISAi_KG52gHWEAQADAgADeQADOgQ",
        "caption": "Съездили на космайчик с твоими друзьями, которые стали нашими))) Как же там было красиво, я все мечтаю снова там оказаться но в туманный день, делаем???",
    },
    {
        "photo": "AgACAgIAAxkBAAIB42mQaRJmTNdkHGqzKUolx2Fe408vAAKAFWsbQQiISLQNirqgZlLoAQADAgADeQADOgQ",
        "caption": "Приезжаем в Ульцин… остаемся там ненадолго ахпха, осознаем себя как любители тусовочный шуршащих движений хотя бы вокруг. Но по дороге до любимой виллочки, заезжаем снова на заброшку и застаем вот такой красивущий закат",
    },
    {
        "photo": "AgACAgIAAxkBAAIB5WmQbB_FqxkeObLQdJYWJk9wUiivAAKfFWsbQQiISC2GmQZC3tTBAQADAgADeQADOgQ",
        "caption": "Пожалуй лучшее фото октября 2025 года, такая бьюти рутинка, обожаю когда ты такой довольный",
    },
    {
        "photo": "AgACAgIAAxkBAAIB52mQbFK2HmdNXFo_11GMiLvOLz63AAKiFWsbQQiISBa0iAExEcBiAQADAgADeQADOgQ",
        "caption": "Пребываю в шоке от того что ты наделал на мой др в сентябре… довез такую красоту, так постарался, а очки???? Сам факт твоих вложений и что ты так можешь слышать, я очень благодарна тебя за момент абсолютного счастья от таких вещей! Чувствую себя на этом фото нереально любимой",
    },
    {
        "photo": "AgACAgIAAxkBAAIB6WmQcljvX24BIFH2vaxmiB546hvOAALMFWsbQQiISKyacgMrFEdeAQADAgADeQADOgQ",
        "caption": "Lovим солнечные деньки ноября, готовимся к режиму сдохни или заработай на Бали! Долгие прогулки по выходным это моя конечно уже любимая рутинка, теплые дни с тобой на подсознании ощущаются по особенному",
    },
    {
        "photo": "AgACAgIAAxkBAAIB62mQdsJC0e-f7ObreOK7qroFFGxlAALuFWsbQQiISJ5RSqNUjIZfAQADAgADeQADOgQ",
        "caption": "Ох уж этот момент твоей голой готовки))) поймала как-то, в итоге снимала две минуты 👀",
    },
    {
        "photo": "AgACAgIAAxkBAAIB7WmQdw1zwBNgH2zh21FJZ1HVamaCAALwFWsbQQiISF9avU3wZkpQAQADAgADeQADOgQ",
        "caption": "Наш уже типичный airport side eye 😒 но перелет реально был пиздец! Зато дальше декабрь был вкусный и Балийский! Рада что мы пережили это 😅",
    },
    {
        "photo": "AgACAgIAAxkBAAIB72mQd30xj_dqCIkEFttoJ-Ki5mGTAAL0FWsbQQiISNF31MVmofHjAQADAgADeQADOgQ",
        "caption": "Стил секси, снова на Бали) уже как пара и учились вместе проводить отдых более расслабленно) сделали кучу всего, о чем нам сказали окружающие. А сами в шоке что так можно",
    },
    {
        "photo": "AgACAgIAAxkBAAIB8WmQd86Jbzt7XBbvgx7y8yDQAjQwAAL3FWsbQQiISPrmp052uCLMAQADAgADeQADOgQ",
        "caption": "Видео с этого места конечно круче))) но я считаю такие совместные фото есть далекоооо не у всех. По настоящему особенный экспириенс, который кладем в копмлочку нашей лав стори",
    },
    {
        "photo": "AgACAgIAAxkBAAIB82mQeBV-JfyMx4WdGW54QbscrDgYAAL6FWsbQQiISNell17xJON1AQADAgADeQADOgQ",
        "caption": "Просто день когда я чувствовал себя плохо, а ты был рядом и это правда бесценно. Заставил меня забыть о вине и ощущать только тепло и безопасность))) Как говорится лучше болеть на Бали, чем работать в Сербии",
    },
    {
        "photo": "AgACAgIAAxkBAAIB9WmQeE7M1E8l6sV4vzW147QUsE6AAAL9FWsbQQiISHVmWDqIB-EQAQADAgADeQADOgQ",
        "caption": "Снова целуемся у океана, сколько таких поцелуев было? Явно можно больше",
    },
]

# ------------------------
# ТЕКСТ "МОЕМУ МАЦО"
# ------------------------
MACO_TEXT = (
    "Этот год с тобой я запомню как бесконечную любовную сцену с разными моментами. "
    "Но я ощущаю какое это настоящее чувство. Моментов на самом деле было очень много. "
    "Просто до чертиков, вся моя галерея просто кишит днями, о которых есть что рассказать: "
    "будь это обычный день дома или поездка в другую часть света.\n\n"
    "Если представить что наши отношения это карта, то точек за этот год получилось очень много. "
    "Особенно эмоций, особенных эмоций.\n\n"
    "Ты мое богатство, моя поддержка, мой человек. Моя сила, мое любопытство! "
    "Мне нравится узнавать тебя разного и также нравится, что еще много я о тебе не знаю, "
    "а что-то не узнаю никогда) в этом прелесть нашего союза, двух стремящихся и растущих людей. "
    "Я вижу как ты старателен, я горжусь тобой и быть рядом с тобой мой выбор, пожалуй самый правильный. "
    "Спасибо тебе за тебя. Спасибо тебе за нас\n\n"
    "Я тебя люблю, Ю."
)

# ------------------------
# UI
# ------------------------
def kb_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Will you be my Valentine? 💘", callback_data="valentine")]]
    )

def kb_yesno() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Да 💗", callback_data="yes"),
          InlineKeyboardButton("Нет 😏", callback_data="no")]]
    )

def kb_no() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("извиняюсь, бес попутал", callback_data="back")]]
    )

def kb_yes_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Получить благодарность 💌", callback_data="thanks")],
            [InlineKeyboardButton("Вспомнить момент нашей стори 📸", callback_data="moment")],
            [InlineKeyboardButton("моему Мацо 💘", callback_data="maco")],
        ]
    )

# ------------------------
# Handlers
# ------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Ответь честно 😉", reply_markup=kb_start())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "valentine":
        await query.edit_message_text("Точно подумай...", reply_markup=kb_yesno())
        return

    if data == "no":
        await query.edit_message_text("Неверный ответ. НЕ БАЛУЙСЯ!", reply_markup=kb_no())
        return

    if data == "back":
        await query.edit_message_text("Подумай еще раз 😉", reply_markup=kb_yesno())
        return

    if data == "yes":
        await query.edit_message_text("Вот что тебя ждет:", reply_markup=kb_yes_menu())
        return

    if data == "thanks":
        used = context.user_data.get("used_thanks", [])
        available = [t for t in THANKS_ALL if t not in used]
        if not available:
            used = []
            available = THANKS_ALL
        msg = random.choice(available)
        used.append(msg)
        context.user_data["used_thanks"] = used
        await query.message.reply_text(msg)
        return

    if data == "moment":
        moment = random.choice(moments)
        await query.message.reply_photo(photo=moment["photo"], caption=moment["caption"])
        return

    if data == "maco":
        await query.message.reply_text(MACO_TEXT)
        return

# ------------------------
# MAIN
# ------------------------
def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
