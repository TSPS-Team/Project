import sqlite3


def __sqlite(query: str):
    con = sqlite3.connect("../resources_manager/ttbm.db")
    cur = con.cursor()

    cur.execute(query)
    result = cur.fetchall()

    con.commit()
    con.close()

    return result


def sqlite_3_add_user(name: str, password: str, id: int):
    __sqlite(f"INSERT INTO users(name, password, id) VALUES('{name}', '{password}', {id})")


def sqlite_3_select_identity_name(name: str):
    try:
        text = __sqlite(f"SELECT * FROM users WHERE name = '{name}'")[0]
        return text
    except IndexError:
        return []


def sqlite_3_create_statistic(name: str, hours: float, win_rates: float, count_of_wins: int, count_of_plays: int):
    key = __sqlite(f"SELECT key FROM users WHERE name = '{name}'")[0][0]
    __sqlite(f"INSERT INTO statistic(hours, win_rates, count_of_wins, count_of_plays, key) VALUES({hours}, {win_rates}"
             f", {count_of_wins}, {count_of_plays}, {key});")


def sqlite_3_update_statistic(name: str, hours: float, win_rates: float, count_of_wins: int, count_of_plays: int):
    key = __sqlite(f"SELECT key FROM users WHERE name = '{name}'")[0][0]
    __sqlite(f"UPDATE statistic SET hours = {hours}, win_rates = {win_rates}, count_of_wins = {count_of_wins}, "
             f"count_of_plays = {count_of_plays} WHERE key = {key}")


def sqlite_3_get_statistic(name: str):
    key = __sqlite(f"SELECT key FROM users WHERE name = '{name}'")[0][0]
    statistic = __sqlite(f"SELECT hours, win_rates, count_of_wins, count_of_plays FROM statistic WHERE key = {key}")[0]
    return statistic


def sqlite_3_create_info(name: str, date: str, gender: str, description: str):
    key = __sqlite(f"SELECT key FROM users WHERE name = '{name}'")[0][0]
    __sqlite(f"INSERT INTO info(date, gender, description, key) VALUES('{date}', '{gender}', '{description}', {key})")


def sqlite_3_get_info(name: str):
    key = __sqlite(f"SELECT key FROM users WHERE name = '{name}'")[0][0]
    info = __sqlite(f"SELECT date, gender, description FROM info WHERE key = {key}")[0]
    return info


def sqlite_3_create_view(table: str):
    __sqlite(f"CREATE VIEW [{table}] AS SELECT users.key, users.name, users.id, users.password, info.date, "
             f"info.description FROM users INNER JOIN info ON users.key=info.key ORDER BY users.key;")


def sqlite_3_get_view(table: str):
    view = __sqlite(f"SELECT * FROM [{table}]")
    return view


def sqlite_3_drop_view(table: str):
    __sqlite(f"DROP VIEW [{table}]")

# print(sqlite_3_select_identity_name('Leshqa_Random'))
# sqlite_3_create_statistic('Leshqa_Random', 0, 0, 0, 0)
# sqlite_3_update_statistic('Leshqa_Random', 0, 50, 1, 2)
# print(sqlite_3_get_statistic('Leshqa_Random'))
# sqlite_3_create_info('Leshqa_Random', '2001-10-18', 'male', 'NULL')
# print(sqlite_3_get_info('Leshqa_Random'))
# sqlite_3_create_view("test")
# print(sqlite_3_get_view("test"))
# sqlite_3_drop_view("test")
