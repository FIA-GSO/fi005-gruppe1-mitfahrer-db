import requests

api_key = "52be6c0603447dfcb77010303e7c5875-2de3d545-6fe61ce2"

def send_registry_mail(to, registry_link):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "GSO Mitfahrer-Datenbank <mailgun@sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org>",
            "to": [to],
            "subject": "Bitte bestätigen Sie Ihre E-Mail-Adresse",
            "template": "bestaetigungsmail",
            "h:X-Mailgun-Variables": """{"test": "%s"}""" % registry_link})


def send_new_password_mail(to, new_password_link):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "GSO Mitfahrer-Datenbank <mailgun@sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org>",
            "to": [to],
            "subject": "Passwort vergessen?",
            "template": "passwortvergessen",
            "h:X-Mailgun-Variables": """{"link": "%s"}""" % new_password_link})


def send_delay_mail(to, date_time_of_ride, delay):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "GSO Mitfahrer-Datenbank <mailgun@sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org>",
            "to": [to],
            "subject": "Verspätung für deine Fahrt gemeldet",
            "template": "verspaetung",
            "h:X-Mailgun-Variables": '{"datum_fahrt":"%s", "verspaetung":"%s"}' % (date_time_of_ride, delay)})
