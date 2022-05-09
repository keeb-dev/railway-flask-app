import requests
import os
import json 

tailscale_url_base = "https://api.tailscale.com/api/v2"
tailscale_api_key = os.getenv("TAILSCALE_API_KEY")
tailscale_tailnet_name = os.getenv("TAILSCALE_TAILNET_NAME")


#close if env is not setup correctly
if not tailscale_api_key or not tailscale_tailnet_name: 
    print ("no api key or name set")
    exit(1)

def build_url(method):
	return "%s/%s" % (tailscale_url_base, method)

def make_call(url):
	data = requests.get(url, auth=(tailscale_api_key, ""))
	return data.text

def get_devices():
	url = build_url("/tailnet/%s/devices" % tailscale_tailnet_name)
	devices_raw = make_call(url)
	
	# we didn't get shit so return nothing, don't know if this actually works
	if not devices_raw: return []

	print("converting json string into json objects")
	
	devices_json = json.loads(devices_raw)
	device_list = devices_json.get("devices")
	
	print ("i count: '%s' devices " % len(device_list))
	
	device_objects = []
	# time to build an actual list of Devices. did anyone say device?
	for device in device_list:
		device_objects.append(Device(device))
		
	return device_objects

class Device():
	def __init__(self, device_json):
		self.hostname = device_json["hostname"]
		#ipv1 is 0, ipv6 is 1, idc about ipv6
		self.ipv4 = device_json["addresses"][0]
		self.os = device_json["os"]

	def render(self):
		return ",".join([self.hostname, self.ipv4, self.os])


if __name__ == "__main__":
	for device in get_devices():
		print(device.render())


