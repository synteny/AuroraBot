import MySQLdb
from settings import DATABASE


def get_connection():
    con_options = dict(
        host=DATABASE['HOST'], user=DATABASE['USER'],
        passwd=DATABASE['PASSWORD'], db=DATABASE["NAME"],
        use_unicode=True, charset="utf8")

    mydb = MySQLdb.connect(**con_options)
    return mydb.cursor(), mydb


def subscribe(chat_id, geo, geo_id):
    c, db = get_connection()
    q = """insert into users (geo, chat_id, geo_id)
    values ('%s', %s, %s)""" % (geo, chat_id, geo_id)
    c.execute(q)
    db.commit()


def unsubscribe(chat_id):
    c, db = get_connection()
    q = """delete from users where chat_id = %s""" % chat_id
    c.execute(q)
    db.commit()
