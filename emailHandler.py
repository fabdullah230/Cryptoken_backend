message =     htmlMessage = """<div style="background-color: #090942; width: 500px; height: 450px;">
<h1 style="color: white; text-align: center; padding-top: 10px;"><img style="width: 25px; margin-top: 10px;" src="https://github.com/fabdullah230/fabdullah230/blob/main/CrypToken_black.png?raw=true" /> CrypToken</h1>
<h2 style="color: white; font-size: 20px; text-align: center; margin-top: 50px;">Hello {email}!</h2>
<h3 style="color: white; font-size: 15px; text-align: center; margin-top: 50px; padding: 20px;">Your token of interest, {token} is approaching your target value of {price}</h3>
<h5 style="color: white; font-size: 12px; text-align: center; margin-top: 100px; padding: 20px;">Click <a href="https://cryptoken.netlify.app/" style="color:#f0be37">here</a> to visit site</h5>
</div>""".format(email="email", token="token", price="price")


print(message)