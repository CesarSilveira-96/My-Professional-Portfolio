from flask import render_template, Flask


app = Flask(__name__)
print(app.name)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pt-br")
def home_pt():
    return render_template("index_pt.html")

if __name__ == "__main__":
    app.run(debug=True)