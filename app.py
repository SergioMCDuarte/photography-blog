from main import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    app.add_url_rule('/favicon.ico',
                     redirect_to=url_for('static', filename='favicon.ico'))
