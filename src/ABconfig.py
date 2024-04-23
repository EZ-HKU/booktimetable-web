import os

# server
PW = os.environ.get('BOOK_PW')
AHEAD_DAYS = 4
TIME_LIST =  {
    "Discussion Room": [f'{(8300930+i*1000100):>0{8}}' for i in range(12)] + ['20302200'],
    # generate time list for single study room from 00:00-00:30, 00:30-01:00, ..., 23:30-24:00
    "Study Room": [f'{i//2:>0{2}}{"00" if i%2==0 else "30"}{i//2+i%2:>0{2}}{"00" if i%2!=0 else "30"}' for i in range(47)],
    "Concept and Creation Room": ["08301300", "13001800", "18002200"]
    }

DEBUG = os.environ.get('BOOKING_DEBUG').lower() == 'true'
PORT = 8080


def DISCUSSION_ROOM(room):
    return int(room.split(' ')[-1]) + 125

FACILITY = {'Discussion Room': DISCUSSION_ROOM}
FTYPE = {'Discussion Room': '21', 'Single Study Room (3 sessions)': '31'}
LIBRARY = {'Main Library': '3'}
FLOOR = {'Level 3': '3', '4/F': '4'}

PREFER_ROOM = ['11', '8', '1', '18', '17', '19']
LOGIN_URL = 'https://booking.lib.hku.hk/Secure/FacilityStatusDate.aspx'
BOOK_URL = 'https://booking.lib.hku.hk/Secure/NewBooking.aspx'
STATUS_URL = 'https://booking.lib.hku.hk/Secure/MyBookingRecordM.aspx'


ALL_ROOMS = [f'Discussion Room {i}' for i in range(1, 20)]+ [f'Study Room {i}' for i in range(1, 11)] + [f'Concept and Creation Room {i}' for i in range(1, 6)]

LENLIMIT ={
    'Discussion Room': 2,
    'Study Room': 4,
    'Concept and Creation Room': 1
}