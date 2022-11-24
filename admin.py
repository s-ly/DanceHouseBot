###################################################################################################
# NOTE
###################################################################################################
# Главный модуль админки
###################################################################################################


###################################################################################################
# TODO
###################################################################################################
# Мне нужно сделать 3-ю страницу админки, где хранятся все анкеты.
###################################################################################################


# render_template - генерирует HTML
# request - получает данные из формы в HTML
from asyncore import write
from flask import Flask, render_template, request

import sql             # мой модуль работы с БД


app = Flask(__name__)

about = 't.me/DanceHouseBot ver 1.3 | 2022.11.24'
# title = 'Админка - телеграм бот школы танцев t.me/DanceHouseBot'
title = 'Админка - t.me/DanceHouseBot'
menu = [
    {'name': 'Контент', 'url': '/'}, 
    {'name': 'Расписание', 'url': 'timetable'},
    {'name': 'Анкеты', 'url': 'questionnaires'},
    ]

@app.route('/')
def index():
    """Перехватывает корневой адрес. Возвращает страницу index.html.
    the_title = 'Админка' - выводится в виде заголовка. """

    title_page = 'Редактирование контента'

    ###############################################################################################
    # Тексты
    
    # Зугружаем тексты из БД
    text_db_1_name = sql.sql_read_text(1, 'message_name')
    text_db_1 = sql.sql_read_text(1, 'message')
    
    text_db_2_name = sql.sql_read_text(2, 'message_name')
    text_db_2 = sql.sql_read_text(2, 'message')
    
    text_db_3_name = sql.sql_read_text(3, 'message_name')
    text_db_3 = sql.sql_read_text(3, 'message')
    
    text_db_4_name = sql.sql_read_text(4, 'message_name')
    text_db_4 = sql.sql_read_text(4, 'message')

    text_db_5_name = sql.sql_read_text(17, 'message_name')
    text_db_5 = sql.sql_read_text(17, 'message')

    text_db_6_name = sql.sql_read_text(18, 'message_name')
    text_db_6 = sql.sql_read_text(18, 'message')

    # Словарь текстов из БД
    text_db = {
        text_db_1_name: text_db_1, 
        text_db_2_name: text_db_2,
        text_db_3_name: text_db_3,
        text_db_4_name: text_db_4,
        text_db_5_name: text_db_5,
        text_db_6_name: text_db_6}

    ###############################################################################################
    # Картинки

    # Загружаем картинки в static
    img = sql.sql_read_img('timetable')
    def save_img(img):
        img_file = open('static/timetable.png', 'wb')
        img_file.write(img)
        img_file.close()
    save_img(img)

    img = sql.sql_read_img('poster')
    def save_img(img):
        img_file = open('static/poster.png', 'wb')
        img_file.write(img)
        img_file.close()
    save_img(img)

    # Словарь картинок из БД
    img_db = {
        'timetable': 'timetable.png',
        'poster': 'poster.png'}

    return render_template(
        'index.html', 
        the_title = title,
        the_title_page = title_page,
        the_menu = menu, 
        the_text_list = text_db, 
        the_img_dict = img_db, 
        the_about = about)


@app.route('/new_text', methods=['POST']) 
def new_text():
    """Показывает озменённый блок текста."""

    title_page = 'Текст отредактирован'
    new_text_id = None  # id блока текста

    # Получение данных из формы.
    # new_text - сам текст
    # new_text_id_name - это нужно что бы знать какой блок редактировали
    new_text = request.form['new_text']
    new_text_id_name = request.form['new_text_id_name']

    # Запись отредактированного текста в БД
    if new_text_id_name == 'about': new_text_id = 1
    if new_text_id_name == 'price': new_text_id = 2
    if new_text_id_name == 'contact': new_text_id = 3
    if new_text_id_name == 'start': new_text_id = 4
    if new_text_id_name == 'description_dances': new_text_id = 17
    if new_text_id_name == 'how_much': new_text_id = 18

    print(str(new_text_id))
    sql.ExecuteSQL_update(new_text_id, new_text)

    return render_template(
        'new_text.html', 
        the_title = title,
        the_title_page = title_page, 
        the_new_text = new_text, 
        the_new_text_id_name = new_text_id_name,
        the_about = about)


