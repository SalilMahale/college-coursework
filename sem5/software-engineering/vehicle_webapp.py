from flask import Flask, render_template_string, request

app = Flask(__name__)

VEHICLE_AVAILABLE = True
BOOKED = False

HTML = '''
<!doctype html>
<html lang="en">
<head>
  <title>Vehicle Management System</title>
  <style>
    body {
      background: #f7f7f7;
      font-family: 'Segoe UI', Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      min-height: 100vh;
      margin: 0;
      padding: 40px 0;
    }
    .main-card {
      background: #fff;
      border-radius: 16px;
      padding: 32px 40px;
      box-shadow: 0 4px 16px rgba(60,60,60,0.12);
      width: 370px;
      margin-top: 30px;
      text-align: center;
    }
    h1 {
      font-size: 2em;
      color: #1b2430;
      margin-bottom: 16px;
      letter-spacing: 1px;
    }
    #msg {
      margin-bottom: 22px;
      color: #228b22;
      font-weight: bold;
    }
    form {
      margin-bottom: 18px;
      padding: 18px 0;
      border-top: 1px solid #e0e0ee;
    }
    label {
      display: block;
      margin-bottom: 7px;
      font-weight: 500;
      text-align: left;
    }
    input {
      width: 90%;
      padding: 7px 9px;
      border: 1px solid #ccc;
      border-radius: 7px;
      margin-bottom: 13px;
      font-size: 1em;
      background: #fbfbfb;
    }
    button {
      padding: 7px 22px;
      border-radius: 6px;
      background: #2d6cdf;
      color: #fff;
      font-weight: bold;
      font-size: 1em;
      border: none;
      margin-top: 4px;
      cursor: pointer;
      transition: background 0.2s;
    }
    button:hover {
      background: #174ea6;
    }
    .logo-img {
      max-width: 80px;
      margin: 0 auto 15px auto;
      display: block;
      border-radius: 7px;
    }
  </style>
</head>
<body>
  <div class="main-card">
    <!-- Optional: Place your logo or vehicle image here -->
    <!-- <img src="YOUR_IMAGE_URL" class="logo-img" alt="Logo"/> -->
    <h1>Vehicle Management System</h1>
    {% if msg %}
      <div id="msg">{{ msg }}</div>
    {% endif %}
    <form method="post" action="/">
      <label for="vehicle_id_1">Vehicle ID:</label>
      <input name="vehicle_id" id="vehicle_id_1" value="1" required>
      <label for="user_id">User ID:</label>
      <input name="user_id" id="user_id" value="101" required>
      <button name="action" value="book">Book</button>
    </form>
    <form method="post" action="/">
      <label for="vehicle_id_2">Vehicle ID:</label>
      <input name="vehicle_id" id="vehicle_id_2" value="1" required>
      <label for="amount">Amount:</label>
      <input name="amount" id="amount" value="500" required>
      <label for="method">Method:</label>
      <input name="method" id="method" value="cash" required>
      <button name="action" value="pay">Pay</button>
    </form>
  </div>
</body>
</html>'''

@app.route("/", methods=["GET", "POST"])
def index():
    global VEHICLE_AVAILABLE, BOOKED
    msg = ""
    if request.method == "POST":
        if request.form["action"] == "book":
            if VEHICLE_AVAILABLE:
                VEHICLE_AVAILABLE = False
                BOOKED = True
                msg = "Booking successful"
            else:
                msg = "Booking failed"
        elif request.form["action"] == "pay":
            if not BOOKED:
                msg = "Payment failed"
            elif request.form["method"] not in ("cash", "online"):
                msg = "Invalid payment method"
            else:
                msg = "Payment successful"
    return render_template_string(HTML, msg=msg)

if __name__ == "__main__":
    print("Visit http://127.0.0.1:5000 in browser")
    app.run(debug=True)
