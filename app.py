from flask import Flask, request
from flask_restful import reqparse
from flask_mail import Mail, Message

from validate_email import validate_email
from dbconnector import insertPriceAlert, checkExistence, getTokensAndPrices, getAllAlerts
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)
app.config['SECRET_KEY'] = "1234567890abcdefghijklmnopqrstuvwxyz"

app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cryptokenalerts@gmail.com'
app.config['MAIL_PASSWORD'] = 'fabdullah230'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

def sendEmail(email, token, price):

    htmlMessage = """<div style="background-color: #090942; width: 500px; height: 450px;">
<h1 style="color: white; text-align: center; padding-top: 10px;"><img style="width: 25px; margin-top: 10px;" src="https://github.com/fabdullah230/fabdullah230/blob/main/CrypToken_black.png?raw=true" /> CrypToken</h1>
<h2 style="color: white; font-size: 20px; text-align: center; margin-top: 50px;">Hello {email}!</h2>
<h3 style="color: white; font-size: 15px; text-align: center; margin-top: 50px; padding: 20px;">Your token of interest, {token}, is approaching your target value of {price}</h3>
<h5 style="color: white; font-size: 12px; text-align: center; margin-top: 100px; padding: 20px;">Click <a href="https://cryptoken.netlify.app/" style="color:#f0be37">here</a> to visit site</h5>
</div>""".format(email=email, token=token, price=price)



    msg = Message("Price alert for " + token, sender="cryptokenalerts@gmail.com", recipients=[email])
    msg.html = htmlMessage
    mail.send(msg)





@app.route("/add", methods=['POST'])
def addAlertEntry():
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument('email', required=True)  # add args
    parser.add_argument('token', required=True)
    parser.add_argument('price_target', required=True)

    args = parser.parse_args()  # parse arguments to dictionary
    email = args['email']
    token = args['token']
    price_target = args['price_target']

    if not bool(validate_email(email)):
        return {'error': 'invalid email address'}, 403

    if not valid_decimal(price_target):
        return {'error': 'invalid price target'}, 403




    try:
        if checkExistence(email) >= 5:
            raise Exception("Already 5 alerts for this user")
        insertPriceAlert(email, token, price_target)
        #print(checkExistence(email))
        return {'Status': 'Successfully added alert entry'}, 200
    except Exception as e:
        print(f'Error: Could not add alert for {email}, {token}, {price_target}')
        return {'Error': 'Could not add alert entry'}, 500


def valid_decimal(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True



@app.route("/test", methods=["POST"])
def testEmail():
    sendEmail("fabdullah230@gmail.com", "bitcoin", "12345.6")

    return {"status" : "Post request received"}, 200


def routineAlertCheck():
    priceTable = getTokensAndPrices()
    result = getAllAlerts()

    for item in result:
        if float(item[2]) - 0.1 * float(item[2]) <= float(priceTable[item[1]]) <= float(item[2]) + 0.1 * float(item[2]):
            #alert(item[0], item[1], item[2])
            print(f"we need to notify {item[0]}, his token {item[1]} is approaching his target value of {item[2]}")
            sendEmail(item[0], item[1], item[2])


with app.app_context():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=routineAlertCheck(), trigger="interval", seconds=60)
    scheduler.start()




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, threaded=True)


