# Фукции для бота

# from aiogram import types

def getPhoto():    
    """возвращает фото расписания занятий"""
    photo = open('data/novoe_raspisanie.jpg', 'rb')
    return photo