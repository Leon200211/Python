import requests
from translate import Translator
from math import floor
from datetime import datetime, timedelta
import pendulum
import PIL.Image as Image
from datetime import date


list_time_day = ["Утро","День","Вечер","Ночь"]
list_of_points = [
    "север","северо-северо-восток","северо-восток","востоко-северо-восток",
    "восток","востоко-юго-восток","юго-восток","юго-юго-восток",
    "юг","юго-юго-запад","юго-запад","западо-юго-запад","запад",
    "западо-северо-запад","северо-запад","северо-северо-запад"
                  ]
list_of_points_2 = [
    "Тихий","Лёгкий","Слабый","Умеренный",
    "Свежий","Сильный","Крепкий","Очень крепкий",
    "Шторм","Сильный шторм","Жестокий шторм","Ураган"
]
translator= Translator(from_lang="english",to_lang="russian")
def deg_to_point(deg):
    return list_of_points[floor(((deg + 11.25) % 360) / 22.5)]
def speed_to_point(speed):
    print(floor((speed + 1.5)/1.5))
    return list_of_points_2[floor(((speed + 1.5) % 33) / 3)]


def weather(url, when):

    if(when == "сейчас"):
        info_weather = ""
        response = requests.get(url).json()
        print(response)
        temp_min = response['main']['temp_min']
        temp_min = round((((temp_min*1.8)-459.67)-32)/1.8, 1)
        temp_max = response['main']['temp_min']
        temp_max = round((((temp_max*1.8)-459.67)-32)/1.8, 1)

        feels_like_temp = response['main']['feels_like']
        humidity = response['main']['humidity']
        if(temp_min==temp_max):
            temperatura = str(temp_min)+ u'\N{DEGREE SIGN}' + "C"
        else:
            temperatura = str(temp_min)+" - " + str(temp_max) + u'\N{DEGREE SIGN}' + "C"
        info_weather += "Погода в Москве: " + translator.translate(response['weather'][0]['main']) + "\n"
        info_weather += translator.translate(response['weather'][0]['description'])+", температура: "+ temperatura +  "\n"
        info_weather += "Давление: "+ str(response['main']['pressure']) +" мм рт. ст., влажность: "+ str(response['main']['humidity'])+"%\n"
        info_weather += "Ветер: "+str(speed_to_point(response['wind']['speed'])) + ", " + str(round(response['wind']['speed'], 1)) + " м/с, направление: "+ str(deg_to_point(response['wind']['deg'])) +"\n"
        weather_photo = "http://openweathermap.org/img/w/" + str(response['weather'][0]['icon'])  +".png"
        print(info_weather)
        return info_weather, weather_photo

    if(when == "на завтра"):
        count_time = 0
        temperatura_string = ""
        mas_icon = []
        info_weather = ""
        response = requests.get(url).json()
        print(response)
        tomorrow = pendulum.tomorrow('Europe/Moscow').format('DD.MM')
        tomorrow = tomorrow[3:]+"-"+tomorrow[0:2]
        for i in range(len(response['list'])):
            if(response['list'][i]['dt_txt'][11:13] == "09" or response['list'][i]['dt_txt'][11:13] == "15" or response['list'][i]['dt_txt'][11:13] == "18"  or response['list'][i]['dt_txt'][11:13] == "21"):
                if(response['list'][i]['dt_txt'][5:10] == tomorrow):
                    print(response['list'][i]['dt_txt'][5:10], tomorrow)
                    temp_min = response['list'][i]['main']['temp_min']
                    temp_min = round((((temp_min*1.8)-459.67)-32)/1.8, 1)
                    temp_max = response['list'][i]['main']['temp_min']
                    temp_max = round((((temp_max*1.8)-459.67)-32)/1.8, 1)
                    feels_like_temp = response['list'][i]['main']['feels_like']
                    humidity = response['list'][i]['main']['humidity']
                    if(temp_min==temp_max):
                        temperatura = str(temp_min)+ u'\N{DEGREE SIGN}' + "C"
                    else:
                        temperatura = str(temp_min)+" - " + str(temp_max) + u'\N{DEGREE SIGN}' + "C"
                    count_time += 1
                    temp_min = response['list'][i]['dt_txt']
                    info_weather += "=========" + "\n"
                    info_weather += translator.translate(response['list'][i]['weather'][0]['description'])+", температура: "+ temperatura +  "\n"
                    info_weather += "Давление: "+ str(response['list'][i]['main']['pressure']) +" мм рт. ст., влажность: "+ str(response['list'][i]['main']['humidity'])+"%\n"
                    info_weather += "Ветер: "+str(speed_to_point(response['list'][i]['wind']['speed'])) + ", " + str(round(response['list'][i]['wind']['speed'], 1)) + " м/с, направление: "+ str(deg_to_point(response['list'][i]['wind']['deg'])) +"\n"
                    temperatura_string += str(temperatura)+ "//"
                    weather_photo = "http://openweathermap.org/img/w/" + str(response['list'][i]['weather'][0]['icon'])  +".png"
                    mas_icon.append(weather_photo)


        if(count_time == 4):
            info_weather = info_weather.replace("=========", list_time_day[0], 1)
            info_weather = info_weather.replace("=========", list_time_day[1], 1)
            info_weather = info_weather.replace("=========", list_time_day[2], 1)
            info_weather = info_weather.replace("=========", list_time_day[3], 1)
        if(count_time == 3):
            info_weather = info_weather.replace("=========", list_time_day[1], 1)
            info_weather = info_weather.replace("=========", list_time_day[2], 1)
            info_weather = info_weather.replace("=========", list_time_day[3], 1)
        if(count_time == 2):
            info_weather = info_weather.replace("=========", list_time_day[2], 1)
            info_weather = info_weather.replace("=========", list_time_day[3], 1)
        if(count_time == 1):
            info_weather = info_weather.replace("=========", list_time_day[3], 1)



    if(when == "на сегодня"):
        count_time = 0
        temperatura_string = ""
        mas_icon = []
        info_weather = ""
        response = requests.get(url).json()
        print(response)
        today = date.today()
        today =str(today)[5:]
        for i in range(len(response['list'])):
            if(response['list'][i]['dt_txt'][11:13] == "09" or response['list'][i]['dt_txt'][11:13] == "15" or response['list'][i]['dt_txt'][11:13] == "18"  or response['list'][i]['dt_txt'][11:13] == "21"):
                if(response['list'][i]['dt_txt'][5:10] == today):
                    print(today)
                    temp_min = response['list'][i]['main']['temp_min']
                    temp_min = round((((temp_min*1.8)-459.67)-32)/1.8, 1)
                    temp_max = response['list'][i]['main']['temp_min']
                    temp_max = round((((temp_max*1.8)-459.67)-32)/1.8, 1)

                    feels_like_temp = response['list'][i]['main']['feels_like']
                    humidity = response['list'][i]['main']['humidity']

                    if(temp_min==temp_max):
                        temperatura = str(temp_min)+ u'\N{DEGREE SIGN}' + "C"
                    else:
                        temperatura = str(temp_min)+" - " + str(temp_max) + u'\N{DEGREE SIGN}' + "C"


                    count_time += 1
                    temp_min = response['list'][i]['dt_txt']
                    info_weather += "=========" + "\n"
                    info_weather += translator.translate(response['list'][i]['weather'][0]['description'])+", температура: "+ temperatura +  "\n"
                    info_weather += "Давление: "+ str(response['list'][i]['main']['pressure']) +" мм рт. ст., влажность: "+ str(response['list'][i]['main']['humidity'])+"%\n"
                    info_weather += "Ветер: "+str(speed_to_point(response['list'][i]['wind']['speed'])) + ", " + str(round(response['list'][i]['wind']['speed'], 1)) + " м/с, направление: "+ str(deg_to_point(response['list'][i]['wind']['deg'])) +"\n"


                    weather_photo = "http://openweathermap.org/img/w/" + str(response['list'][i]['weather'][0]['icon'])  +".png"
                    mas_icon.append(weather_photo)

                    temperatura_string += str(temperatura) +"//"

        if(count_time == 4):
            info_weather = info_weather.replace("=========", list_time_day[0], 1)
            info_weather = info_weather.replace("=========", list_time_day[1], 1)
            info_weather = info_weather.replace("=========", list_time_day[2], 1)
            info_weather = info_weather.replace("=========", list_time_day[3], 1)
        if(count_time == 3):
            info_weather = info_weather.replace("=========", list_time_day[1], 1)
            info_weather = info_weather.replace("=========", list_time_day[2], 1)
            info_weather = info_weather.replace("=========", list_time_day[3], 1)
        if(count_time == 2):
            info_weather = info_weather.replace("=========", list_time_day[2], 1)
            info_weather = info_weather.replace("=========", list_time_day[3], 1)
        if(count_time == 1):
            info_weather = info_weather.replace("=========", list_time_day[3], 1)


    if(when == "на 5 дней"):
        temperatura_string = ""
        temperatura_string_2 = ""
        mas_icon = []
        info_weather = ""
        response = requests.get(url).json()
        print(response)
        for i in range(len(response['list'])):
            if(response['list'][i]['dt_txt'][11:13] == "15"):
                print(response['list'][i]['dt_txt'][5:10])
                temp_min = response['list'][i]['main']['temp_min']
                temp_min = round((((temp_min*1.8)-459.67)-32)/1.8, 1)
                temp_max = response['list'][i]['main']['temp_min']
                temp_max = round((((temp_max*1.8)-459.67)-32)/1.8, 1)
                feels_like_temp = response['list'][i]['main']['feels_like']
                humidity = response['list'][i]['main']['humidity']
                if(temp_min==temp_max):
                    temperatura = str(temp_min)+ u'\N{DEGREE SIGN}' + "C"
                else:
                    temperatura = str(temp_min)+" - " + str(temp_max) + u'\N{DEGREE SIGN}' + "C"
                temp_min = response['list'][i]['dt_txt']
                info_weather += "=========" + "\n"
                info_weather += translator.translate(response['list'][i]['weather'][0]['description'])+", температура: "+ temperatura +  "\n"
                info_weather += "Давление: "+ str(response['list'][i]['main']['pressure']) +" мм рт. ст., влажность: "+ str(response['list'][i]['main']['humidity'])+"%\n"
                info_weather += "Ветер: "+str(speed_to_point(response['list'][i]['wind']['speed'])) + ", " + str(round(response['list'][i]['wind']['speed'], 1)) + " м/с, направление: "+ str(deg_to_point(response['list'][i]['wind']['deg'])) +"\n"
                temperatura_string += str(temperatura)+ "//"
                weather_photo = "http://openweathermap.org/img/w/" + str(response['list'][i]['weather'][0]['icon'])  +".png"
                mas_icon.append(weather_photo)
            if(response['list'][i]['dt_txt'][11:13] == "21"):
                temp_min = response['list'][i]['main']['temp_min']
                temp_min = round((((temp_min*1.8)-459.67)-32)/1.8, 1)
                temp_max = response['list'][i]['main']['temp_min']
                temp_max = round((((temp_max*1.8)-459.67)-32)/1.8, 1)
                if(temp_min==temp_max):
                    temperatura = str(temp_min)+ u'\N{DEGREE SIGN}' + "C"
                else:
                    temperatura = str(temp_min)+" - " + str(temp_max) + u'\N{DEGREE SIGN}' + "C"

                temperatura_string_2 += str(temperatura)+ "//"


    for i in range(len(mas_icon)):
        image = requests.get(mas_icon[i], stream=True)
        with open(str(i)+".png", "wb") as f:
            f.write(image.content)
    img = Image.new('RGB', ((len(mas_icon))*50, 50))
    for i in range(len(mas_icon)):
        img1 = Image.open(str(i)+".png")
        print(i*50)
        img.paste(img1, (i*50, 0))
    img.save("image.png")

    print("=============")
    #print(info_weather)
    #print(mas_icon)

    try:
        info_weather += "\n" + temperatura_string + "\n" + temperatura_string_2
    except UnboundLocalError:
        info_weather += "\n" + temperatura_string

    return info_weather






