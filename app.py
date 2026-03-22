from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Constants
GAMMA = 1.4
R = 287
T0 = 288.15
P0 = 101325
L = 0.0065
g = 9.81

# ISA model
def isa_properties(h):
    if h < 11000:
        T = T0 - L * h
        P = P0 * (T / T0) ** (g / (R * L))
    else:
        T = 216.65
        P = 22632 * math.exp(-g * (h - 11000) / (R * T))
    
    rho = P / (R * T)
    return T, P, rho

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    velocity = ""
    altitude = ""

    if request.method == "POST":
        try:
            velocity = request.form["velocity"]
            altitude = request.form["altitude"]

            V = float(velocity)
            h = float(altitude)

            T, P, rho = isa_properties(h)

            a = math.sqrt(GAMMA * R * T)
            M = V / a

            # Flow regime
            if M < 0.8:
                regime = "Subsonic"
            elif M < 1.2:
                regime = "Transonic"
            else:
                regime = "Supersonic"

            result = {
                "T": round(T, 2),
                "P": round(P, 2),
                "rho": round(rho, 4),
                "a": round(a, 2),
                "M": round(M, 3),
                "regime": regime
            }

        except:
            result = {"error": "Invalid input!"}

    return render_template("index.html",
                           result=result,
                           velocity=velocity,
                           altitude=altitude)

if __name__ == "__main__":
    app.run(debug=True)