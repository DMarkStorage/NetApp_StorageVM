import requests, base64
import json
import os
import traceback
from docopt import docopt
from prettytable import PrettyTable
requests.packages.urllib3.disable_warnings()



def get_args():

	usage = """
	Usage:
		netapp_SVM.py -s <STORAGE> -VM <SVM> --create
		netapp_SVM.py -s <STORAGE> -VM <SVM> --remove
		netapp_SVM.py -s <STORAGE> -VM <SVM> --details

		netapp_SVM.py --version
		netapp_SVM.py -h | --help

	Options:
		-h --help            Show this message and exit
		-s <STORAGE>         ZFS appliance/storage name

	"""
	# version = '{} VER: {} REV: {}'.format(__program__, __version__, __revision__)
	# args = docopt(usage, version=version)
	args = docopt(usage)
	return args	

def Headers():
	username = "admin"
	password = "netapp123"
	userpass = username + ':' + password
	encoded_u = base64.b64encode(userpass.encode()).decode()

	headers = {"Authorization" : "Basic %s" % encoded_u}

	return headers


def get_svm(svm, storage):

	url = 'https://'+storage
	headers = Headers()

	try:
		r = requests.get(url+'/api/svm/svms?name='+svm,
						 verify=False, headers = headers)
		status = r.status_code

		resp={}
		vm=[]
		d = r.json()
		uu = d['records'][0]['_links']['self']['href']
		url1 = 'https://'+storage+ uu
		req = requests.get(url1,verify=False, headers = headers)
		data1 = req.json()
		resp.update(data1)

		return resp
		
	except requests.exceptions.ConnectionError as err:
		print('Cant connect to the storage!')
		quit()

	except IndexError as err:
		print('SVM not found!')
		quit()
	except json.decoder.JSONDecodeError as err:
		print('Cant connect to the storage!')
		quit()
	except requests.exceptions.HTTPError as err:
		print('Cant connect to the storage!')
		quit()
	except requests.exceptions.RequestException as err:
		print('Cant connect to the storage!')
		quit()
	except Exception as e:
		raise e
		quit()


def check_svm(svm, storage):

	url = 'https://'+storage
	headers = Headers()

	vm_name = {}
	try:
		r = requests.get(url+'/api/svm/svms',
		verify=False, headers = headers)
		data = r.json()
		vm_name.update(data)

		vm=[]

		for i in vm_name['records']:
			vm.append(i['name'])

		if svm in vm:
			print('The VM named '+svm+' is already running!')
			quit()
		else:
			pass
	except requests.exceptions.ConnectionError as err:
		print('Cant connect to the storage!')
		quit()

	except json.decoder.JSONDecodeError as err:
		print('Cant connect to the storage!')
		quit()

	except requests.exceptions.HTTPError as err:
		print('Cant connect to the storage!')
		quit()

	except requests.exceptions.RequestException as err:
		print('Cant connect to the storage!')
		quit()
		
	except Exception as e:
		raise e
		quit()



def	create_svm(svm,storage):

	check_svm(svm, storage)
	data = {
		"name" : svm,
		"snapshot_policy" :{
				'name':'default'
		},
	}

	data_ = json.dumps(data)
	url = 'https://'+storage
	headers = Headers()
	try:
		if svm.isalnum():
			t = PrettyTable()
			r = requests.post(url+'/api/svm/svms', data = data_,
							 verify=False, headers = headers)

			status = r.status_code

			# try:
			print('-'*50)
			resp={}
			d = r.json()
			url1 = 'https://'+storage+ d['job']['_links']['self']['href']
			req = requests.get(url1,verify=False, headers = headers)
			data1 = req.json()
			resp.update(data1)

			t.field_names = [
			'SVM',
			'Status',
			'Details'
			]

			t.add_row(
				[svm,
				resp['state'],
				resp['start_time'],
				]
				)
			print(t)


		else:
			print('SVM name is not valid!')

		
	except Exception as e:
		raise e
		quit()

def delete_svm(svm,storage):
	t = PrettyTable()

	data_svm = get_svm(svm,storage)
	uuid = data_svm['uuid']
	
	data = {
		"uuid" : uuid
	}

	data_ = json.dumps(data)
	url = 'https://'+storage
	headers = Headers()

	r = requests.delete(url+'/api/svm/svms', data = data_,
					 verify=False, headers = headers)

	status = r.status_code
	print(status)
	print(r.text)
	resp2={}
	print(resp2)

	d = r.json()
	url1 = 'https://'+storage+ d['job']['_links']['self']['href']
	newresp = requests.get(url1,verify=False, headers = headers)
	print(newresp.text)
	d = newresp.json()
	resp2.update(d)

	print(url1)
	print(resp2)

	t.field_names = [
			'SVM name',
			'State',
			'Details',
			'Mesage'
			]

	t.add_row(
			[
			svm,
			resp2['state'],
			resp2['description'],
			resp2['message'],
			]
		)
	print(t)


def details_svm(svm,storage):

	data = get_svm(svm,storage)
	print(json.dumps(data, indent = 2))



def main(args):
	storage = args['<STORAGE>']
	svm_name = args['<SVM>']


	if args['--create']:
		create_svm(svm_name,storage)

	elif args['--remove']:
		delete_svm(svm_name,storage)

	elif args['--details']:
		details_svm(svm_name,storage)

if __name__ == '__main__':
	try:
		ARGS = get_args()

		main(ARGS)
	except KeyboardInterrupt:
		print('\nReceived Ctrl^C. Exiting....')
	except Exception:
		ETRACE = traceback.format_exc()
		print(ETRACE)