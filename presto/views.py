from presto import app


@app.route('/')
def index():
    return 'Hello World', 200
