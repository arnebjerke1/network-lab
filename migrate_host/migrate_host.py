#!/usr/bin/python3
import sys
import json
import requests
import logging
import os
import re
import configparser
import argparse
import ipaddress
from cpapirequest import login_checkpoint, logout_checkpoint, publish_checkpoint
import xmltodict
from datetime import datetime
import socket
import getpass
from devices import gc_hosts,palo_hosts,DOMAINS,proxy_mgmt


#Variables
## Paths
config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.conf')
log = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log')

##Read data from config file
config = configparser.ConfigParser(interpolation=None)
config.read(config_file)
snap_host = config['SNAP']['SNAP_HOST']
snap_netsec_user = config['SNAP']['SNAP_NETSEC_API_USER']
snap_netsec_password = config['SNAP']['SNAP_NETSEC_API_PASSWORD']

##Hardcoded variables
good_resp_codes = [ 200, 201 ]
bc_policies = ["SE_NO_AUTH_SRC", "SE ProxySG VPM PROD", "EE ProxySG VPM"]
palo_api_ver = "10.2"
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m' 
YELLOW = '\033[33m'


#To disable HTTPS warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Logging config
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    filename=log,
    filemode='a',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

#Check if it's valid IP or CIDR
def check_ip_address(value):
    try:
        return ipaddress.ip_address(value)
    except ValueError as err:
        raise argparse.ArgumentTypeError(f"Invalid IP address: {err}")
    
## Get arguments
parser = argparse.ArgumentParser(description='This script will find if old IP address is used somewhere in brownfield')
parser.add_argument('--new_ip', type=check_ip_address, help='Please insert the IP in greenfield')
parser.add_argument('--old_ip', type=check_ip_address,required=True, help='Please insert the IP in brownfield')
parser.add_argument('--check',action='store_true', help='Check if IP is used anywhere')

#Parse arguments
args = parser.parse_args()

if (args.new_ip and not args.check) or (args.check and args.old_ip): 
    if args.new_ip:
        print("Processing with new IP and old IP:")
        print(f"New IP: {args.new_ip}")
        print(f"Old IP: {args.old_ip}")
        pass
    elif args.check:
        print("Checking old IP usage:")
        print(f"Old IP: {args.old_ip}")
        pass
else:
    print("Either both --new_ip and --old_ip must be specified, or --check with --old_ip.")
    parser.print_help()
    sys.exit()

args_old_ip = str(args.old_ip)
args_new_ip = str(args.new_ip)

#SNAP
def find_f5_backend_in_snap():
    url = f"https://{snap_host}/api/now/table/u_cmdb_ci_lb_service_backend?sysparm_query=nameLIKE{args_old_ip}^install_status=1&sysparm_fields=name%2Csys_id%2Cinstall_status%2Coperational_status"
    headers = {
            "Content-Type": "application/json"
            }   
    req = requests.get(url, headers=headers, auth=(snap_netsec_user, snap_netsec_password), verify = False)
    resp_status = {}
    resp_status = json.loads(req.text)
    try:
        backends = resp_status['result']
        if not backends:
            return False
        else:
            return True
    except Exception as e:
        logging.error(f"Tried to find F5 backends in SNAP, got {str(e)}")
        return False
    
def find_snap_fw_rule(address):
    src_url = f"https://{snap_host}/api/now/table/u_cmdb_ci_network_fw_rule?sysparm_query=u_source_ip={address}^install_status=1&sysparm_fields=name"
    dst_url = f"https://{snap_host}/api/now/table/u_cmdb_ci_network_fw_rule?sysparm_query=u_destination_ip={address}^install_status=1&sysparm_fields=name"

    headers = {
                "Content-Type": "application/json"
              }

    rules = []
    try:
        src_req = requests.get(src_url, headers=headers, auth=(snap_netsec_user, snap_netsec_password), verify = False)
        resp_status = {}
        resp_status = json.loads(src_req.text)
        req_status_code = src_req.status_code
        result = resp_status['result']
        for i,names in enumerate(result):
             name = names['name']
             rules.append(name)
    except:
        logging.info(f"WARNING:DEBUG - Couldn't fetch IP address {address} related rules (as source) from SNAP. HTTP response {req_status_code}")
        pass

    try:
        dst_req = requests.get(dst_url, headers=headers, auth=(snap_netsec_user, snap_netsec_password), verify = False)
        resp_status = {}
        resp_status = json.loads(dst_req.text)
        result = resp_status['result']
        for i,names in enumerate(result):
             name = names['name']
             rules.append(name)
    except:
        logging.info(f"WARNING:DEBUG - Couldn't fetch IP address {address} related rules (as destination) from SNAP. HTTP response {req_status_code}")
        pass
    logging.info(f"Found the following firewall rule CI -s to be associated with the group")
    logging.info(f"{rules}")

    return rules

