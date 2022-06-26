###################################################################################################
# NOTE
###################################################################################################
# Главный модуль админки
###################################################################################################


###################################################################################################
# TODO
###################################################################################################
# 
###################################################################################################


# render_template - генерирует HTML
# request - получает данные из формы в HTML
from asyncore import write
from flask import Flask, render_template, request

import sql             # мой модуль работы с БД


app = Flask(__name__)

about = ('t.me/DanceHouseBot - версия 1.1, дата 2022.06.26.' +
    ' Разработка t.me/SergeyLysov')

@app.route('/')
def index():
    """Перехватывает корневой адрес. Возвращает страницу index.html.
    the_title = 'Админка' - выводится в виде заголовка. """

    # Заголовок
    title = 'Админка - телеграм бот школы танцев t.me/DanceHouseBot'
    # about = ('t.me/DanceHouseBot - версия 1.1 alpha 2, дата 2022.06.25.' +
    # ' Разработка t.me/SergeyLysov')
    
    # Зугружаем тексты из БД
    text_db_1_name = sql.sql_read_text(1, 'message_name')
    text_db_1 = sql.sql_read_text(1, 'message')
    
    text_db_2_name = sql.sql_read_text(2, 'message_name')
    text_db_2 = sql.sql_read_text(2, 'message')
    
    text_db_3_name = sql.sql_read_text(3, 'message_name')
    text_db_3 = sql.sql_read_text(3, 'message')
    
    text_db_4_name = sql.sql_read_text(4, 'message_name')
    text_db_4 = sql.sql_read_text(4, 'message')

    # Словарь текстов из БД
    text_db = {
        text_db_1_name: text_db_1, 
        text_db_2_name: text_db_2,
        text_db_3_name: text_db_3,
        text_db_4_name: text_db_4}

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
        the_text_list = text_db, 
        the_img_dict = img_db, 
        the_about = about)


@app.route('/new_text', methods=['POST']) 
def new_text():
    """Показывает озменённый блок текста."""

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

    print(str(new_text_id))
    sql.ExecuteSQL_update(new_text_id, new_text)

    return render_template(
        'new_text.html', 
        the_title = 'Админка - текст отредактирован.', 
        the_new_text = new_text, 
        the_new_text_id_name = new_text_id_name,
        the_about = about)


# @app.route('/new_img') 
@app.route('/new_img', methods=['GET', 'POST']) 
# @app.route('/new_img', methods=['GET']) 
# @app.route('/new_img') 
def new_img():
    """Показывает новую картинку."""

    # Получаем из формы (скрытое поле) имя картинки и саму картинку
    new_img_name = request.form['new_img_name']
    new_img_name_db = request.form['new_img_name_db']
    new_img = request.files['new_img']
    new_img.save('static/' + new_img_name)

    sql.ExecuteSQL_Image_update(new_img_name_db, ('static/' + new_img_name))

    return render_template('new_img.html', the_new_img_name = new_img_name)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)