import datetime
import mysql.connector
from helper_functions import getPrice


config = {
    'host': 'sql6.freemysqlhosting.net',
    'user': 'sql6463885',
    'password': 'bL2AA8P8yc',
    'database': 'sql6463885'
}

def insertPriceAlert(email, token, price):

    try:
        conn = mysql.connector.connect(**config)
        print('DC connected')
    except Exception as e:
        print('Error: ' + str(e))
        raise Exception

    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE alerts (email VARCHAR(100), token VARCHAR(10), price VARCHAR (20), createdAt DATETIME)")
    except Exception as e:
        print('Error: ' + str(e))

    try:
        sql = """INSERT INTO alerts VALUES (%s, %s, %s, %s)"""
        now = datetime.datetime.utcnow()
        cursor.execute(sql, (email, token, str(price), now.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        print(f"Added alert for {email}, {token}, {price} at {now}")
    except Exception as e:
        print('Error: ' + str(e))
        raise Exception


def checkExistence(email):

    try:
        conn = mysql.connector.connect(**config)
        print('DC connected')
    except Exception as e:
        print('Error: ' + str(e))
        raise Exception

    cursor = conn.cursor()

    try:
        sql = """SELECT COUNT(email) FROM alerts WHERE email=%s"""
        cursor.execute(sql, (email,))
        number_of_alerts = cursor.fetchone()[0]
        print(number_of_alerts)
        return number_of_alerts
    except Exception as e:
        print("Error: " + str(e))
        return None


def getTokensAndPrices():
    try:
        conn = mysql.connector.connect(**config)
        print('DC connected')
    except Exception as e:
        print('Error: ' + str(e))
        raise Exception

    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT DISTINCT token FROM alerts""")
        result = cursor.fetchall()
        tokens = [x[0] for x in result]
        print(tokens)

        token_prices = {token: getPrice(token) for token in tokens}
        print(token_prices)
        return token_prices

    except Exception as e:
        print('Error: ' + str(e))
        raise Exception



def getAllAlerts():
    try:
        conn = mysql.connector.connect(**config)
        print('DC connected')
    except Exception as e:
        print('Error: ' + str(e))
        raise Exception

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT email, token, price FROM alerts")
        result = cursor.fetchall()
        print(result)
        return result

    except Exception as e:
        pass





if __name__ == "__main__":

    priceTable = getTokensAndPrices()

    result = getAllAlerts()

    for item in result:
        if float(item[2]) - 0.1 * float(item[2]) <= float(priceTable[item[1]]) <= float(item[2]) + 0.1 * float(item[2]):
            #alert(item[0], item[1], item[2])
            #print(f"we need to notify {item[0]}, his token {item[1]} is approaching his target value of {item[2]}")
            pass
