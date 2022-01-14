from flask import Flask

from webapp.routes.sms import sms_route

app = Flask(__name__)
app.register_blueprint(sms_route)


@app.route('/', methods=['POST'])
def root():
    pass


if __name__ == '__main__':
    app.run(port=8080)
