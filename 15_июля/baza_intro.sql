# кое-что из СУБД

SELECT fields_list (*)
FROM table_name
WHERE condition

-- например по годам выпуска типа того:
SELECT title, year, duration
    FROM films
        WHERE year >= 2005
            AND year <= 2007
            AND duration < 90
    ORDER BY year

    SELECT title, year, duration
    FROM films
        WHERE year BETWEEN 2005 AND 2007
            AND duration < 90
    ORDER BY year

--    пример не вполне корректного:
SELECT title, year, duration
    FROM films WHERE genre = 8
    ORDER BY year
-- а это пример вполне корректного составного:
SELECT title, year
    FROM films WHERE genre = (
        SELECT id FROM genres
            WHERE title = 'фантастика'
    )
    ORDER BY year

--    IN означает совпадение с чем-то из множества ()
    SELECT title, year, duration
        FROM films WHERE duration IN (45, 60, 90)
        ORDER BY duration DESC

--        группировка

--  подобие
-- % - это сколько угодно символов (или нисколько)
-- _ - это любой один символ
SELECT * FROM films
    WHERE title LIKE 'А_к%'
--    ещё есть ILIKE значит игнорируя регистр (не работает в SQLite)
--    ещё NOT LIKE конечно

-- без повторов
SELECT DISTINCT year FROM films ORDER BY year DESC

# а вот и великий джойн:
SELECT films.title AS Фильм, genres.title AS Жанр
    FROM films JOIN genres
        WHERE films.genre = genres.id
-- в данном случае эквивалентно:
SELECT films.title AS Фильм, genres.title AS Жанр
    FROM films, genres
        WHERE films.genre = genres.id

--какой джойн по умолчанию?
-- фул джойн не везде поддерживается

-- а вот и считалка
SELECT year, COUNT(*) AS Кол_во
    FROM films
    GROUP BY year
    ORDER BY Кол_во DESC

SELECT year, COUNT(*) AS Кол_во
    FROM films
    GROUP BY year HAVING Кол_во > 500
    ORDER BY Кол_во DESC

-- ДЗ мин-макс, групинг etc