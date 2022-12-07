from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth


app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

suap = oauth.remote_app(
    'suap',
    consumer_key="7F65kRtgwW2B6JJbXgSHnkAf75f9bHsmVbIOt1AO",
    consumer_secret="iDUTqLzNaW8E7uALJ5RuaHfv6zSoyxHCPrwhrY9jlFfPT7iTyNwqjgt6KZHLz7SiYX5IKRC06PtOwL92TSmHd4pQb34mgiEymQp1q0bblmRHhk423tKxojaWPZAeZw9C",
    base_url='https://suap.ifrn.edu.br/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://suap.ifrn.edu.br/o/token/',
    authorize_url='https://suap.ifrn.edu.br/o/authorize/'
)


@app.route('/')
def index():
    if 'suap_token' in session:
        me = suap.get('v2/minhas-informacoes/meus-dados')
        return render_template('user.html', user_data=me.data, foto=me.data['url_foto_150x200'])
    else:
        return render_template('index.html')


@app.route('/login')
def login():
    return suap.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('suap_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = suap.authorized_response()
    if resp is None or resp.get('access_token') is None:
       return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['suap_token'] = (resp['access_token'], '')
    return redirect(url_for('index')) 


@suap.tokengetter
def get_suap_oauth_token():
    return session.get('suap_token')

if __name__ == '__main__':
    app.run()