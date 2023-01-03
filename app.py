from flask import Flask, render_template, request, flash
import gunicorn

app = Flask(__name__)
app.secret_key = "wastogi999"

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST", "GET"])
def dcf():
    while True:
        time = request.values.get('time')
        if time.isnumeric():
            time = int(time)
            if time > 0:
                break
        else:
            flash("Wrong Input")
            return render_template("index.html")

            
    fcf = float(request.values.get('fcf'))
    growthrate = float(request.values.get('growthrate'))
    discountrate = float(request.values.get('discountrate'))
    avg_fcf_multiple = float(request.values.get('avg_fcf_multiple'))

    year = 0
    discountedfcf = 0

    for i in range(time):
        year += 1
        fcf = fcf * growthrate
        discount = discountrate ** year
        final = fcf / discount
        discountedfcf += final

    terminal_value = (fcf * avg_fcf_multiple) / (discountrate ** year)
    intrinsic_value = terminal_value + discountedfcf

    shares = float(request.values.get('shares'))

    if shares < 1:
        intrinsic_value = intrinsic_value / shares

    
    flash(f"Intrinsic value: ${intrinsic_value}B")
    return render_template("index.html")


if __name__ == "__main__":
    gunicorn.run()
