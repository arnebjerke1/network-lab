https://jira.swedbank.net/browse/NS-5706__

https://git.swedbank.net/projects/DCINW/repos/migrate_host/browse

This script will check all Checkpoint domains, Palo alto firewalls, Guardicore assets and labels, SNAP F5 backend table and Bluecoat proxy Sweden and Estonia policies for occurense of old IP.
If the IP is found in Checkpoint, a group with the resolved name for the old IP will be used to create a network group containing both old IP and new IP.

Example:
python .\migrate_host.py --new_ip 1.2.3.4 --old_ip 2.3.4.5

This script allows to check if IP is used in Checkpoint, Palo ALto, Guardicore, Proxy, F5 or SNAP FW rule CI -s

Example
python migrate_host.py --old_ip 1.1.1.1 --check

