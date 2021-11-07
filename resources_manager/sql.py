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
    __sqlite(f"INSERT INTO users VALUES('{name}', '{password}', {id})")


def sqlite_3_select_identity_name(name: str):
    con = sqlite3.connect("../resources_manager/ttbm.db")
    cur = con.cursor()

    cur.execute(f"SELECT * FROM users WHERE name = '{name}'")
    text = cur.fetchone()

    con.commit()
    con.close()

    return text
    # __sqlite(f"SELECT * FROM users")
