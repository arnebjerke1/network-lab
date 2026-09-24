import json
import requests
import os
import time
good_resp_codes = [ 200, 201 ]


def login_checkpoint(host,domain,username,password):
    url = "https://"+ host +"/web_api/login"
    headers = {"Content-Type": "application/json"}
    body = {
             "user" : username,
             "password" : password,
             "session-timeout" : 1800,
             "domain" : domain
           }
    req = requests.post(url, json=body, headers=headers, verify = False)
    resp_status = {}
    resp_status = json.loads(req.text)
    try:
       sid = resp_status["sid"]
    except:
       sid = "N/A"
    return sid

def logout_checkpoint(host,sid):
    url = "https://"+ host +"/web_api/logout"
    headers = {"Content-Type": "application/json",
               "X-chkp-sid" : sid
              }
    body = {
           }
    req = requests.post(url, json=body, headers=headers, verify = False)
    resp_status = {}
    resp_status = json.loads(req.text)
    return resp_status

def publish_checkpoint(host,domain,sid):
    url = "https://"+ host +"/web_api/publish"
    headers = {"Content-Type": "application/json",
               "X-chkp-sid" : sid
              }
    body = {
           }
    req = requests.post(url, json=body, headers=headers, verify = False)
    time.sleep(2)
    res_status_code = req.status_code

    if res_status_code not in good_resp_codes:
        print("ERROR : Publish failed : {} : {}".format(res_status_code, req.text))

    return res_status_code

def get_host_obj_count(host,sid):
    url =  "https://"+ host +"/web_api/show-hosts"
    headers = {"Content-Type": "application/json",
               "X-chkp-sid" : sid
              }
    body = {
             "details-level" :  "standard",
             "limit" : "1"
            }

    try:
        req = requests.post(url, json=body, headers=headers, verify = False)
        resp_status = {}
        resp_status = json.loads(req.text)
        total = resp_status["total"]
        return total
    except Exception as e:
            return 0


def get_service_tcp_obj_count(host,sid):
    url =  "https://"+ host +"/web_api/show-services-udp"
    headers = {"Content-Type": "application/json",
               "X-chkp-sid" : sid
              }
    body = {
             "details-level" :  "standard",
             "limit" : "1"
            }

    try:
        req = requests.post(url, json=body, headers=headers, verify = False)
        resp_status = {}
        resp_status = json.loads(req.text)
        total = resp_status["total"]
        return total
    except Exception as e:
            return 0

def get_service_udp_obj_count(host,sid):
    url =  "https://"+ host +"/web_api/show-services-udp"
    headers = {"Content-Type": "application/json",
               "X-chkp-sid" : sid
              }
    body = {
             "details-level" :  "standard",
             "limit" : "1"
            }

    try:
        req = requests.post(url, json=body, headers=headers, verify = False)
        resp_status = {}
        resp_status = json.loads(req.text)
        total = resp_status["total"]
        return total
    except Exception as e:
            return 0


def main():
    print("This library needs to be imported by other scripts")
if __name__ == "__main__":
    main()

