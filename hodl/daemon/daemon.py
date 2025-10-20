from flask import Flask

version = "0.1"
app = Flask(__name__)


class Sender:
    pass


@app.route('/status')
def status():
    return f'HDN is available. Version of daemon: {version}'


if __name__ == '__main__':
    app.run(port=7979)
