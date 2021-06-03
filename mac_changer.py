#!/usr/bin/python3
import subprocess as s
import argparse
import re

def check_interface(interface):
	ifconfig_output = s.check_output(['ifconfig','-a'],text=True)
	interface_list = re.findall('(.*): flags',ifconfig_output)
	#print(interface_list)
	if interface not in interface_list:
		print('[+] Please enter a valid interface.')
		exit()

def get_args():
	parser = argparse.ArgumentParser(description="A simple MAC address changer.")
	parser.add_argument('-i','--interface',help='Interface whose MAC is to be changed.')
	parser.add_argument('-m','--mac',help='MAC to be be changed to.')
	args = parser.parse_args()
	if not args.interface:
		parser.error("[+] Please enter the interface. Use --help for more info.")
	elif not args.mac:
		parser.error("[+] Please enter the mac address. Use --help for more info.")
	return parser.parse_args()

def change_mac(interface,MAC):
	print("[+] Changing MAC address...]")
	s.run(['ifconfig',interface,'down'])
	s.run(['ifconfig',interface,'hw','ether',MAC])
	s.run(['ifconfig',interface,'up'])

def change_check(interface,mac):
	ifconfig_result = s.check_output(['ifconfig',interface],text=True)
	#print(ifconfig_result)
	try:
		found_mac = re.findall('ether (.*)  t',ifconfig_result)[0]
	except:
		print('[+] Could not find MAC address.')
		exit()

	if mac == found_mac:
		print("[+] MAC address of {} has been successfully changed to {}".format(interface,mac))
	else:
		print("[+] Error while changing the MAC address of {}".format(interface))


args = get_args()
check_interface(args.interface)
change_mac(args.interface,args.mac)
change_check(args.interface,args.mac)