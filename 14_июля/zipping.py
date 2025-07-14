from zipfile import ZipFile
import os

copy_files = [f for f in os.listdir() if f.endswith('.csv')]
print(copy_files)

with ZipFile('my_csvs.zip', 'w') as z:
    for f in copy_files:
        z.write(f)
        os.remove(f)

# вытащить пара способов:

# with ZipFile('my_csvs.zip', 'r') as zo:
#     zo.extractall()
#
# files_to_extract = ['people.csv', 'stuff.csv']
# with ZipFile('my_csvs.zip', 'r') as zo:
#     zo.extractall(members=files_to_extract)

# получить список файлов из него
with ZipFile('my_csvs.zip', 'r') as zo:
    print(zo.namelist())

# ДЗ регимся на openeathermap.org/api
# на дипломную страничку вставим и погоду в Питере
"""
    Astropy. Предоставляет инструменты для работы с астрономическими данными, включая расчёты эфемерид,
        преобразования координат. Поддерживает различные системы координат, включая экваториальные и эклиптические.
    PyEphem. Библиотека для астрономических расчётов, которая позволяет вычислять позиции небесных тел.
        Поддерживает расчёты эфемерид, восходов, кульминаций и заходов.
    Skyfield. Библиотека для вычисления эфемерид, основанная на данных от JPL (Jet Propulsion Laboratory).
        Позволяет вычислять позиции планет, спутников и других объектов.
"""
