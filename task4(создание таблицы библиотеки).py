import sqlite3

conn = sqlite3.connect("librarytask4.db")
cursor = conn.cursor()

conn.execute("""CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year INT,
    link TEXT,
    is_available INTEGER DEFAULT 1)""")

conn.commit()

books_data = [
    ("Война и мир", "Толстой Л.Н.", 1869,"https://ilibrary.ru/text/11/p.1/index.html"),
    ("Преступление и наказание", "Достоевский Ф.М.", 1866,"https://ilibrary.ru/text/69/p.1/index.html"),
    ("Мастер и Маргарита", "Булгаков М.А.", 1967,"https://www.vehi.net/mbulgakov/master/index.html"),
    ("1984", "Оруэлл Дж.", 1949,"https://opentextnn.ru/old/man/index.html@id=5134"),
    ("Скотный двор", "Оруэлл Дж.", 1945,"https://mishka-knizhka.ru/rasskazy-dlya-detej/sbornik-rasskazov/skotnyj-dvor/"),
    ("Герой нашего времени", "Лермонтов М.Ю.", 1840,"https://ilibrary.ru/text/12/p.1/index.html"),
    ("Мертвые души", "Гоголь Н.В.", 1842,"https://ilibrary.ru/text/78/p.1/index.html"),
    ("Отцы и дети", "Тургенев И.С.", 1862,"https://ilibrary.ru/text/96/p.1/index.html"),
    ("Тихий Дон", "Шолохов М.А.", 1928,"https://sholohov.lit-info.ru/sholohov/proza/tihij-don/index.htm"),
    ("Доктор Живаго", "Пастернак Б.Л.", 1957,"https://loveread.ec/read_book.php?id=10611&p=1"),
    ("Собачье сердце", "Булгаков М.А.", 1925,"https://rushist.com/index.php/rus-literature/3084-bulgakov-sobache-serdtse-polnyj-tekst"),
    ("Пикник на обочине", "Стругацкие А. и Б.", 1972,"https://loveread.ec/read_book.php?id=3622&p=1"),
    ("Улисс", "Джойс Дж.", 1922, "https://loveread.ec/read_book.php?id=67269&p=1"),
    ("Волхв", "Фаулз Дж.", 1965, "https://loveread.ec/read_book.php?id=16213&p=1"),
    ("Имя розы", "Эко У.", 1980, "https://loveread.ec/read_book.php?id=3712&p=1"),
    ('Дюна', 'Герберт Ф.', 1965, "https://loveread.ec/read_book.php?id=8582&p=1#gl_1"),
    ('Автостопом по галактике', 'Адамс Д.', 1979, "https://loveread.ec/read_book.php?id=28230&p=1"),
    ('451 градус по Фаренгейту', 'Брэдбери Р.', 1953, "https://loveread.ec/read_book.php?id=2039&p=1"),
    ('Марсианин', 'Уир Э.', 2011, "https://loveread.ec/read_book.php?id=37991&p=1"),
    ('Гарри Поттер и философский камень', 'Роулинг Дж.К.', 1997, "https://loveread.ec/read_book.php?id=2317&p=1#gl_1"),
    ('Властелин колец: Братство кольца', 'Толкин Дж.Р.Р.', 1954, "https://loveread.ec/read_book.php?id=2345&p=1"),
    ('Хоббит', 'Толкин Дж.Р.Р.', 1937, "https://loveread.ec/read_book.php?id=2344&p=1"),
    ('Три товарища', 'Ремарк Э.М.', 1936, "https://loveread.ec/read_book.php?id=3330&p=1"),
    ('Над пропастью во ржи', 'Сэлинджер Дж.Д.', 1951, ""),
    ('Убить пересмешника', 'Ли Х.', 1960, "https://loveread.ec/read_book.php?id=3617&p=1"),
    ('Портрет Дориана Грея', 'Уайльд О.', 1890, "https://loveread.ec/read_book.php?id=2502&p=1"),
    ('Шерлок Холмс: Этюд в багровых тонах', 'Дойл А.К.', 1887, "https://loveread.ec/read_book.php?id=111804&p=77"),
    ('Таинственный остров', 'Верн Ж.', 1874, "https://loveread.ec/read_book.php?id=6507&p=1"),
    ('Двадцать тысяч лье под водой', 'Верн Ж.', 1870, "https://loveread.ec/read_book.php?id=6505&p=1"),
    ('Остров сокровищ', 'Стивенсон Р.Л.', 1883, "https://loveread.ec/read_book.php?id=9565&p=1#gl_1"),
    ('Братья Карамазовы', 'Достоевский Ф.М.', 1880, "https://loveread.ec/read_book.php?id=1728&p=1"),
    ('Идиот', 'Достоевский Ф.М.', 1869, "https://loveread.ec/read_book.php?id=1730&p=1"),
    ('Бесы', 'Достоевский Ф.М.', 1872, "https://loveread.ec/read_book.php?id=1727&p=1"),
    ('Подросток', 'Достоевский Ф.М.', 1875, "https://loveread.ec/read_book.php?id=1731&p=1"),
    ('Анна Каренина', 'Толстой Л.Н.', 1877, "https://loveread.ec/read_book.php?id=3621&p=1"),
    ('Воскресение', 'Толстой Л.Н.', 1899, "https://ilibrary.ru/text/1462/index.html"),
    ('Детство', 'Толстой Л.Н.', 1852, "https://ilibrary.ru/text/1179/p.1/index.html"),
    ('Отрочество', 'Толстой Л.Н.', 1854, "https://ilibrary.ru/text/1310/p.1/index.html"),
    ('Юность', 'Толстой Л.Н.', 1857, "https://ilibrary.ru/text/1334/p.1/index.html"),
    ('Герой нашего времени', 'Лермонтов М.Ю.', 1840, "https://loveread.ec/read_book.php?id=3019&p=1"),
    ('Князь Серебряный', 'Толстой А.К.', 1862, "https://ilibrary.ru/text/4320/p.1/index.html"),
    ('Петербург', 'Белый А.', 1913, "https://dugward.ru/library/beliy/beliy_peterburg.html#a100"),
    ('Записки из подполья', 'Достоевский Ф.М.', 1864, "https://loveread.ec/read_book.php?id=1738&p=1"),
    ('Смерть Ивана Ильича', 'Толстой Л.Н.', 1886, "https://ilibrary.ru/text/7/p.1/index.html"),
    ('Хаджи-Мурат', 'Толстой Л.Н.', 1912, "https://ilibrary.ru/text/1006/p.1/index.html")
]

cursor.executemany("""INSERT INTO books (title, author, year, link)
                   VALUES (?,?,?,?)""", (books_data))
conn.commit()
cursor.execute("SELECT * FROM books")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]} | Name: {row[1]} | Author: {row[2]} | Year: {row[3]} | Available: {"Yes" if row[4] == 1 else "No"} | Link: {row[5]}")
    
conn.close()