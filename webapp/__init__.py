from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Youtube to RSS"


if __name__ == '__main__':
    app.run(debug=True)
