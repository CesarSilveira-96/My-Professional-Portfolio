from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap5 import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired, InputRequired
from datetime import datetime
import os



hours = [f"{hour}:00" for hour in range(0, 24)]

# cafes_data = pandas.read_csv('cafe-data.csv')

app = Flask(__name__, instance_path=os.path.join(os.path.dirname(__file__), 'instance'))
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap(app)

# CREATE DB
class Base(DeclarativeBase):
  pass

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafe-and-wifi.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cafe_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String,nullable=False)
    review: Mapped[str] = mapped_column(String(1000), nullable=True)
    coffee_rating: Mapped[str] = mapped_column(String(30), nullable=False)
    open_time: Mapped[str] = mapped_column(String(20), nullable=False)
    closing_time: Mapped[str] = mapped_column(String(20), nullable=False)
    wifi_rating: Mapped[str] = mapped_column(String(30), nullable=False)
    power_outlet_rating: Mapped[str] = mapped_column(String(30), nullable=False)
    final_rating: Mapped[str] = mapped_column(String(30), nullable=False)


with app.app_context():
    db.create_all()

class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location URL', validators=[DataRequired()])
    review = StringField('Write a review of this cafe', validators=[DataRequired()])
    open_time = SelectField('Open time', validators=[DataRequired()], choices=hours)
    closing_time = SelectField('Closing time', validators=[DataRequired()], choices=hours)
    coffee_rating = SelectField('Coffee rating', validators=[DataRequired()], 
                                choices=["-", "☕", " ☕ ☕", " ☕ ☕ ☕", " ☕ ☕ ☕ ☕", " ☕ ☕ ☕ ☕ ☕"])
    wifi_rating = SelectField('Wifi speed', validators=[DataRequired()], 
                              choices=["-", "🛜", "🛜🛜", "🛜🛜🛜", "🛜🛜🛜🛜", "🛜🛜🛜🛜🛜"])
    power_outlet_rating = SelectField("Power outlet", validators=[DataRequired()],
                        choices=["-", "⚡", "⚡⚡", "⚡⚡⚡", "⚡⚡⚡⚡", "⚡⚡⚡⚡⚡"])
    final_rating = HiddenField("Final Rating", validators=[InputRequired()])
    submit = SubmitField('Submit')


# all Flask routes below


@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

@app.route("/")
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.final_rating.desc()))
    top3_cafes = result.scalars().all()[:3]
    return render_template("index.html", cafes=top3_cafes)


@app.route('/add', methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        print("POST data:", request.form)
    if form.validate_on_submit():
        new_cafe_dict = {
        "cafe_name":form.cafe_name.data,
        "location":form.location.data,
        "review":form.review.data,
        "open_time":form.open_time.data,
        "closing_time":form.closing_time.data,
        "coffee_rating":form.coffee_rating.data,
        "wifi_rating":form.wifi_rating.data,
        "power_outlet_rating":form.power_outlet_rating.data,
        "final_rating":form.final_rating.data
        }

        existing_cafe = db.session.execute(db.select(Cafe).filter_by(cafe_name=form.cafe_name.data)).scalar()
        if existing_cafe:
            # Error Message
            return "This Cafe already exists!", 400
        
        new_cafe = Cafe(
            cafe_name=form.cafe_name.data.title(),
            location=form.location.data,
            review=form.review.data.capitalize(),
            open_time=form.open_time.data,
            closing_time=form.closing_time.data,
            coffee_rating=form.coffee_rating.data,
            wifi_rating=form.wifi_rating.data,
            power_outlet_rating=form.power_outlet_rating.data,
            final_rating=form.final_rating.data
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('all_cafes'))
    return render_template("add.html", form=form)


@app.route('/cafes')
def all_cafes():
    cafes_data = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    return render_template('cafes.html', cafes=cafes_data)


@app.route('/search')
def search():
    query = request.args.get("search-box", "").strip()
    
    if query:
        results = db.session.execute(
            db.select(Cafe).where(Cafe.cafe_name.ilike(f"%{query}%"))
        ).scalars().all()
    else:
        results = []

    return render_template("search.html", query=query, cafes=results)

if __name__ == '__main__':
    app.run(debug=True)

