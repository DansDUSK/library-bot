import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

dp = Dispatcher()
class SearchState(StatesGroup):
    waiting_author = State()
    waiting_buy_book = State()
    return_book = State()
class ProfileState(StatesGroup):
    waiting_age = State()
    waiting_phone = State()
    waiting_password = State()
class BookState(StatesGroup):
    waiting_delete_name = State()
    waiting_name = State()
    waiting_author = State()
    waiting_year = State()

def get_db_library():
    conn = sqlite3.connect("librarytask4.db")
    cursor = conn.cursor()
    return conn, cursor

@dp.message(Command("start"))
async def start(message: types.Message) -> None:
    kb = [
        [types.InlineKeyboardButton(text="Показать все книги📚", callback_data="show_book"),
         types.InlineKeyboardButton(text="Поиск по автору🔎", callback_data="find_by_author")],
        [types.InlineKeyboardButton(text="Взять книгу🎇", callback_data="buy_book"),
         types.InlineKeyboardButton(text="Вернуть книгу😋", callback_data="return_book")],
        [types.InlineKeyboardButton(text="АДМИН ПАНЕЛЬ(НУЖЕН КОД!)👾", callback_data="admin_panel"),
         types.InlineKeyboardButton(text="Обо мне и боте✔", callback_data="about_me")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb) 
    await message.answer(f"Приветствую {message.from_user.full_name}, выберите взаимодействие в меню ниже!",reply_markup=keyboard)

@dp.message(Command("profile"))
async def start_profile(message: Message, state: FSMContext):
    user_id = message.from_user.id
    conn, cursor = get_db_library()
    cursor.execute("SELECT * FROM users WHERE id_profile = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if user:
        await message.answer(f"Ваш профиль🙍🏻‍♂️: Имя {user[1]}\nВозраст {user[2]}\nТелефон {user[3]}\nАйди профиля {user[4]}", reply_markup=keyboard)
    else:
        
        await message.answer("Профиль не найден!❌ Создаем...")
        await message.answer("Введите возраст (только число)", reply_markup=keyboard)
        await state.set_state(ProfileState.waiting_age)

@dp.message(ProfileState.waiting_age, F.text)
async def age_profile(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число!❌")
        return
    await state.update_data(age=int(message.text))
    
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Поделиться номером📱", request_contact=True)],
            [types.KeyboardButton(text="В меню👀")]
        ],
        resize_keyboard=True
    )
    await message.answer("📱 Поделитесь номером телефона:", reply_markup=kb)
    await state.set_state(ProfileState.waiting_phone)

@dp.message(ProfileState.waiting_phone, F.contact)
async def phone_profile(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    name = message.from_user.full_name
    data = await state.get_data()
    age = data.get("age")
    user_id = message.from_user.id
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    
    conn, cursor = get_db_library()
    cursor.execute("INSERT OR REPLACE INTO users (name, age, phone, id_profile) VALUES (?,?,?,?)", (name, age, phone, user_id))
    conn.commit()
    conn.close()
    
    await message.answer(f"Приятно познакомиться {name}\nПрофиль успешно сохранен!✔", reply_markup=types.ReplyKeyboardRemove())
    kb = [
        [types.InlineKeyboardButton(text="Показать все книги📚", callback_data="show_book"),
         types.InlineKeyboardButton(text="Поиск по автору🔎", callback_data="find_by_author")],
        [types.InlineKeyboardButton(text="Взять книгу🎇", callback_data="buy_book"),
         types.InlineKeyboardButton(text="Вернуть книгу😋", callback_data="return_book")],
        [types.InlineKeyboardButton(text="АДМИН ПАНЕЛЬ(НУЖЕН КОД!)👾", callback_data="admin_panel"),
         types.InlineKeyboardButton(text="Обо мне и боте✔", callback_data="about_me")]
    ]    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb) 
    await message.answer(f"Приветствую {message.from_user.full_name}, выберите взаимодействие в меню ниже!",reply_markup=keyboard)
    await state.clear()
    
@dp.callback_query(F.data=="menu")
async def menu(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton(text="Показать все книги🖨", callback_data="show_book"),
         types.InlineKeyboardButton(text="Поиск по автору🔎", callback_data="find_by_author")],
        [types.InlineKeyboardButton(text="Взять книгу🎇", callback_data="buy_book"),
         types.InlineKeyboardButton(text="Вернуть книгу😋", callback_data="return_book")],
        [types.InlineKeyboardButton(text="АДМИН ПАНЕЛЬ(НУЖЕН КОД!)👾", callback_data="admin_panel"),
         types.InlineKeyboardButton(text="Обо мне и боте✔", callback_data="about_me")]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb) 
    await callback.message.answer(f"Приветствую {callback.message.from_user.full_name}, выберите взаимодействие в меню ниже!",reply_markup=keyboard)
    
