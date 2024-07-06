from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'YouTubeToAudioPodcast'
    return render_template('login.html', page_title=title)


if __name__ == '__main__':
    app.run(debug=True)