@app.route('/new_timetable', methods=['POST']) 
def new_timetable():
    """Показывает изменённый блок расписания. Сохраняет всё в БД"""
    title_page = 'Блок отредактирован'
    
    # Получение данных из формы.
    dance_edit = request.form['dance']
    timetable_dance_edit = request.form['timetable_dance']
    dey1_edit = request.form['day1']
    dey2_edit = request.form['day2']

    # Куда записывать данные
    if dance_edit == 'timetable_bachata':
        dance_id = 5
        dance_dey1_id = 9
        dance_dey2_id = 10
    if dance_edit == 'timetable_salsa':
        dance_id = 6
        dance_dey1_id = 11
        dance_dey2_id = 12
    if dance_edit == 'timetable_kizomba':
        dance_id = 7
        dance_dey1_id = 13
        dance_dey2_id = 14
    if dance_edit == 'timetable_lady_style':
        dance_id = 8
        dance_dey1_id = 15
        dance_dey2_id = 16

    # Записываем в БД
    sql.ExecuteSQL_update(dance_id, timetable_dance_edit)
    sql.ExecuteSQL_update(dance_dey1_id, dey1_edit)
    sql.ExecuteSQL_update(dance_dey2_id, dey2_edit)

    new_timetable = {
        'dance': dance_edit, 
        'timetable_dance': timetable_dance_edit, 
        'day1': dey1_edit, 
        'day2': dey2_edit
        }

    return render_template(
        'new_timetable.html',
        the_title = title,
        the_title_page = title_page,
        the_about = about, 
        the_new_timetable = new_timetable)


@app.route('/new_img', methods=['GET', 'POST']) 
def new_img():
    """Показывает новую картинку."""

    # Получаем из формы (скрытое поле) имя картинки и саму картинку
    new_img_name = request.form['new_img_name']
    new_img_name_db = request.form['new_img_name_db']
    new_img = request.files['new_img']
    new_img.save('static/' + new_img_name)

    sql.ExecuteSQL_Image_update(new_img_name_db, ('static/' + new_img_name))

    return render_template('new_img.html', the_new_img_name = new_img_name)


@app.route('/timetable', methods=['GET', 'POST']) 
def timetable():
    """Редактирование расписание."""

    title_page = 'Редактирование расписания'

    timetable = [
        {
        'dance': sql.sql_read_text(5, 'message_name'), 
        'timetable_dance': sql.sql_read_text(5, 'message'), 
        'day1': sql.sql_read_text(9, 'message'), 
        'day2': sql.sql_read_text(10, 'message')
        },
        {
        'dance': sql.sql_read_text(6, 'message_name'), 
        'timetable_dance': sql.sql_read_text(6, 'message'), 
        'day1': sql.sql_read_text(11, 'message'), 
        'day2': sql.sql_read_text(12, 'message')
        },
        {
        'dance': sql.sql_read_text(7, 'message_name'), 
        'timetable_dance': sql.sql_read_text(7, 'message'), 
        'day1': sql.sql_read_text(13, 'message'), 
        'day2': sql.sql_read_text(14, 'message')
        },
        {
        'dance': sql.sql_read_text(8, 'message_name'), 
        'timetable_dance': sql.sql_read_text(8, 'message'), 
        'day1': sql.sql_read_text(15, 'message'), 
        'day2': sql.sql_read_text(16, 'message')
        }
    ]

    return render_template(
        'timetable.html',
        the_title = title,
        the_title_page = title_page,
        the_menu = menu,
        the_about = about,
        the_timetable = timetable)


@app.route('/questionnaires', methods=['GET', 'POST']) 
def questionnaires():
    """Показывает анкеты."""

    title_page = 'Анкеты'

    return render_template(
        'questionnaires.html',
        the_title = title,
        the_title_page = title_page,
        the_menu = menu,
        the_about = about)


if __name__ == "__main__":
    app.run(debug=True, host='81.163.31.153', port=5001)
    # app.run(debug=True, host='0.0.0.0')