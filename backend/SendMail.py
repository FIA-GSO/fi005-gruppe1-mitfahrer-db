import requests
import json

api_key = "52be6c0603447dfcb77010303e7c5875-2de3d545-6fe61ce2"
template_info_getter = {
    "bestaetigungsmail": {"subject": "Bitte bestätigen Sie Ihre E-Mail-Adresse"},
    "passwortvergessen": {"subject": "Passwort vergessen?"},
    "verspaetung": {"subject": "Verspätung für deine Fahrt gemeldet"},
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