#Checkpoint
def add_cp_group(host,sid,group_name,comments):
    url = f"https://{host}/web_api/add-group"
    headers = {
                "Content-Type": "application/json",
                "X-chkp-sid" : sid
              }
    body = {
            "name" : group_name,
            "color" : "orange",
            "ignore-warnings" : True,
            "comments" : comments
           }
    req = requests.post(url, json=body, headers=headers, verify = False)
    res_status_code = req.status_code

    if res_status_code not in good_resp_codes:
        logging.info("ERROR : Adding group failed : {} : {}".format(res_status_code, req.text))
    else:
       logging.info(f"Created Checkpoint group {group_name}")

    return res_status_code


def show_cp_host(host,sid,ip_address):
    url = f"https://{host}/web_api/show-host"
    headers = {
                "Content-Type": "application/json",
                "X-chkp-sid" : sid
              }
    body = {
            "name" : f"ip.{ip_address}"
           }
    req = requests.post(url, json=body, headers=headers, verify = False)
    res_status_code = req.status_code
    if res_status_code not in good_resp_codes:
        logging.info("Checkpoint host not found : {}".format(res_status_code))
    else:
        logging.info(f"Checkpoint host {ip_address} exists")

    return res_status_code

def add_cp_host(host,sid,group_name,ip_address):
    url = f"https://{host}/web_api/add-host"
    headers = {
                "Content-Type": "application/json",
                "X-chkp-sid" : sid
              }
    body = {
            "name" : f"ip.{ip_address}",
            "ip-address" : ip_address,
            "groups" : [ group_name ],
            "color" : "orange",
            "ignore-warnings" : True
           }
    req = requests.post(url, json=body, headers=headers, verify = False)
    res_status_code = req.status_code

    if res_status_code not in good_resp_codes:
        logging.info("ERROR : Adding host failed : {} : {}".format(res_status_code, req.text))
    else:
        logging.info(f"Created Checkpoint host {ip_address}")

    return res_status_code

def set_cp_host(host,sid,group_name,ip_address,action):
    if action not in [ "add", "remove"]:
        logging.info(f"ERROR: set_cp_host input parameters faulty. {host}, {group_name},{ip_address}, {action} ")
        return None

    url = f"https://{host}/web_api/set-host"
    headers = {
                "Content-Type": "application/json",
                "X-chkp-sid" : sid
              }
    body = {
            "name" : f"ip.{ip_address}",
            "groups" : {
                action : [ group_name ]
            }
           }

    req = requests.post(url, json=body, headers=headers, verify = False)
    res_status_code = req.status_code
    if res_status_code not in good_resp_codes:
        logging.info("ERROR : Setting host failed : {} : {}".format(res_status_code, req.text))
    else:
        logging.info(f"Checkpoint host - action {action} - {ip_address} to/from group {group_name}")

    return res_status_code

def cp_where_used(host,sid,ip_address,domain):
    url = f"https://{host}/web_api/where-used"
    headers = {
            "Content-Type": "application/json",
            "X-chkp-sid" : sid
            }
    body = {
            "name" : f"ip.{ip_address}"
           }
    
    req = requests.post(url, json=body, headers=headers, verify = False)
    res_status_code = req.status_code
    if res_status_code in good_resp_codes:
        resp_status = {}
        resp_status = json.loads(req.text)
        total = resp_status["used-directly"]["total"]
        return total
    else:
        logging.info(f"Host not found in {domain}")
        return 0      
           
