import requests
import base64
import json
import traceback
from docopt import docopt
from prettytable import PrettyTable

requests.packages.urllib3.disable_warnings()

def get_args():
    """
    Define and parse command-line arguments.
    """
    usage = """
    Usage:
        netapp_SVM.py -s <STORAGE> -VM <SVM> --create
        netapp_SVM.py -s <STORAGE> -VM <SVM> --remove
        netapp_SVM.py -s <STORAGE> -VM <SVM> --details
        netapp_SVM.py --version
        netapp_SVM.py -h | --help

    Options:
        -h --help            Show this message and exit
        
    """
    return docopt(usage)

def get_headers():
    """
    Generate authorization headers for the API requests.
    """
    username = "admin"
    password = "netapp1234"
    encoded_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

def handle_request_errors(func):
    """
    Decorator to handle request and other exceptions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException:
            print('Cannot connect to the storage!')
        except json.decoder.JSONDecodeError:
            print('Failed to parse the server response!')
        except Exception as e:
            print(f"Error: {str(e)}")
    return wrapper

@handle_request_errors
def get_svm(svm_name, storage):
    """
    Retrieve SVM details.
    """
    url = f'https://{storage}/api/svm/svms?name={svm_name}'
    headers = get_headers()
    
    r = requests.get(url, verify=False, headers=headers)
    d = r.json()
    svm_url = f"https://{storage}{d['records'][0]['_links']['self']['href']}"
    
    req = requests.get(svm_url, verify=False, headers=headers)
    return req.json()

@handle_request_errors
def check_svm_exists(svm_name, storage):
    """
    Check if the SVM exists on the storage.
    """
    url = f'https://{storage}/api/svm/svms'
    headers = get_headers()

    r = requests.get(url, verify=False, headers=headers)
    svms = [svm['name'] for svm in r.json()['records']]

    if svm_name in svms:
        print(f'The SVM named {svm_name} is already running!')
        return True
    return False

@handle_request_errors
def create_svm(svm_name, storage):
    """
    Create a new SVM on the storage.
    """
    if check_svm_exists(svm_name, storage):
        return
    
    data = {
        "name": svm_name,
        "snapshot_policy": {"name": "default"}
    }
    url = f'https://{storage}/api/svm/svms'
    headers = get_headers()

    if svm_name.isalnum():
        r = requests.post(url, json=data, verify=False, headers=headers)
        job_url = f"https://{storage}{r.json()['job']['_links']['self']['href']}"
        
        t = PrettyTable(field_names=['SVM', 'Status', 'Details'])
        job_resp = requests.get(job_url, verify=False, headers=headers).json()

        t.add_row([svm_name, job_resp['state'], job_resp['start_time']])
        print(t)
    else:
        print('Invalid SVM name!')

@handle_request_errors
def delete_svm(svm_name, storage):
    """
    Delete an SVM from the storage.
    """
    svm_data = get_svm(svm_name, storage)
    if not svm_data:
        return
    
    uuid = svm_data['uuid']
    url = f'https://{storage}/api/svm/svms/{uuid}'
    headers = get_headers()
    
    r = requests.delete(url, verify=False, headers=headers)
    job_url = f"https://{storage}{r.json()['job']['_links']['self']['href']}"
    
    t = PrettyTable(field_names=['SVM Name', 'State', 'Details', 'Message'])
    job_resp = requests.get(job_url, verify=False, headers=headers).json()

    t.add_row([svm_name, job_resp['state'], job_resp['description'], job_resp['message']])
    print(t)

@handle_request_errors
def show_svm_details(svm_name, storage):
    """
    Display details of a specific SVM.
    """
    svm_data = get_svm(svm_name, storage)
    if svm_data:
        print(json.dumps(svm_data, indent=2))

def main(args):
    storage = args['<STORAGE>']
    svm_name = args['<SVM>']

    if args['--create']:
        create_svm(svm_name, storage)
    elif args['--remove']:
        delete_svm(svm_name, storage)
    elif args['--details']:
        show_svm_details(svm_name, storage)

if __name__ == '__main__':
    try:
        ARGS = get_args()
        main(ARGS)
    except KeyboardInterrupt:
        print('\nReceived Ctrl^C. Exiting...')
    except Exception:
        print(traceback.format_exc())
