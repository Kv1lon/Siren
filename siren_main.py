from pyrogram import Client, filters
import keyboard
from pygame import mixer  # Load the popular external library
import os
import asyncio

app = Client("my_account", api_id=10736822, api_hash="3a730347f1f410c6d8491fbfaed0add9", config_file="")
filenames = os.listdir()  # [] if no fi


def check(input_t, error_t):
    t = input(input_t)

    if "+" in t or "-" in t:
        print("checked_2")

        return t
    else:
        print(error_t)
        check(input_t, error_t)


def check_s_s(input_t, error_t):
    t = input(input_t)

    if t in filenames:
        print("checked")
        return t
    else:
        print(error_t)
        check_s_s(input_t, error_t)

plays = True
busy = True
mixer.init()
tel_channel = input("Введите название канала для отслеживания сирены (Например 'sirena_dp' //без '@' ): ")
call_text = input(
    "Введите часть текста сообщения канала при котором должна срабатывать сирена (внимание, текст чувствительный к "
    "символам, поэтому рекомндуеться просто скопировать из телеграмм канала уникальную часть сообщения о тревоге): ")

siren_music = check_s_s("Введите название файла для сирены (файл должен лежать в папке файла siren_main.exe  ): ",
                        "Такого файла нет в папке, проверьте корректность написания имени файла")

good_play = check("Проигрывать спец. звук при окончании сирены? (+ означает ДА, - означает НЕТ)",
                  "Введён не тот символ. Введите '+' или '-'")
if "+" in good_play:
    good_call_text = input(
        "Введите часть текста сообщения канала при котором должна срабатывать музыка отбоя сирены (внимание, "
        "текст чувствительный к символам, поэтому рекомндуеться просто скопировать из телеграмм канала уникальную "
        "часть "
        "сообщения о отбое тривоги): ")
    good_siren_music = check_s_s("Введите название файла для сирены (файл должен лежать в папке файла siren_main.exe  "
                                 "): ", "Такого файла нет в папке, проверьте корректность написания имени файла")
print("Отслеживание канала...")

@app.on_message(filters.channel and filters.create(lambda self, c, m: (m.chat.username == tel_channel)))
async def call(client, message):
    global plays, busy
    plays = True
    busy = True
    print("Пришло сообщение")
    m = await app.get_history(tel_channel, limit=1)
    if call_text in m[0].text:
        mixer.music.load(siren_music)
        await asyncio.sleep(0.1)
        while plays:
            mixer.music.play()
            print("В укрытие!!!")
            print("Что б остановить нажмите Enter")
            busy = mixer.music.get_busy()
            while busy:  # wait for music to finish playing
                await asyncio.sleep(0.1)
                busy = mixer.music.get_busy()
                if keyboard.is_pressed('enter'):
                    print("Остановлено")
                    plays = False
                    busy = False
                    mixer.music.stop()
                    break
    if "+" in good_play:
        if good_call_text in m[0].text:
            mixer.music.load(good_siren_music)
            await asyncio.sleep(0.1)
            while plays:
                mixer.music.play()
                print("Отмена тривоги")
                print("Что б остановить нажмите Enter")
                busy = mixer.music.get_busy()
                while busy:
                    await asyncio.sleep(0.1)
                    busy = mixer.music.get_busy()
                    if keyboard.is_pressed('enter'):
                        print("Остановлено")
                        print("Отслеживание канала продолжено...")
                        plays = False
                        busy = False
                        mixer.music.stop()
                        break


app.run()
