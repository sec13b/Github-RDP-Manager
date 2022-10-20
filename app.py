from ngrok import Client
from datetime import datetime
import requests
from flask import Flask, request, render_template, flash, redirect

username='runneradmin'
password='Windows@10'
branch, owner, repo, workflow_name, ghp_token="main", "jannatulsifa", "test-python", "reverse_rdp.yml", "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"

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

def run_workflow(branch=branch, owner=owner, repo=repo, workflow_name=workflow_name, ghp_token=ghp_token):
	url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_name}/dispatches"
	
	headers = {
		"Accept": "application/vnd.github+json",
		"Authorization": f"Bearer {ghp_token}",
		"Content-Type": "application/json"
	}

	data = '{"ref":"'+branch+'"}'
	
	resp = requests.post(url, headers=headers, data=data)
	if resp.status_code==204:
		return True
	return resp.text

app=Flask(__name__)
app.config['SECRET_KEY']='thisismysecretkey'

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method=="POST":
		resp=run_workflow()
		if resp==True:
			flash('A RDP is being triggered. Please wait a few moments!', 'success')
		else:
			flash(f'Something went wrong! Error: {resp}', 'error')
		return redirect('/')

	return render_template('index.html', tunnels=get_tunnels(), username=username, password=password)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
