# import json
# import os
import album
from bottle import request, HTTPError
from bottle import route
from bottle import run


# TODO  Веб-сервер принимает GET-запросы по адресу /albums/<artist>
#  и выводит на экран сообщение с количеством альбомов исполнителя artist и списком названий этих альбомов.
@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {}:<br>".format(artist)
        result += "<br>".join(album_names)
    return result

# TODO Веб-сервер принимает POST-запросы по адресу /albums/ и сохраняет переданные пользователем данные об альбоме.
#  Данные передаются в формате веб-формы. Если пользователь пытается передать данные об альбоме, который уже есть в базе данных,
#  обработчик запроса отвечает HTTP-ошибкой 409 и выводит соответствующее сообщение.
@route("/albums", method="POST")
def create_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")

    try:
        new_album = album.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:
        print("New #{} album successfully saved".format(new_album.id))
        result = "Альбом #{} успешно сохранен".format(new_album.id)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)

# TODO Запуск  GET terminal/cmd:
#  http -f http://localhost:8080/albums/Pink%20Floyd
# TODO Запуск  POST terminal/cmd:
#  http -f POST http://localhost:8080/albums artist="Ляпис Трубецкой" genre="рок" year=1998 album="Ты кинула"
