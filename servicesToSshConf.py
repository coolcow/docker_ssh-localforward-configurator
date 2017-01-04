#!/usr/bin/env python

__author__ = 'Jean-Michel Ruiz (mail@coolcow.org)'

import sys
import json
import argparse
from ipaddress import ip_address
 
# ARGUMENTS

parser = argparse.ArgumentParser(description='Creates a ssh.config for the given services file (as json). Also outputs the corresponding /etc/hosts entries to stdout.')
parser.add_argument('services_file', help='The input file containing the services description as json.', type=argparse.FileType('r'), nargs='?', default=sys.stdin)
parser.add_argument('-n', '--name', help='The profile name (Host in ssh.conf).', required=True)
parser.add_argument('-t', '--target', help='The host name this profile connects to (Hostname in ssh.conf).', required=True)
parser.add_argument('-p', '--port', help='The port this profile connects to (Host in ssh.conf).', type=int, default=22, required=False)
parser.add_argument('-u', '--user', help='The login name this profile connects with (User in ssh.conf).', required=True)
parser.add_argument('-i', '--identity-file', help='The ssh identity file this profile connects with (IdentityFile in ssh.conf).', required=False)
parser.add_argument('-l', '--local-ip', help='The first local ip the remote port is forwarded to. This ip is incremented for each new remote host.', default='127.0.1.1', required=False)
parser.add_argument('-o', '--output-file', help='The file where the ssh.config is written to.', type=argparse.FileType('w'), required=True)

args = parser.parse_args()

services = json.load(args.services_file)
name = args.name
target = args.target
port = args.port
user = args.user
identity = args.identity_file
local_ip = ip_address(str(args.local_ip))
output_file = args.output_file

# HEAD COMMENT

print('##########')
print('# Writing ssh configuration to: ' + output_file.name)
print('# The /etc/hosts entries are printed below...')
print('##########')

first = True
args = ''
for arg in sys.argv :
	args += '' if first else (str(arg) + ' ')
	first = False
output_file.write('# ' + args + '\n')

# MAIN PART

output_file.write('Host ' + name + '\n')
output_file.write('   Hostname ' + target + '\n')
if port is not None : output_file.write('   Port ' + str(port) + '\n')
if user is not None : output_file.write('   User ' + user + '\n')
if identity is not None : output_file.write('   IdentityFile ' + identity + '\n')

# LOCALFORWARD PART

for service in services :
	service_ip = ip_address(str(service['ip']))
	
	names = str(service_ip)
	for name in service['names'] :
		names += ' ' + name

	if str(local_ip).endswith('.0') :
		local_ip += 1

	print(str(local_ip) + " " + names)

	for service_port in service['ports'] :
		output_file.write('   LocalForward ' + str(local_ip) + ":" + str(service_port) + ' ' + str(service_ip) + ':' + str(service_port) + '\n')

	local_ip += 1
