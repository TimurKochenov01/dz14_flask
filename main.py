from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

@app.route("/")
def index():
    all_notes = Notes.query.all()
    return render_template("index.html", notes=all_notes)

@app.route("/add", methods=["POST"])
def add_note():

    title = request.form["title"]
    text = request.form["text"]
    
    new_note = Notes(title=title, text=text)
    db.session.add(new_note)
    db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/notes")
def show_notes():
    all_notes = Notes.query.order_by(Notes.id.desc()).all()
    return render_template("notes.html", notes=all_notes)

@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    note = Notes.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("show_notes"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
