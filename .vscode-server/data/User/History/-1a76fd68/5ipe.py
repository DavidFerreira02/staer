from OpenSkyAPI import OpenSkyApi
import requests
import login

api = OpenSkyApi(login.username,login.password)
states = api.get_states()
print(states)