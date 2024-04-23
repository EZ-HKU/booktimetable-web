import db

from ABconfig import *
from flask import Flask, request, render_template, redirect, url_for
import datetime

from flask_login import UserMixin, LoginManager, login_required, login_user, current_user


app = Flask(__name__)

app.secret_key = PW


# 1、实例化登录管理对象
login_manager = LoginManager()

# 参数配置
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'

login_manager.init_app(app)


class User(UserMixin):
    def __init__(self):
        super().__init__()
        self.gpt = None


# 3、加载用户, login_required 需要查询用户信息
@login_manager.user_loader
def user_loader(user_id):
    if db.users.find_one({'id': user_id}) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user


@app.route('/posttest', methods=['POST'])
@login_required
def post():
    if request.method == 'POST':
        temp = str(request.get_data())[2:-1]
        temp = temp.split(',')
        times = list(map(db.time2data, temp[2].split('.')))
        task = [temp[1], times, ['Main Library', 'Level 3',
                                 'Discussion Room', 'Discussion Room ' + temp[0]], temp[3]]
        db.add_task(*task)
        return 'success'


@app.route('/postuser', methods=['POST'])
@login_required
def postu():
    if request.method == 'POST':
        temp = str(request.get_data())[2:-1]
        temp = temp.split(',')
        user = {'id': temp[0], 'pw': temp[1], 'name': temp[2]}
        return db.add_user(user['id'], user['pw'], user['name'])


@app.route('/getusers', methods=['GET'])
@login_required
def get():
    if request.method == 'GET':
        return ','.join(db.get_users())


@app.route('/check', methods=['GET'])
@login_required
def check():
    date = datetime.datetime.now()
    l = []
    for i in range(3):
        l.extend(db.find_by_date(
            (date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")))
    if request.method == 'GET':
        return db.check_format(l)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        idd = request.form['id']
        pw = request.form['pw']
        if db.check_user(idd, pw):
            curr_user = User()
            curr_user.id = idd

            login_user(curr_user, remember=True,
                       duration=datetime.timedelta(days=365))
            return redirect(url_for('index'))
        else:
            return render_template('login.html', result='Wrong ID or Password! Please try again.')


@app.route('/regist', methods=['POST'])
def regist():
    user = {'id': request.form['id'],
            'pw': request.form['pw'], 'name': request.form['name']}
    r = db.add_user(user['id'], user['pw'], user['name'])
    if r == 'success':
        return render_template('login.html', result='Success! Please login.')
    elif r == 'repeat':
        return render_template('login.html', result='Repeat ID or Name! Please try again.')
    elif r == 'invalid':
        return render_template('login.html', result='Wrong ID or Password! Please try again.')
    else:
        return render_template('login.html', result='Unknown Error! Please try again.')


@app.route('/cancel_prebook', methods=['POST'])
@login_required
def cancel_prebook():
    idd = int(request.form['id'])
    roomm = request.form['room']
    roomtype = ' '.join(roomm.split(' ')[:-1])
    time = idd // 7
    date = datetime.datetime.now() + datetime.timedelta(days=idd % 7)
    date = date.strftime("%Y-%m-%d")
    time = TIME_LIST[roomtype][time]
    if db.cancel_prebook(str(current_user.id), date, time, roomm):
        return 'success'
    else:
        return 'fail to cancel prebook'


@app.route('/add_task_by_id', methods=['POST'])
@login_required
def add_task_by_id():
    idd = int(request.form['id'])
    roomm = request.form['room']
    roomtype = ' '.join(roomm.split(' ')[:-1])
    time = idd // 7
    date = datetime.datetime.now() + datetime.timedelta(days=idd % 7)
    date = date.strftime("%Y-%m-%d")
    time = TIME_LIST[roomtype][time]
    name = db.users.find_one({'id': str(current_user.id)})['name']
    task = [date, [time], [roomtype, roomm], name]
    return db.add_task(*task)


@app.route('/timetable/<room>', methods=['GET'])
@login_required
def timetable(room):
    if room not in ALL_ROOMS:
        return redirect(url_for('index'))

    roomtype = ' '.join(room.split(' ')[:-1])

    tasks = [{'state': "", 'color': "accent-white-gradient"}
             for i in range(len(TIME_LIST[roomtype]) * 7)]

    usertask = db.find_by_room(room)

    today = datetime.datetime.strptime(
        datetime.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    for task in usertask:
        date = datetime.datetime.strptime(task['date'], "%Y-%m-%d")
        for time in task['times']:
            if task['state'] == 'booked':
                color = 'accent-blue-gradient'
            elif task['state'] == 'prebooked':
                color = 'accent-orange-gradient'
            elif task['state'] == 'failed':
                color = 'accent-red-gradient'
            else:
                continue

            tasks[(date - today).days + TIME_LIST[roomtype].index(time)
                  * 7] = {'state': task['username'], 'color': color}

    times = list(map(db.data2time, TIME_LIST[roomtype]))
    dates = [(datetime.datetime.now() + datetime.timedelta(days=i)
              ).strftime("%Y-%m-%d") for i in range(7)]

    name = db.users.find_one({'id': str(current_user.id)})['name']

    return render_template('timetable.html',
                           times=times,
                           dates=dates,
                           tasks=tasks,
                           room=room,
                           name=name,
                           timelen=len(TIME_LIST[roomtype]),)


@app.route('/')
@login_required
def index():
    return render_template('index.html')


if __name__ == '__main__':

    # name = os.environ.get('PREBOOK_WEB_NAME')
    app.run(
        host='0.0.0.0',
        port=PORT,
        threaded=True,
        debug=DEBUG,
    )

