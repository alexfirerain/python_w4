--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.17 в Вт июл 15 14:17:33 2025
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: users
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER NOT NULL);
INSERT INTO users (id, name, age) VALUES (1, 'Билли', 23);
INSERT INTO users (id, name, age) VALUES (3, 'Ватыч', 22);
INSERT INTO users (id, name, age) VALUES (4, 'Михася', 20);
INSERT INTO users (id, name, age) VALUES (6, 'Юдыштыра', 39);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
