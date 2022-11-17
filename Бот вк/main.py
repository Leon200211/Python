import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from parsing_mirea import *
from parsing_pogoda import *
from parsing_korona import *

class User():

    def __init__(self, id, mode, state):
        self.id = id
        self.mode = mode
        self.state = state


prepod_name = "none"

now = datetime.datetime.now()


vk_session = vk_api.VkApi(token = "")
vk = vk_session.get_api()
longpol = VkLongPoll(vk_session)


def get_but(text, color):
    return {
        "action": {
            "type": "text",
            #"payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }




start_keyboard = {
    "one_time" : False,
    "buttons" : [
        [get_but('начать', 'positive')]
    ]
}
start_keyboard = json.dumps(start_keyboard, ensure_ascii = False).encode('utf-8')
start_keyboard = str(start_keyboard.decode('utf-8'))

new_weather_keyboard = {
    "one_time" : False,
    "buttons" : [
        [get_but('сейчас', 'positive'), get_but('на сегодня', 'positive')],
        [get_but('на завтра', 'positive'), get_but('на 5 дней', 'positive')]
    ]
}
new_weather_keyboard = json.dumps(new_weather_keyboard, ensure_ascii = False).encode('utf-8')
new_weather_keyboard = str(new_weather_keyboard.decode('utf-8'))

raspisanie_1_keyboard = {
    "one_time" : False,
    "buttons" : [
        [get_but('на сегодня', 'positive'), get_but('на завтра', 'positive')],
        [get_but('на эту неделю', 'positive'), get_but('на следующую неделю', 'positive')],
        [get_but('какая неделя?', 'primary'), get_but('какая группа?', 'primary')]
    ]
}
raspisanie_1_keyboard = json.dumps(raspisanie_1_keyboard, ensure_ascii = False).encode('utf-8')
raspisanie_1_keyboard = str(raspisanie_1_keyboard.decode('utf-8'))

menu_keyboard = {
    "one_time" : False,
    "buttons" : [
        [get_but('расписание', 'positive'), get_but('погода', 'negative')],
    ]
}
menu_keyboard = json.dumps(menu_keyboard, ensure_ascii = False).encode('utf-8')
menu_keyboard = str(menu_keyboard.decode('utf-8'))

prepod_menu_keyboard = {
    "one_time" : False,
    "buttons" : [
        [get_but('на сегодня', 'positive'), get_but('на завтра', 'positive')],
        [get_but('на эту неделю', 'positive'), get_but('на следующую неделю', 'positive')]
    ]
}
prepod_menu_keyboard = json.dumps(prepod_menu_keyboard, ensure_ascii = False).encode('utf-8')
prepod_menu_keyboard = str(prepod_menu_keyboard.decode('utf-8'))





def create_prepod(group, vk_msg,when):
    print("create_prepod")
    print(vk_msg)
    mas_name_prepod, mas_prepod = parsing_prepod_2(group, vk_msg,when)
    mas_for_keyboard = []
    print(mas_name_prepod, mas_prepod)
    for i in range(len(mas_name_prepod)):
        mas_for_keyboard.append(get_but(mas_name_prepod[i], 'positive'))
    prepod_keyboard = {
        "one_time" : False,
        "buttons" : [
            mas_for_keyboard
        ]
    }
    prepod_keyboard = json.dumps(prepod_keyboard, ensure_ascii = False).encode('utf-8')
    prepod_keyboard = str(prepod_keyboard.decode('utf-8'))
    return mas_name_prepod, mas_prepod, prepod_keyboard





def sender(id, text, key):

    vk_session.method('messages.send', {'user_id' : id ,'message' : text, 'random_id' : 0, 'keyboard' : key})

def sender_2(id, attachments,text, key):
    attachment = ','.join(attachments)
    vk_session.method('messages.send', {'user_id' : id, 'attachment' :  attachment, 'message' : text, 'random_id' : 0, 'keyboard' : key})





users = []

def main():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if(event.to_me):
                print(users)
                id = event.user_id
                msg = event.text.lower()
                print(msg)
                if msg == 'начать':
                    flag1 = 0
                    for user in users:
                        if user.id == id:
                            print(123)
                            sender(id, "Привет, я умный бот, как я могу помочь тебе?\n "
                                       "Введи номер группы, чтобы я смог тебя запомнить\n "
                                       "напиши Бот чтобы получить распивание", menu_keyboard)
                            user.mode = 'start'
                            user.state = "menu"
                            flag1 = 1
                    if flag1 == 0:
                        users.append(User(id, 'start', 'menu'))
                        sender(id, "Привет, я умный бот, как я могу помочь тебе?\n "
                                   "Для получения расписания введи номер группы, чтобы я смог тебя запомнить\n"
                                    "Команды бота:\n "
                                   "Начать - для запуска бота\n"
                                   "Меню - переход в меню\n"
                                   "Погода - переход в раздел погоды\n"
                                   "Расписание - переход в раздел расписания\n"
                                   "Найти 'имя преподавателя' - показать расписание преподавателя\n"
                                   "Корона 'место' - информация о коронавирусе\n", menu_keyboard)



                for user in users:
                    if user.id == id:
                        global prepod_name
                        if msg.lower() == 'меню':
                            user.state = "menu"
                            sender(id, "переход в меню", menu_keyboard)
                        try :
                            if msg[4].lower()== '-' and msg[7].lower() and msg[5].lower().isdigit() and msg[8].lower().isdigit():
                                user.mode = msg.lower()
                                sender(id, "Я запомнил твою группу: "+user.mode, menu_keyboard)
                        except IndexError:
                            pass

                        if msg.lower() == "корона":
                            info_corona = corona_1()
                            upload = VkUpload(vk_session)
                            attachments = []
                            photo = upload.photo_messages(photos = "tessstttyyy.png")[0]
                            attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                            sender_2(id, attachments, info_corona, menu_keyboard)
                        if msg.lower().find("корона") != -1 and len(msg.lower())>6:
                            mg_from_vk = msg.lower()[7:]
                            print(mg_from_vk)
                            sender(id, corona_2(mg_from_vk), raspisanie_1_keyboard)

                        if msg.lower() == 'бот' or msg.lower()=="расписание":
                            user.state = "raspisanie"
                            sender(id, "выберите действие", raspisanie_1_keyboard)

                        if msg.lower() == "погода":
                            user.state = "pogoda"
                            sender(id, "выберите действие", new_weather_keyboard)

                        if msg.lower().find("найти") != -1:
                            sender(id, "ok", prepod_menu_keyboard)
                            prepod_name = msg.lower()
                            #prepod_name = re.sub("^\s+|\n|\r|\s+$","",msg.lower())
                            #prepod_name = prepod_name[6:]
                            user.state = "poisk"

                        if(user.state == "raspisanie"):
                            if (msg.lower() == 'на завтра' or msg.lower() == 'на сегодня' or msg.lower() == 'на следующую неделю' or msg.lower() == 'на эту неделю') and prepod_name == "none":
                                print(123)
                                info = save_from_www_and_parsing(user.mode, datetime.datetime.today().weekday(), msg.lower())
                                print(123)
                                sender(id, info, raspisanie_1_keyboard)
                            if msg.lower() =="какая неделя?":
                                fgh = datetime.date(2021, now.month, now.day).isocalendar()[1]
                                fgh -= 33
                                sender(id, str(fgh), raspisanie_1_keyboard)
                            if msg.lower() == "какая группа?":
                                sender(id, user.mode, raspisanie_1_keyboard)

                        if(user.state == "pogoda"):
                            if(msg.lower()=="сейчас"):
                                city_name = "moscow"
                                api_key = "81f8953f98dfe25ad251384300929c47"
                                url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

                                info_weather, weather_photo = weather(url, msg.lower())

                                upload = VkUpload(vk_session)
                                attachments = []
                                image = requests.get(weather_photo, stream = True)
                                photo = upload.photo_messages(photos = image.raw)[0]
                                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))

                                sender_2(id, attachments, info_weather, new_weather_keyboard)

                            if(msg.lower()=="на сегодня"):
                                city_name = "moscow"
                                api_key = "81f8953f98dfe25ad251384300929c47"
                                url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
                                info_weather = weather(url, msg.lower())

                                try:
                                    upload = VkUpload(vk_session)
                                    attachments = []
                                    photo = upload.photo_messages(photos = "image.png")[0]
                                    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                                    sender_2(id, attachments, info_weather, new_weather_keyboard)
                                except:
                                    sender(id, "что то пошло не так", menu_keyboard)

                            if(msg.lower()=="на завтра"):
                                city_name = "moscow"
                                api_key = "81f8953f98dfe25ad251384300929c47"
                                url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
                                info_weather = weather(url, msg.lower())

                                try:
                                    upload = VkUpload(vk_session)
                                    attachments = []
                                    photo = upload.photo_messages(photos = "image.png")[0]
                                    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                                    sender_2(id, attachments, info_weather, new_weather_keyboard)
                                except:
                                    sender(id, "что то пошло не так", menu_keyboard)

                            if(msg.lower()=="на 5 дней"):
                                city_name = "moscow"
                                api_key = "81f8953f98dfe25ad251384300929c47"
                                url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
                                info_weather = weather(url, msg.lower())

                                try:
                                    upload = VkUpload(vk_session)
                                    attachments = []
                                    photo = upload.photo_messages(photos = "image.png")[0]
                                    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                                    sender_2(id, attachments, info_weather, new_weather_keyboard)
                                except:
                                    sender(id, "что то пошло не так", menu_keyboard)


                        if user.state=="poisk":
                            info = ""
                            if((msg.lower() == 'на завтра' or msg.lower() == 'на сегодня' or msg.lower() == 'на следующую неделю' or msg.lower() == 'на эту неделю')):
                                #mas_name_prepod, mas_info_prepod = parsing_prepod_2(user.mode, prepod_name, msg.lower())
                                mas_name_prepod, mas_info_prepod, prepod_keyboard = create_prepod(user.mode, prepod_name, msg.lower())


                                print(len(mas_info_prepod))
                                """
                                for x in range(len(mas_info_prepod)):
                                    for y in range(len(mas_info_prepod[x])):
                                        if(mas_info_prepod[x][y]==""):
                                            info +=str(y+1)+") " +str(mas_info_prepod[x][y]) + "\n"
                                        else:
                                            info +=str(y+1)+") " +str(mas_info_prepod[x][y])
                                """

                                """
                                nomer = ""
                                sender(id, "Выбор", prepod_keyboard)
                                while(nomer == ""):
                                    for i in range(len(mas_name_prepod)):
                                        print(mas_name_prepod[i], msg.lower())
                                        if(mas_name_prepod[i]==msg.lower()):
                                            nomer = i
                                            break
                                    print(nomer)
                                    try:
                                        for y in range(len(mas_info_prepod[nomer])):
                                            if(mas_info_prepod[nomer][y]==""):
                                                info +=str(y+1)+") " +str(mas_info_prepod[nomer][y]) + "\n"
                                            else:
                                                info +=str(y+1)+") " +str(mas_info_prepod[nomer][y])
                                    except TypeError:
                                        pass
                                """
                                nomer = 0

                                for i in range(len(mas_name_prepod)):
                                    print(mas_name_prepod[i], msg.lower())
                                    if(mas_name_prepod[i]==msg.lower()):
                                        nomer = i
                                        break

                                sender(id, "Выбор", prepod_keyboard)
                                for y in range(len(mas_info_prepod[nomer])):
                                    if(mas_info_prepod[nomer][y]==""):
                                        info +=str(y+1)+") " +str(mas_info_prepod[nomer][y]) + "\n"
                                    else:
                                        info +=str(y+1)+") " +str(mas_info_prepod[nomer][y])

                                sender(id, info, prepod_keyboard)





                            elif(msg.lower() == "на эту неделю"):
                                pass





if __name__ == '__main__':
    main()