@dp.message(F.text=="В меню👀")
async def menu(message: Message, state: FSMContext):
    await state.clear()
    kb = [
        [types.InlineKeyboardButton(text="Показать все книги🖨", callback_data="show_book"),
         types.InlineKeyboardButton(text="Поиск по автору🔎", callback_data="find_by_author")],
        [types.InlineKeyboardButton(text="Взять книгу🎇", callback_data="buy_book"),
         types.InlineKeyboardButton(text="Вернуть книгу😋", callback_data="return_book")],
        [types.InlineKeyboardButton(text="АДМИН ПАНЕЛЬ(НУЖЕН КОД!)👾", callback_data="admin_panel"),
         types.InlineKeyboardButton(text="Обо мне и боте✔", callback_data="about_me")]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb) 
    await message.answer(f"Приветствую {message.from_user.full_name}, выберите взаимодействие в меню ниже!",reply_markup=keyboard)
    
user_books_cache = {}

@dp.callback_query(F.data == "show_book")
async def show_book(callback: types.CallbackQuery):
    conn, cursor = get_db_library()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await callback.message.edit_text("📚 Библиотека пуста!🙁", reply_markup=keyboard)
        await callback.answer()
        return
    
    user_books_cache[callback.from_user.id] = rows
    
    await show_page(callback.message, callback.from_user.id, 0, edit=True)
    await callback.answer()


async def show_page(message, user_id, page, edit=False):
    rows = user_books_cache.get(user_id, [])
    if not rows:
        await message.answer("❌ Список книг пуст")
        return
    page_size = 5  
    total_pages = (len(rows) + page_size - 1) // page_size
    if page < 0:
        page = 0
    if page >= total_pages:
        page = total_pages - 1
    start = page * page_size
    end = min(start + page_size, len(rows))
    text = f"📚 Книги (страница {page + 1}/{total_pages}):\n\n"
    for i in range(start, end):
        row = rows[i]
        status = '✅ В наличии' if row[5] == 1 else '❌ Нет в наличии'
        text += f"{i + 1}) {row[1]} | {row[2]} | {row[3]} | {status}\n"
    kb = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"book_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(types.InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"book_page_{page + 1}"))
    if nav_buttons:
        kb.append(nav_buttons)
    action_buttons = []
    if page == 0:  
        action_buttons.append(types.InlineKeyboardButton(text="Взять книгу🎇", callback_data="buy_book"))
    action_buttons.append(types.InlineKeyboardButton(text="В меню👀", callback_data="menu"))
    kb.append(action_buttons)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    
    if edit:
        await message.edit_text(text, reply_markup=keyboard)
    else:
        await message.edit_text(text, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data and c.data.startswith("book_page_"))
