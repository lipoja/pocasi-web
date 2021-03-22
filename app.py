import datetime

from database import Weather, db, app
from flask import Flask, render_template, request, abort, jsonify


@app.route('/add', methods=['GET'])
def add():
    if 'temp' not in request.args:
        abort(400, {"status": "error"})

    temp = request.args.get('temp')
    weather = Weather(temperature=temp)

    db.session.add(weather)
    db.session.commit()

    return jsonify({"status": "added"})


@app.route('/nibeuplink', methods=['GET'])
def nibeuplink():
    ret = ''
    if 'code' not in request.args:
        abort(400, "Parameter 'code' not found<br>")
        ret += "Parameter 'code' not found<br>"
    else:
        code = request.args['code']
        ret += f"Parameter 'code' found, value is: {code}<br>"

    if 'state' not in request.args:
        abort(400, "Parameter 'state' not found<br>")
        ret += "Parameter 'state' not found<br>"
    else:
        state = request.args['state']
        ret += f"Parameter 'state' found, value is: {state}<br>"

    if 'error' in request.args:
        ret += f"{request.args['error']}"

    return ret


@app.route('/')
def home():
    tmp = Weather.query.order_by(Weather.time.desc()).first()
    if tmp is None:
        return render_template("temperature.html", teperature=999,
                               time=datetime.datetime.now(),
                               temp_data='')
    since = datetime.datetime.now() - datetime.timedelta(hours=12)
    half_day = Weather.query.filter(Weather.time > since).order_by(Weather.time.desc()).all()

    hd_data = []
    for data in half_day:
        hd_data.append(f'[new Date("{data.time}"), {data.temperature}]')

    return render_template("temperature.html",
                           temperature=round(tmp.temperature, 1), time=tmp.time,
                           temp_data=','.join(hd_data))


@app.cli.command('initdb')
def initdb_command():
    db.create_all()
    print("Database initialized")


if __name__ == '__main__':
    app.run()
