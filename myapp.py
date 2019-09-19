"""Basic start with Flask
"""
from flask import Flask, render_template

# create flask webserver
app = Flask(__name__)  # __name__ pulls name of file

# route tells it where to go (determines location)


@app.route("/")
# define a function to tell it what to do at that route
def home():
    return render_template('home.html')

# create another route
@app.route("/about")
# define function for this route
def pred():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)

# can also run using FLASH_APP=myapp.py flask run