#Bluecoat
def get_bc_policies(username,password,bc_policy):
    url = f"https://{proxy_mgmt}:8082/api/policies"
    headers = { "Content-Type": "application/json" }
    req = requests.get(url, headers=headers, auth=(username, password), verify = False)
    resp_status = {}
    resp_status = json.loads(req.text)
    policy_uuid = []
    try:
       for i,policy in enumerate(resp_status):
            if policy["name"] == bc_policy:
                policy_uuid = policy["uuid"]
    except:
       print(f"{YELLOW}Unable parse Bluecoat policies - {resp_status}{RESET}")
       logging.warning(f"Unable parse Bluecoat policies - {resp_status}")

    return policy_uuid

def parse_bc_policy_for_ip(policy_uuid,username,password):
    url = f"https://{proxy_mgmt}:8082/api/policies/{policy_uuid}/content"
    headers = { "Content-Type": "application/json" }
    req = requests.get(url, headers=headers, auth=(username, password), verify = False)
    try:
        resp_status = {}
        resp_status = json.loads(req.text)
        ip_addresses = resp_status["content"]["ipAddresses"]
        for i,address in enumerate(ip_addresses):
            if args_old_ip == address["ipAddress"]:
                found = True
                break
            else:
                found = False
    except KeyError:
        vpm_policy = resp_status["content"]["xml"]
        if args_old_ip in vpm_policy:
            found = True
        else:
            found = False
    except Exception as e:
        print(f"{YELLOW}Unable to parse Bluecoat policy {policy_uuid} - got exception {e}{RESET}")
        logging.warning(f"Unable to parse Bluecoat policy {policy_uuid} - got exception {e}")
        found = False

    return found

#Palo
def check_palo_address(host,api_key,cidr):
    names = [ "ip.", "mip."]
    headers = {
                "Content-Type": "application/json",
                "X-PAN-KEY" : api_key
              }
    
    for name in names:
        url = f"https://{host}/restapi/v{palo_api_ver}/objects/addresses?location=shared&name={name}{cidr}"
        req = requests.get(url, headers=headers, verify = False)
        res_status_code = req.status_code
        if res_status_code in good_resp_codes:
            logging.info(f"Address object {name} exists on {host}.")
            return True
    return False
    
def login_palo(username,password,host):
    url = f"https://{host}/api/?type=keygen&user={username}&password={password}"
    try:
       req = requests.post(url, verify = False)
       d = xmltodict.parse(req.text)
       key = d['response']['result']['key']
    except Exception as e:
       logging.error(f"Uneble to log into Palo host {host}. Got {e}")
       key = "N/A"

    return key  

#Guardicore
def login_guardicore(gc_host,username,password):
    url = f"https://{gc_host}/api/v3.0/authenticate"
    headers = {"Content-Type": "application/json"}
    body = {
             "username" : username,
             "password" : password
           }
    try:
        req = requests.post(url, json=body, headers=headers, verify = False)
        resp_status = {}
        resp_status = json.loads(req.text)
        token = resp_status["access_token"]
    except Exception as e:
        logging.error(f"Unable to log into Guardicore host {gc_host} - got {e}")
        token = "N/A"
    return token

def check_guardicore_assets(gc_host,token):
    asset_url = f"https://{gc_host}/api/v4.0/assets?fields=id,name,status,nics&ip={args_old_ip}&status=on"
    headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " +token
            }
    try:
        asset_req = requests.get(asset_url, headers=headers, verify = False)
        resp_status = {}
        resp_status = json.loads(asset_req.text)
        total = resp_status["total"]
        if total > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error getting response from Guardicore - got {e}")
    
def check_guardicore_labels(gc_host,token):
    headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " +token
            }
    url = f"https://{gc_host}/api/v3.0/visibility/labels?assets=on,off&distinguish_static_dynamic_assets=false&from_time=0&text_search={args_old_ip}"
    try:
        req = requests.get(url, headers=headers, verify = False)
        resp_status = {}
        resp_status = json.loads(req.text)
        total = resp_status["total_count"]
    except Exception as e:
        print(f"Error getting response from Guardicore - got {e}")
    if total > 1:
        return True
    else:
        return False

