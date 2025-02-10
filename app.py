from flask import Flask, render_template

app = Flask(__name__)

@app.route('/chat')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    pass
# must add generative logic

if __name__ == '__main__':
    app.run(debug=True)