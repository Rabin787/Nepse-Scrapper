import datetime

def already_ran_today(db):
    cursor = db.cursor()
    today = datetime.datetime.now().date()
    query = "SELECT COUNT(*) FROM company WHERE updated_on = %s"
    cursor.execute(query, (today,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0