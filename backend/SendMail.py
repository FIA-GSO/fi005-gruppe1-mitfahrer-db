import requests

api_key = "52be6c0603447dfcb77010303e7c5875-2de3d545-6fe61ce2"

def send_mail(subject, content):
 return requests.post(
		"https://api.mailgun.net/v3/sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org/messages",
		auth=("api", api_key),
		data={"from": "GSO Mitfahrer-Datenbank <mailgun@sandboxdddd85465af748c8b8ebdb9a4b3c0087.mailgun.org>",
			"to": ["tompatrick.g@gso.schule.koeln"],
			"subject": subject,
			"text": content})

# content = "Testing some Mailgun awesomness!"
# subject = "HelloMello"
# send_mail(subject, content)