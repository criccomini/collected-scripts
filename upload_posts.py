import httplib
import json
import os

with open('rendered/power_lifting_log.md') as f:
	token = os.environ['COLLECTED_NOTES_API_TOKEN']
	email = os.environ['COLLECTED_NOTES_API_EMAIL']
	conn = httplib.HTTPSConnection("collectednotes.com")
	headers = {
		'Authorization': '{} {}'.format(email, token),
		'Accept': 'application/json',
		'Content-Type': 'application/json',
	}
	json_dict = {
		"note": 
		{
			"body": f.read(), 
			"visibility": "public_site"
		}
	}
	conn.request("PUT", "/sites/2/notes/3543", json.dumps(json_dict), headers)
	r1 = conn.getresponse()
	print r1.status, r1.reason
