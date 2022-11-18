import requests
import json
import os

api_key = os.getenv("MAILGUN_API_KEY")
template_info_getter = {
    "bestaetigungsmail": {"subject": "Bitte bestätigen Sie Ihre E-Mail-Adresse"},
    "passwortvergessen": {"subject": "Passwort vergessen?"},
    "verspaetung": {"subject": "Verspätung für deine Fahrt gemeldet"},
    "new_reservation": {"subject": "Neue Reservierung für deine Fahrt"},
    "canceled_reservation": {
        "subject": "Eine reservierte Mitfahrt bei deiner Fahrt wurde storniert"
    },
    "user_canceled_ride": {"subject": "Eine von Dir reservierte Fahrt wurde storniert"},
}


def should_send_mail(email):
    return email.endswith("@gso.schule.koeln")


def send_mail_from_template(template, to, **template_variables):
    """available templates and their template variables:
    bestaetigungsmail : link
    passwortvergessen : link
    verspaetung : date_time, delay
    new_reservation : date_time, link_to_details
    canceled_reservation : date_time, link_to_details
    user_canceled_ride : date_time"""

    if not should_send_mail(to):
        print("Skipping mail send", template, to, template_variables)
        return {"skipped": "true"}

    current_template = template_info_getter[template]
    mailgun_request = requests.post(
        "https://api.mailgun.net/v3/sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org/messages",
        auth=("api", api_key),
        data={
            "from": "GSO Mitfahrer-Datenbank <mailgun@sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org>",
            "to": [to],
            "subject": current_template["subject"],
            "template": template,
            "h:X-Mailgun-Variables": json.dumps(template_variables),
        },
    )

    print("Send Mail Response", mailgun_request, mailgun_request.text)

    return mailgun_request
