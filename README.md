# 📚 Library Bot — Telegram-ассистент для управления библиотекой

---

## 📖 Описание

Этот Telegram-бот — ваш цифровой библиотекарь. Он позволяет просматривать каталог книг, брать и возвращать книги, а также управлять профилем пользователя. Администраторы получают доступ к удобной панели для управления книгами и просмотра данных о читателях.

---

## ✨ Возможности

### 📚 Каталог книг
- Просмотр всех книг с указанием доступности
- Поиск по автору
- Постраничный вывод для больших библиотек

### 👤 Профиль пользователя
- Создание и хранение профиля
- Безопасное хранение контакта (через запрос Telegram)
- История взятых книг

### 🛡️ Админ-панель
- Вход по паролю
- Просмотр всех книг и их статуса
- Добавление новых книг
- Удаление книг
- Список зарегистрированных пользователей
- Список должников

---

## 🚀 Команды и кнопки

| Команда | Описание |
|---------|----------|
| `/start` | Открыть главное меню |
| `/profile` | Просмотр или создание профиля |

| Кнопка | Действие |
|--------|----------|
| Показать все книги | 📋 Список всех книг с пагинацией |
| Поиск по автору | 🔍 Поиск по имени автора |
| Взять книгу | 📖 Взять книгу (нужен профиль) |
| Вернуть книгу | ↩️ Вернуть книгу |
| Админ панель | 👾 Вход в админку (нужен пароль) |
| Обо мне | ℹ️ Информация об авторе |

---

## 🛠️ Используемые технологии

- **Python 3.13+** — язык программирования
- **Aiogram 3.x** — фреймворк для Telegram Bot API
- **SQLite** — лёгкая реляционная база данных
- **Pydantic** — валидация данных

---

## 📁 Структура проекта
📁 library_bot/
├── 📄 task4.py # Основной файл бота
├── 📄 librarytask4.db # База данных (SQLite)
├── 📄 loger_admin.txt # Лог входов в админку
└── 📄 README.md # Документация

text

---

## 🚦 Запуск проекта

1. Клонируй репозиторий:
```bash
git clone https://github.com/DansDUSK/library_bot.git
cd library_bot
```
2. Установи зависимости:

```bash
pip install aiogram
```

Создай бота через @BotFather и получи BOT_TOKEN
Вставь токен в main() в файле task4.py

3. Запусти бота:

```bash
python task4.py
```
👨‍💻 Об авторе
Меня зовут Даниил (DansDagger). Я начинающий разработчик, изучаю Python и создаю Telegram-ботов. Этот проект — моя практическая работа, в которой я объединил работу с базами данных, асинхронным программированием и Telegram API.

📬 Контакты
GitHub: https://github.com/DansDUSK

Telegram: t.me/daggerka

⭐ Поддержка
Если проект был полезен — поставь звёздочку на GitHub! ⭐

📚 Library Bot — Telegram Assistant for Library Management
📖 Description
This Telegram bot is your digital library assistant. It allows you to browse books, borrow and return them, and manage your profile. Administrators have access to a convenient panel for managing books and viewing reader data.

✨ Features
📚 Book Catalog
View all books with availability status

Search by author name

Paginated view for large libraries

👤 User Profile
Create and store user profiles

Securely store contact information (via Telegram's native request)

Borrowing history

🛡️ Admin Panel
Password-protected login

View all books and their status

Add new books

Remove books

List of all registered users

List of debtors (users with unreturned books)

🚀 Commands and Buttons
Command	Description
/start	Open main menu
/profile	View or create profile
Button	Action
Show all books	📋 List of all books with pagination
Search by author	🔍 Search by author name
Take a book	📖 Borrow a book (profile required)
Return a book	↩️ Return a book
Admin panel	👾 Admin login (password required)
About me	ℹ️ Information about the author
🛠️ Tech Stack
Python 3.13+ — programming language

Aiogram 3.x — framework for Telegram Bot API

SQLite — lightweight relational database

Pydantic — data validation

📁 Project Structure
text
📁 library_bot/
├── 📄 task4.py                # Main bot file
├── 📄 librarytask4.db         # Database (SQLite)
├── 📄 loger_admin.txt         # Admin login log
└── 📄 README.md               # Documentation
🚦 How to Run
Clone the repository:

```bash
git clone https://github.com/DansDUSK/library_bot.git
cd library_bot
```
2. Install dependencies:

```bash
pip install aiogram
```
Create a bot via @BotFather and get your BOT_TOKEN
Insert your token in the main() function in task4.py

3. Run the bot:

```bash
python task4.py
```

👨‍💻 About the Author
My name is Daniil (DansDagger). I am a beginner developer learning Python and creating Telegram bots. This project is my practical work, combining databases, asynchronous programming, and the Telegram API.

📬 Contacts
GitHub: https://github.com/DansDUSK

Telegram: t.me/daggerka

⭐ Support
If you find this project useful — give it a star on GitHub! ⭐
