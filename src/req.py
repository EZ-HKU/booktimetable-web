import requests
import re

import datetime
import threading


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.13",
    "Connection": "keep-alive",
}


class Booker:
    def __init__(self, user, task=None):
        self.user = user
        if 'push_type' in user.keys():
            self.push_type = user['push_type']
        else:
            self.push_type = None

        self.task = task

        self.session = None
        self.with_login = False

    def login(self):
        try:
            username = self.user['id']
            password = self.user['pw']
            s = requests.Session()
            s.headers.update(headers)
            r = s.get(
                "https://booking.lib.hku.hk/Secure/FacilityStatusDate.aspx", allow_redirects=False, verify=False)
            r = s.get(
                "https://lib.hku.hk/hkulauth/legacy/authMain?uri=https://booking.lib.hku.hk/getpatron.aspx")

            # handle SAML
            SCOPE = re.findall(r'scope = "(.*)"', r.text)[0]
            SAML_URL = re.findall(
                r'<script src="(https://ids.hku.hk/idp/profile/SAML2.*)"', r.text)[0]

            login_data = {"conversation": "e1s1",
                          "scope": SCOPE,
                          "userid": username,
                          "password": password,
                          "submit": "Submit"}

            r = s.get(SAML_URL, allow_redirects=False, verify=False)
            SSO_URL = "https://ids.hku.hk" + r.headers['Location']
            r = s.get(SSO_URL, allow_redirects=False)
            LOGIN_URL = "https://ids.hku.hk" + r.headers['Location']
            r = s.get(LOGIN_URL, allow_redirects=False)
            AuthnLib_URL = "https://ids.hku.hk/idp/" + r.headers['Location']
            r = s.get(AuthnLib_URL, allow_redirects=False)
            handleLogin_URL = r.headers['Location']
            r = s.get(handleLogin_URL, allow_redirects=False)
            
            r = s.post("https://ids.hku.hk/idp/ProcessAuthnLib",
                       data=login_data, allow_redirects=False)
            SSO_URL = "https://ids.hku.hk" + r.headers['Location']
            r = s.get(SSO_URL)
            SAML_RESPONSE = re.findall(
                r'<input type="hidden" name="SAMLResponse" value="(.*)"/>', r.text)[0]
            saml_data = {"SAMLResponse": SAML_RESPONSE,
                         "RelayState": SCOPE}
            r = s.post("https://lib.hku.hk/hkulauth/handleSAML",
                       data=saml_data, allow_redirects=False)

            getpatron_url = r.headers['Location']

            r = s.get(getpatron_url, allow_redirects=False)

            self.session = s
            self.with_login = True

            return True
        except:
            return False

    def get_url(self, url, with_login=None):
        if with_login is None:
            with_login = self.with_login
        if with_login:
            return self.session.get(url)
        else:
            if not self.login():
                # error
                return None
            return self.session.get(url)

    def book(self):
        url = self.task.make_book_url()
        r = self.get_url(url)

        if r is None:
            return False

        VIEWSTATE = re.findall(r'id="__VIEWSTATE" value="(.*)"', r.text)[0]
        VIEWSTATEGENERATOR = re.findall(
            r'id="__VIEWSTATEGENERATOR" value="(.*)"', r.text)[0]
        EVENTVALIDATION = re.findall(
            r'id="__EVENTVALIDATION" value="(.*)"', r.text)[0]

        MAIN_TOOLKIT = re.findall(
            r'id="main_ToolkitScriptManager1_HiddenField" value="(.*)"', r.text)[0]

        data = {
            "__VIEWSTATE": VIEWSTATE,
            "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
            "__EVENTVALIDATION": EVENTVALIDATION,
            "main_ToolkitScriptManager1_HiddenField": MAIN_TOOLKIT,
            "ctl00$main$ToolkitScriptManager1": f"ctl00$main$upMain|ctl00$main$btnSubmit",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "ctl00$main$ddlLibrary": self.task['Library'],
            "ctl00$main$ddlFloor": self.task['Floor'],
            "ctl00$main$ddlType": self.task['FacilityType'],
            "ctl00$main$ddlFacility": self.task['Facility'],
            "ctl00$main$ddlDate": self.task['date'],
            "ctl00$main$txtUserDescription": "",
            "ctl00$main$hBtnSubmit": "",
            "ctl00$main$hBtnEmail": "",
            "ctl00$main$txtEmail": "",
            "ctl00$main$hBtnResult": "",
            "__ASYNCPOST": "true",
            "ctl00$main$btnSubmit": "Submit"
        }
        

        for t, s in zip(self.task['times'], self.task.GetSessions()):
            data[f"ctl00$main$listSession${s}"] = t

        r = self.session.post(url, data=data, allow_redirects=False)

        data['ctl00$main$ToolkitScriptManager1'] = "ctl00$main$UpdatePanel3|ctl00$main$btnSubmitYes"
        data['ctl00$main$btnSubmitYes'] = "Yes"
        del data['ctl00$main$hBtnSubmit']

        r = self.session.post(url, data=data, allow_redirects=False)

        if 'Your Booking is successful' in r.text:
            return True
        else:
            return False


def if_correct(user):
    temp = Booker(user)
    return temp.login()


def book_timer(start_time: datetime.datetime, function, task=None):
    wait_time = start_time - datetime.datetime.now()
    if task is None:
        timer = threading.Timer(wait_time.total_seconds(), function)
    else:
        timer = threading.Timer(wait_time.total_seconds(), function, task)
    timer.start()


if __name__ == "__main__":
    user = {
        'id': '***REMOVED***',
        'pw': '***REMOVED***',
        'push_type': 'Telegram',
        'send_key': 'user_telegram_id'
    }
    room = ['Main Library', 'Level 3', 'Discussion Room', 'Discussion Room 1']
    date = '2023-02-19'
    times = ['09001000', '12001300']
    data = {'room': room, 'date': date, 'times': times}
    print(if_correct(user))
