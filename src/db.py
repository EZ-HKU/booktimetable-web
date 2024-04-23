import pymongo

from ABconfig import *
from req import if_correct

import datetime
import os

MONGO_LINK = os.environ.get('MONGO_LINK')

db = pymongo.MongoClient(MONGO_LINK).booking

users = db.user
log = db.log

if DEBUG and len(list(users.find({}))) == 0:
    users.insert_one({'id': 'admin', 'pw': '123456', 'name': 'admin'})

def add_user(id, pw, name):
    user = {
        'id': id,
        'pw': pw,
        'name': name
    }
    idd = users.find({'$or': [{'id': user['id']}, {'name': user['name']}]})
    if len(list(idd)) == 0:
        if if_correct(user):
            
            users.insert_one(user)
            return 'success'
        else:
            return 'invalid'
    else:
        return 'repeat'


def add_task(date, times, room, username, state='prebooked', book_date=None):
    # check if the task is already in the database
    for time in times:
        if log.find_one({'date': date, 'times': time, 'username': username}) is not None:
            return 'task already exists'
    
    ts = log.find({'date': date, 'username': username, 'room': room[-2]})
    total = 0
    for t in ts:
        total += len(t['times'])
    lenlimit = LENLIMIT[room[-2]]
    if total >= lenlimit:
        return 'too many tasks'
    
    task = {
        'date': date,
        'times': times,
        'room': room,
        'username': username,
        'state': state,
        'book_date': book_date
    }
    log.insert_one(task)
    return 'success'


def change_state(task, state):
    condition = {'_id': task['_id']}
    task['state'] = state
    log.update_one(condition, {'$set': task})


def change_message(user, message):
    condition = {'id': user}
    users.update_one(condition, {'$set': {'messages': message}})


def data2time(date):
    return f'{date[0:2]}:{date[2:4]}-{date[4:6]}:{date[6:8]}'


def time2data(date):
    return f'{date[0:2]}{date[3:5]}{date[6:8]}{date[9:]}'


def find_by_date(date):
    dic = [[dic['date'], [data2time(timedata) for timedata in dic['times']], dic['room'][-1],
            dic['username'], dic['state']] for dic in log.find({'date': date})]
    return dic


def get_users():
    userlist = users.find({})
    usernamelist = [user['name'] for user in userlist]
    return usernamelist


def from_task(task):
    user = users.find_one({'name': task['username']})
    return user, task

def check_user(id, pw):
    user = users.find_one({'id': id})
    if user is None:
        return False
    else:
        return user['pw'] == pw

def cancel_prebook(id, date, time):
    name = users.find_one({'id': id})['name']
    task = log.find_one({'date': date, 'times': time, 'username': name})
    if task is None:
        return False
    else:
        log.delete_one(task)
        return True

def find_by_user(id, ahead=7):
    tasks = log.find({
        'room': 'Discussion Room',
        '$or': [{'date': (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d") } for i in range(ahead)]
    })
    return tasks

def find_by_room(room, ahead=7):
    tasks = log.find({
        'room': room,
        '$or': [{'date': (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d") } for i in range(ahead)]
    })
    return tasks

def get_ahead(ahead=7):
    tasks = log.find({
        '$or': [{'date': (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d") } for i in range(ahead)]
    })
    return tasks


def check_format(l):
    text = ''
    if len(l) == 0:
        text += 'Uhh, you do not book any facility🤔\n'
    else:
        text += 'OK, Let me check...🧐\n\n'
        for i in range(len(l)):
            if len(l[i][1]) == 1:
                text += 'User: ' + l[i][3] + '\n' + 'Type: ' + l[i][2] + '\n' + 'Date: ' + l[i][0] + '\n' + 'Time: ' + \
                                l[i][1][0] + '\n' + ('Status:  ⚠️' if l[i][4] != 'booked' else 'Status:  ✅') + l[i][4] + '\n\n'

            elif l[i][1][0].split('-')[1] == l[i][1][1].split('-')[0]: 
                text += 'User: ' + l[i][3] + '\n' + 'Type: ' + l[i][2] + '\n' + 'Date: ' + l[i][0] + '\n' + 'Time: ' + \
                                l[i][1][0].split('-')[0] + '-' + l[i][1][1].split('-')[1] + '\n' + ('Status:  ⚠️' if l[i][4] != 'booked' else 'Status:  ✅') + \
                                l[i][4] + '\n\n'
            else: 
                text += 'User: ' + l[i][3] + '\n' + 'Type: ' + l[i][2] + '\n' + 'Date: ' + l[i][0] + '\n' + 'Time1: ' + \
                                l[i][1][0] + '\n' + 'Time2: ' + l[i][1][1] + '\n' + ('Status:  ⚠️' if l[i][4] != 'booked' else 'Status:  ✅') + l[i][4] + '\n\n'
    return text





if __name__ == "__main__":
    add_task('2023-03-11', ['01000130', '01300200'], ['Study Room', 'Study Room 7'], 'zzl')
