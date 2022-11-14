from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = True
    init_app(app)
    return app

def init_app(app):
    @app.route('/')
    def hello_world():
        return 'Hello World', 200

if __name__ == "__main__":
    app = create_app()
    app.run()