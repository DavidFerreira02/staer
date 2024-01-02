from OpenSkyAPI import OpenSkyApi
import requests

api = OpenSkyApi("1201370","staer")
states = api.get_states()
print(states)