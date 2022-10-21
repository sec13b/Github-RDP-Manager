from ngrok import Client
from datetime import datetime
import requests
from mechanize import Browser
from flask import Flask, request, render_template, flash, redirect

username='runneradmin'
password='Windows@10'

def check_repo():
	resp=requests.get(f'https://github.com/{owner}/{repo}/')
	if resp.status_code==200:
		return True
	return False

def get_hosted_time(date):
	time=datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
	timenow=datetime.utcnow()
	diff=timenow-time
	return f"{diff.seconds // 3600}h {diff.seconds // 60 % 60}m ago"

def get_tunnels():
	client=Client('2GNy4cnxtLwEwhq8tcY39VyAoNr_7o4cE6k6SXZv9Bdgzy9n1')
	tunnels={}
	for t in client.tunnels.list():
		if t.proto=='tcp':
			tunnels[t.public_url.replace('tcp://','')]=get_hosted_time(t.started_at)
	return tunnels

def run_workflow():
	cookie="_device_id=9886c6859f4634d8201bc2fe6d442596; _octo=GH1.1.48487309.1666349759; logged_in=yes; _gh_sess=zunh%2B0pBPZclJxNOqeM3iSXskGaCK0fTbS8QTG9ZwbxaXSe%2BBcReRgBpuL6bQ4C8BJXRslg4BbHmosec71SwTzbMRYvyNGO%2BtAP2K57hjhqOsic5CNZEdW6i6CugBz0aEfVXj5wuaCwDmi0yGeENRWEuI8oVD9q12o%2B6Zxgbez2J0Y6jrcirQPoLnfcB%2FGEJTe0b0yrEcVHfJyPfw7e72BAkBIxA%2F1cDKWWCmSEY1GdZ%2BunUPOKxaYmsHASc9Woza9wAXOv%2BQ0k%2FFxmmIK9H15hjZ9MWWe80p7Ue774t86BcnJ1KY8Scjjdop25nul9%2FB4WcIF%2FYVtODPmbAkWVXxF2GpT0H%2BbvrMVAXRVB2PGrn4Lgdk7Zu49w176d6RJR%2Bpr6qoTJLwlrfSVKPV3jJYvnA5xaZW1xg61bzmgHwBk8zGGPav7PCuyVEunRUkDHacxnY2kio28Qc3015u2zohbMFFZbR1v3uITOCIvzr9%2Fh1F5Mes3EO2vl4hgqYOmQKSetY3%2BZlOUP32RORoqaJjNW4d2NhzyGWg7tKVSBwOFnnLKcoYt3f5vMG%2BZeqq%2BMHdaVHK7pMVvm%2BuF9sY4VziLQ09w%2F8C%2BTV4OQnQUJVMSkhs9onJYquxjXcQhkGeYYoNJz54ZNMQNadMvT97Q1N3N4U3zljtYtc5EFjMuLm%2B3E13lt5lPHqGYteG%2FuEOlm0fudwllhtG4d7UY60r4oe%2FrmncEwXUDYTzsC8b%2FYygQ56l%2BbHitp9TT7uxUYR6RsbFu4pB0LOX%2BdMDYphjIUPitiTwM2KtUjbHXbwxZ9wXLAWs0Y3A8o7aUq7sAshwLyeknS0RFxsAt0abYzd3qsdKhXazeI6Y9JsBF%2FQwmOZCh%2B9sUpI%2FNeS41%2FWZAw4T9s88Lxmuw%3D%3D--NgZEVESeCMuY8VgV--sFFv1HzMzr7xmufZvOvMjQ%3D%3D; preferred_color_mode=dark; tz=Asia%2FDhaka; has_recent_activity=1; user_session=77xBiDHcc_1OK6hJQAGFwMAIiu1De1LStiK74uPtiJN8wHkg; __Host-user_session_same_site=77xBiDHcc_1OK6hJQAGFwMAIiu1De1LStiK74uPtiJN8wHkg; tz=Asia%2FDhaka; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; dotcom_user=jannatulsifa"

	br=Browser()
	br.set_handle_robots(False)
	br.set_header('Cookie', cookie)
	br.open('https://github.com/jannatulsifa/test-python/actions/manual?workflow=.github%2Fworkflows%2Freverse_rdp.yml')

	br.select_form(nr=1)
	try:
		br.submit()
	except:
		pass


app=Flask(__name__)
app.config['SECRET_KEY']='thisismysecretkey'

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method=="POST":
		run_workflow()
		flash('A RDP is being triggered. Please wait a few moments!', 'success')
		return redirect('/')

	return render_template('index.html', tunnels=get_tunnels(), username=username, password=password)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)