def check_guardicore_policy(gc_host,token):
    headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " +token
            }
    url = f"https://{gc_host}/api/v4.0/visibility/policy/rules?start_at=0&max_results=128&order=section_position&order_direction=down&subnets={args_old_ip}"
    try:
        req = requests.get(url, headers=headers, verify = False)
        resp_status = {}
        resp_status = json.loads(req.text)
        total = resp_status["total"]
    except Exception as e:
        print(f"Error getting response from Guardicore - got {e}")
        print(resp_status)

    if total > 1:
        objects = resp_status["objects"]
        for obj in objects:
            try:
                found_in_source = any(x == f"{args_old_ip}/32" for x in obj["source"]["subnets"])
            except:
                found_in_source = False
            try:
                found_in_destination = any(x == f"{args_old_ip}/32" for x in obj["destination"]["subnets"])
            except:
                found_in_destination = False
            if found_in_source or found_in_destination:
                if found_in_source:
                    return True
                if found_in_destination:
                    return True
            else:
                return False
    else:
        return False

#Resolve DNS
def get_hostname(ip_address):
    return socket.getnameinfo((ip_address, 0),0)[0].split(".", 1)[0].lower()

def match_servername(input_text):
    pattern = re.compile(r"^(lx|srv)([0-9]{5})$", re.IGNORECASE)
    return bool(pattern.match(input_text))