async def book_page_handler(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await show_page(callback.message, callback.from_user.id, page, edit=True)
    await callback.answer()

@dp.callback_query(F.data=="find_by_author")
async def find_by_author(callback: types.CallbackQuery, state: FSMContext):
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Введите имя автора👾", reply_markup=keyboard)
    await state.set_state(SearchState.waiting_author)
    await callback.answer()
    
@dp.message(SearchState.waiting_author, F.text)
async def search_author(message: Message, state: FSMContext):
    author = message.text
    conn, cursor = get_db_library()
    cursor.execute("SELECT * FROM books WHERE author LIKE ?", (f"%{author}%",))
    rows = cursor.fetchall()
    conn.close()
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if not rows:
        await message.answer("Не найдено книг введеного автора❌\nПроверьте правильность вводимых данных!", reply_markup=keyboard)
        return
    
    text = f"📚Книги автора *{author}:\n\n"
    for i, row in enumerate(rows):
            text += f"{i}) {row[1]} | {row[2]} | {row[3]} год | {'✔ В наличии' if row[5] == 1 else '❌ Нет в наличии'}\n"
    await message.answer(text, reply_markup=keyboard)
    await state.clear()
        
@dp.callback_query(F.data=="buy_book")
async def buy_book(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    conn, cursor = get_db_library()
    cursor.execute("SELECT name, age, phone FROM users WHERE id_profile = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if not user:
        await callback.message.edit_text("⚠Профиль не найден, создайте профиль: /profile", reply_markup=keyboard)
        await callback.answer()
        return
    
    name, age, phone = user
    await state.update_data(name=name, age=age, phone=phone)
    await callback.message.edit_text("Введите название книги для взятия👀", reply_markup=keyboard)
    await state.set_state(SearchState.waiting_buy_book)  
    await callback.answer()
    
@dp.message(SearchState.waiting_buy_book, F.text)
async def book_buy(message: Message, state: FSMContext):
    book = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    name = data.get("name", "Неизвестно⚠")
    age = data.get("age", "-")
    phone = data.get("phone", "-")
    conn, cursor = get_db_library()
    cursor.execute("SELECT * FROM books WHERE title = ?", (book,))
    books = cursor.fetchone()
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if books:
        if books[5] == 1:
            cursor.execute("UPDATE books SET is_available = 0 WHERE title = ?", (book,))
            cursor.execute("INSERT INTO borrowers (profile_id, name, age, phone, book_title, borrow_date) VALUES (?,?,?,?,?,?)", (user_id, name,  age, phone, book, message.date.strftime("%Y-%m-%d")))
            conn.commit()
            await message.answer(f"Книга {book} успешно выдана!✔\nВаша ссылка на книгу🔎: [Тык]({books[4]})",reply_markup=keyboard, parse_mode="Markdown")
        else:
            await message.answer(f"Книги {book} нету на складе!❌",reply_markup=keyboard)
    else:
        await message.answer(f"Книга {book} не найдена, проверьте вводимы данные!❌", reply_markup=keyboard) 
    await state.clear() 
    conn.close() 
    
@dp.callback_query(F.data=="return_book")
async def return_book(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    conn, cursor = get_db_library()
    cursor.execute("SELECT name, age, phone FROM users WHERE id_profile = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if not user:
        await callback.message.edit_text("⚠Профиль не найден, создайте профиль: /profile", reply_markup=keyboard)
        await callback.answer()
        return
    
    name, age, phone = user
    await state.update_data(name=name, age=age, phone=phone)
    await callback.message.edit_text("Введите название книги для возврата✍🏻", reply_markup=keyboard)
    await state.set_state(SearchState.return_book)  
    await callback.answer()
    
@dp.message(SearchState.return_book, F.text)
async def book_return(message: Message, state: FSMContext):
    book = message.text
    conn, cursor = get_db_library()
    cursor.execute("SELECT * FROM books WHERE title = ?", (book,))
    books = cursor.fetchone()
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if not books:
        await message.answer(f"Книга {book} не найдена в библиотеке, проверьте вводимые данные! ❌", reply_markup=keyboard)
        conn.close()
        await state.clear()
        return
    
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM borrowers WHERE book_title = ? AND profile_id = ?", (book, user_id))
    borrow = cursor.fetchone()
    if not borrow:
        await message.answer(f"Книга {book} за вами не числится!❌", reply_markup=keyboard)
        conn.close()
        await state.clear()
        return
    
    cursor.execute("DELETE FROM borrowers WHERE book_title = ? AND profile_id = ?", (book, user_id))
    cursor.execute("UPDATE books SET is_available = 1 WHERE title = ?", (book,))
    conn.commit()
    conn.close()
    await message.answer(f"Книга {book} успешно возращена!✔", reply_markup=keyboard)
    await state.clear()
    
async def logging_admin(name, profile_id, date, dostup):
    with open("loger_admin.txt", "w", encoding="utf-8") as f:
        f.write(f"Входил: {name}")
        f.write(f"ID профиля: {profile_id}")
        f.write(f"Дата входа: {date}")
        f.write(f"Доступ: {dostup}")    
        f.write('-' * 40 + '\n')
        

@dp.callback_query(F.data == "admin_panel")
async def admin_panel(callback: types.CallbackQuery, state: FSMContext):
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.edit_text("Вход в админ панель! Введите код или вернитесь в меню!", reply_markup=keyboard)
    await state.set_state(ProfileState.waiting_password)  
    await callback.answer()
@dp.message(ProfileState.waiting_password, F.text)
async def admin_panel_password(message: Message, state: FSMContext):
    kb1 = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard1 = types.InlineKeyboardMarkup(inline_keyboard=kb1)
    if message.text != "1602admin":
        await message.answer("❌Вы ввели неверный код! Доступ запрещен!❌", reply_markup=keyboard1)
        logging_admin(message.from_user.full_name, message.from_user.id, message.date.strftime("%Y-%m-%d"), "Запрещен! Введен неверный код!❌")
        await state.clear()
        return
    kb = [
        [types.InlineKeyboardButton(text="Должники👾", callback_data="dolgi")],
        [types.InlineKeyboardButton(text="Зарегистрированные профили👾", callback_data="profili")],
        [types.InlineKeyboardButton(text="Удаление книги🙁", callback_data="delete_book")],
        [types.InlineKeyboardButton(text="Добавление книги😋", callback_data="append_book")],
        [types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Добро пожаловать в админ панель! Выберите взаимодействие ниже🎇", reply_markup=keyboard)
    logging_admin(message.from_user.full_name, message.from_user.id, message.date.strftime("%Y-%m-%d"), "Разрешен! Код верен!✔")
    await state.clear()
    
@dp.callback_query(F.data == "admin_panel_password1")
async def admin_panel_password1(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton(text="Должники👾", callback_data="dolgi")],
        [types.InlineKeyboardButton(text="Зарегистрированные профили👾", callback_data="profili")],
        [types.InlineKeyboardButton(text="Удаление книги🙁", callback_data="delete_book")],
        [types.InlineKeyboardButton(text="Добавление книги😋", callback_data="append_book")],
        [types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Добро пожаловать в админ панель! Выберите взаимодействие ниже🎇", reply_markup=keyboard)
    await callback.answer()
         
@dp.callback_query(F.data == "dolgi")
async def dolgi(callback: types.CallbackQuery):
    conn, cursor = get_db_library()
    await callback.message.edit_text("Загружаю базу должников...📝")
    asyncio.sleep(2)
    cursor.execute("SELECT * FROM borrowers")
    borrow = cursor.fetchall()
    conn.close()
    kb = [[types.InlineKeyboardButton(text="Назад👾", callback_data="admin_panel_password1")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if not borrow:
        await callback.message.edit_text("❌Должников не найдено, или базы нету❌", reply_markup=keyboard)
        await callback.answer()
        return
    
    text = "Должники библиотеки📚:\n\n"
    for row in borrow:
        text += f"ID {row[0]}: ID профиля: {row[1]} | Имя: {row[2]} | Возраст: {row[3]} | Телефон: {row[4]}\nКнига: {row[5]} | Дата взятия: {row[6]}\n"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
    
@dp.callback_query(F.data == "profili")
async def profili(callback: types.CallbackQuery):
    conn, cursor = get_db_library()
    await callback.message.edit_text("Загружаю базу зарегистрированных профилей...📝")
    asyncio.sleep(2)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    kb = [[types.InlineKeyboardButton(text="Назад👾", callback_data="admin_panel_password1")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if not users:
        await callback.message.edit_text("❌Зарегистрированных профилей не найдено, или базы нету❌", reply_markup=keyboard)
        await callback.answer()
        return
    
    text = "Зарегистрированные профили библиотеки🙍🏻‍♂️:\n\n"
    for row in users:
        text += f"ID {row[0]}: Имя: {row[1]} | Возраст: {row[2]} | Телефон: {row[3]} | ID профиля: {row[4]}\n"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "delete_book")
async def delete_book(callback: types.CallbackQuery, state: FSMContext):
    kb = [[types.InlineKeyboardButton(text="Назад👾", callback_data="admin_panel_password1")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.edit_text("⚠Введите название книги для удаления⚠", reply_markup=keyboard)
    await state.set_state(BookState.waiting_delete_name)
    await callback.answer()
@dp.message(BookState.waiting_delete_name, F.text)
async def delete_name(message: Message, state: FSMContext):
    book = message.text
    conn, cursor = get_db_library()
    cursor.execute("SELECT * FROM books WHERE title = ?", (book,))
    books = cursor.fetchone()
    kb = [[types.InlineKeyboardButton(text="Назад👾", callback_data="admin_panel_password1")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if books:
        cursor.execute("DELETE FROM books WHERE title = ?", (book,))
        conn.commit()
        await message.answer(f"Книга {book} успешно удалена!✔", reply_markup=keyboard)
    else:
        await message.answer(f"❌Книга {book} не найдена!❌", reply_markup=keyboard)
    await state.clear()
    conn.close()

@dp.callback_query(F.data == "append_book")
async def append_book(callback: types.CallbackQuery, state: FSMContext):
    kb = [[types.InlineKeyboardButton(text="Назад👾", callback_data="admin_panel_password1")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.edit_text("🎇Введите название книги для добавления в библиотеку🎇", reply_markup=keyboard)
    await state.set_state(BookState.waiting_name)
    await callback.answer()
    
@dp.message(BookState.waiting_name, F.text)
async def book_name(message: Message, state: FSMContext):
    await state.update_data(book_name=message.text)
    kb = [[types.InlineKeyboardButton(text="Назад👾", callback_data="admin_panel_password1")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("🙍🏻‍♂️Введите автора книги🙍🏻‍♂️", reply_markup=keyboard)
    await state.set_state(BookState.waiting_author)
@dp.message(BookState.waiting_author, F.text)
async def book_author(message: Message, state: FSMContext):
    await state.update_data(book_author=message.text)
    kb = [[types.InlineKeyboardButton(text="Назад👾", callback_data="admin_panel_password1")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("📅Введите год издания книги (только число)📅", reply_markup=keyboard)
    await state.set_state(BookState.waiting_year)
@dp.message(BookState.waiting_year, F.text)
async def book_year(message: Message, state: FSMContext):
    kb = [[types.InlineKeyboardButton(text="Назад👾", callback_data="admin_panel_password1")]]
    keyboard1 = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if not message.text.isdigit():
        await message.answer("❌Ошибка! Введите число (например 1934)❌", reply_markup=keyboard1)
        return
    
    year = int(message.text)
    data = await state.get_data()
    name = data.get("book_name")
    author = data.get("book_author")
    
    conn, cursor = get_db_library()
    cursor.execute("SELECT * FROM books WHERE title = ? AND author = ?", (name, author))
    availability = cursor.fetchone()
    
    if availability:
        await message.answer("❌Книга уже есть в библиотеке или произошла ошибка!❌", reply_markup=kb)
        conn.close()
        await state.clear()
        return
    
    cursor.execute("INSERT INTO books (title, author, year, is_available) VALUES (?, ?, ?, ?)", (name, author, year, 1))
    conn.commit()
    conn.close()
    
    await message.answer(f"Книга {name} успешно добавлена✔", reply_markup=keyboard1)
    
    kb = [
        [types.InlineKeyboardButton(text="Должники👾", callback_data="dolgi")],
        [types.InlineKeyboardButton(text="Зарегистрированные профили👾", callback_data="profili")],
        [types.InlineKeyboardButton(text="Удаление книги🙁", callback_data="delete_book")],
        [types.InlineKeyboardButton(text="Добавление книги😋", callback_data="append_book")],
        [types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Добро пожаловать в админ панель! Выберите взаимодействие ниже🎇", reply_markup=keyboard)
    await state.clear()

@dp.callback_query(F.data=="about_me")
async def about_me(callback: types.CallbackQuery):
    kb = [[types.InlineKeyboardButton(text="В меню👀", callback_data="menu")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text = (
        "👋 Привет!\n\n"
        "Меня зовут *DansDagger(настоящее имя Даниил)*.\n"
        "Этот бот — мой учебный проект на **Python + Aiogram**.\n\n"
        "📚 Здесь я реализовал:\n"
        "• Базу данных книг\n"
        "• Профили пользователей и базу данных для них\n"
        "• Выдачу и возврат книг и базу должников\n"
        "• Админ-панель\n\n"
        "💡 Проект создавался для практики и души.\n"
        "Буду рад, если он будет полезен!\n\n"
        "🔗 Мой GitHub: [Тык](https://github.com/DansDUSK)\n"
        "📩 Контакты: [Тык](t.me/daggerka)\n\n"
        "*Спасибо, что пользуешься!* 😊"
    )
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()
    
async def main() -> None:
    token = "8879159359:AAEZezS9elloX6UPe92fkzJCflOIp4DLobo"
    bot = Bot(token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print('=' * 50)
        print('🎉Бот запущен, приятного использования!')
        print('=' * 50)
        asyncio.run(main())   
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")