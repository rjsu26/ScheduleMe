from torrequest import TorRequest
import requests

tr = TorRequest(password='10BoiledCabbage')
response = requests.get('http://ipecho.net/plain')
print("My original IP is: ", response.text)
for _ in range(10):
    tr = TorRequest(password='10BoiledCabbage')
    tr.reset_identity()
    response = tr.get('http://ipecho.net/plain')
    print("New IP is: ", response.text)