def main():
    logging.info('=' * 60)
    command = (" ".join(sys.argv))
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Executed command - {command}")

    #Ask user for credentials
    if sys.stdin.isatty():
        print("Enter A account credentials")
        username = input("Username: ")
        password = getpass.getpass("Password: ")
    else:
        username = sys.stdin.readline().rstrip()
        password = sys.stdin.readline().rstrip()

    if not username or not password:
        print("Username or password cannot be empty. Exiting")
        sys.exit()

    logging.info(f"Request is run by user {username} at {now}")
    logging.info('-' * 60)
    if not args.check:
        #Resolve name
        resolved_name = get_hostname(str(args_old_ip))
        if match_servername(resolved_name):
            hostname = resolved_name
            
        else:
            given_hostname = input("Hostname was not resolved. Please provide group name to use: ") 
            if match_servername(given_hostname):
                hostname = given_hostname
            else:
                print(f"Given name {given_hostname} does not comply to server naming (srv...|lx...). Exiting!")
                sys.exit()
        print(f"Creating group with following name - {hostname}")
    #Add groups to Checkpoint
    for key, val in enumerate(DOMAINS):
        for checkpoint_management,checkpoint_domain in val.items():
            for i, checkpoint_domain_list_item in enumerate(checkpoint_domain):
                sid = login_checkpoint(checkpoint_management,checkpoint_domain_list_item,username,password)
                if sid != "N/A":
                    used_in = cp_where_used(checkpoint_management,sid,args_old_ip,checkpoint_domain_list_item)
                    if used_in > 0:
                        print(f"IP address {args_old_ip} {GREEN}is used in domain {checkpoint_domain_list_item}{RESET}")
                        logging.info(f"IP address {args_old_ip} is used in domain {checkpoint_domain_list_item}")
                        if not args.check:
                            group_add_status = add_cp_group(checkpoint_management,sid,hostname,f"{args_old_ip},{args_new_ip}")
                            if group_add_status in good_resp_codes:
                                add_new = add_cp_host(checkpoint_management,sid,hostname,args_new_ip)
                                if add_new in good_resp_codes:
                                    logging.info(f"Added new host {args_new_ip} to group {hostname} in domain {checkpoint_domain_list_item}")
                                else:
                                    logging.info(f"Failed to add new host {args_new_ip} to group {hostname} in domain {checkpoint_domain_list_item} - {add_new}")
                                add_old = set_cp_host(checkpoint_management,sid,hostname,args_old_ip,"add")
                                if add_old in good_resp_codes:
                                    logging.info(f"Added old host {args_old_ip} to group {hostname} in domain {checkpoint_domain_list_item}")
                                else:
                                    logging.info(f"Failed to old add host {args_old_ip} to group {hostname} in domain {checkpoint_domain_list_item} - {add_old}")
                                publish_checkpoint(checkpoint_management,checkpoint_domain_list_item,sid)
                        logout_checkpoint(checkpoint_management,sid)
                    else:
                        print(f"IP address {args_old_ip} {RED}is not used in domain {checkpoint_domain_list_item}{RESET}")
                        logging.info(f"IP address {args_old_ip} is not used in domain {checkpoint_domain_list_item}")
                else:
                    print(f"{YELLOW}Unable to log into Checkpoint domain {checkpoint_domain_list_item}{RESET}")
                    logging.error(f"Unable to log into Checkpoint domain {checkpoint_domain_list_item}")
                    continue

    #Check Palo Alto
    for palo_host in (palo_hosts):
        api_key = login_palo(username,password,palo_host)
        if api_key != "N/A":
            host_exists = check_palo_address(palo_host,api_key,args_old_ip)
            if host_exists:
                print(f"IP address {args_old_ip}{GREEN} found in Panorama host {palo_host}{RESET}")
            else:
                print(f"IP address {args_old_ip}{RED} is not used in  Panorama host {palo_host}{RESET}")
        else:
            print(f"{YELLOW}Unable to log into Panorama host {palo_host}{RESET}")

    #Check BlueCoat
    for policy in bc_policies:
        policy_uuid = get_bc_policies(username,password,policy)
        found_in_bc = parse_bc_policy_for_ip(policy_uuid,username,password)
        if found_in_bc:
            print(f"IP address {args_old_ip}{GREEN} found in Bluecoat policy {policy}{RESET}")
            logging.info(f"IP address {args_old_ip} found in Bluecoat policy {policy}")
        else:
            print(f"IP address {args_old_ip}{RED} is not used in Bluecoat policy {policy}{RESET}")
            logging.info(f"IP address {args_old_ip} is not used in Bluecoat policy {policy}")

    #Check SNAP
    found_in_snap = find_f5_backend_in_snap()
    if found_in_snap:
        print(f"IP address {args_old_ip}{GREEN} is used as backend for F5. Please check SNAP. {RESET}")
        logging.info(f"IP address {args_old_ip} is used as backend for F5. Please check SNAP.")
    else:
        print(f"IP address {args_old_ip}{RED} is not used as backend for F5. {RESET}")
        logging.info(f"IP address {args_old_ip} is not used as backend for F5.")
    
    if args.check:
        fw_rule_ci_count = len(find_snap_fw_rule(args_old_ip))
        if fw_rule_ci_count > 1:
            print(f"IP address {args_old_ip}{GREEN} is used in FW rule CI. Please check SNAP. {RESET}")
            logging.info(f"IP address {args_old_ip} is used in FW rule CI. Please check SNAP.")
        else:
            print(f"IP address {args_old_ip}{RED} is not used in FW rule CI. {RESET}")
            logging.info(f"IP address {args_old_ip} is not used in FW rule CI.")


    #Guardicore
    for gc_host in gc_hosts:
        token = login_guardicore(gc_host,username,password)
        if token != "N/A":
            assets = check_guardicore_assets(gc_host,token)
            
            if assets:
                print(f"IP address {args_old_ip}{GREEN} is used in Guardicore assets in host {gc_host}.{RESET}")
                logging.info(f"IP address {args_old_ip} is used in Guardicore assets in host {gc_host}.")
            else:
                print(f"IP address {args_old_ip}{RED} is not used in Guardicore assets in  host {gc_host}.{RESET}")
                logging.info(f"IP address {args_old_ip} is not used in Guardicore assets in  host {gc_host}.")

            labels = check_guardicore_labels(gc_host,token)
            if labels:
                print(f"IP address {args_old_ip}{GREEN} is used in Guardicore labels in host {gc_host}.{RESET}")
                logging.info(f"IP address {args_old_ip} is used in Guardicore labels in host {gc_host}.")
            else:
                print(f"IP address {args_old_ip}{RED} is not used in Guardicore labels in host {gc_host}.{RESET}")
                logging.info(f"IP address {args_old_ip} is not used in Guardicore labels in host {gc_host}.")

            policy = check_guardicore_policy(gc_host,token)
            if policy:
                print(f"IP address {args_old_ip}{GREEN} is used in Guardicore policy in host {gc_host}.{RESET}")
                logging.info(f"IP address {args_old_ip} is used in Guardicore policy in host {gc_host}.")
            else:
                print(f"IP address {args_old_ip}{RED} is not used in Guardicore policy in host {gc_host}.{RESET}")
                logging.info(f"IP address {args_old_ip} is not used in Guardicore policy in host {gc_host}.")
        else:
            print(f"{YELLOW} Unable to log into Guardicore host {gc_host} {RESET}")
            logging.info(f"Unable to log into Guardicore host {gc_host}")
        
            

if __name__ == "__main__":
    main()