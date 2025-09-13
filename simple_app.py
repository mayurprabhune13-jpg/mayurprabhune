from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <h1>Hello from Railway!</h1>
    <p>This is a simple Flask test application.</p>
    <p>If you can see this, Railway is working.</p>
    <p>Domain: mayurprabhune.in</p>
    '''

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Simple app is running'}

if __name__ == '__main__':
    app.run(debug=True)