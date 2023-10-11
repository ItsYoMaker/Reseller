import logging

from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import dbmanager
import kb
import text
import util
from bot import bot
from bot import dp
from states import AddUrl

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)
    logging.debug(dbmanager.get_list_of_urls())

@dp.callback_query(lambda c: c.data == 'paste_url')
async def paste_url_callback(callback_query: CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите ссылку для мониторинга: /url [название] [ссылка]")
    await state.set_state(AddUrl.enter_urlname)

@router.message(Command("url"))
async def cmd_url(msg: types.Message, command: CommandObject):
    if command.args:
        arguments = command.args.split(' ')
        dbmanager.add_url(arguments[0], arguments[1])
        await msg.answer("Вы успешно установили url для парсинга " + dbmanager.get_url(arguments[0]))

    else:
        await msg.answer("Пожалуйста, укажите url после /url!")

@router.message(Command("urldelete"))
async def cmd_urldelete(msg: types.Message, command: CommandObject):
    if command.args:
        dbmanager.delete_url(command.args)
        await msg.answer("Вы успешно удалили " + command.args)
    else:
        await msg.answer("Пожалуйста, укажите название после /urldelete!")

@router.message(Command("stop"))
async def cmd_stop(msg: Message):
    await util.restart_run_tasks()
    logging.debug('парсер остановлен')