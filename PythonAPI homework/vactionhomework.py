#!/usr/bin/env python
# coding: utf-8

# # VacationPy
# ----
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os

# Import API key
from api_keys import g_key


# In[2]:


gmaps.configure("AIzaSyAajmei5kgRsEoeT9bOrt3macfxAOBu-B8")


# ### Store Part I results into DataFrame
# * Load the csv exported in Part I to a DataFrame

# In[3]:


df = pd.read_csv("weatherData.csv")
df.head()


# ### Humidity Heatmap
# * Configure gmaps.
# * Use the Lat and Lng as locations and Humidity as the weight.
# * Add Heatmap layer to map.

# In[4]:


locations = df[["latitude", "longitude"]]

humid = df["humidity"]


# In[5]:


fig = gmaps.figure(map_type="HYBRID")


# ### Create new DataFrame fitting weather criteria
# * Narrow down the cities to fit weather conditions.
# * Drop any rows will null values.

# In[6]:


vaction1 = (df.temperature >= 70) & (df.temperature < 80)
vaction2 = df.wind_speed < 10
vaction3 = df.cloudiness == 0
vaction4 = weather1 & weather2 & weather3

ideal_cities = df.loc[vaction4].reset_index(drop=True)
ideal_cities


# In[8]:


figure_layout = {
    'width': '800px',
    'height': '600px',
    'border': '1px solid black',
    'padding': '1px',
    'margin': '0 auto 0 auto'
}
fig = gmaps.figure(map_type="HYBRID", layout=figure_layout)

coordinates = ideal_cities[["latitude", "longitude"]]

markers = gmaps.marker_layer(coordinates)

fig.add_layer(markers)
fig


# In[9]:


city_info = []

for indx, row in ideal_cities.iterrows():
    info_box = f"""
                <dl>
                <dt>Name</dt><dd>{row.cities}</dd>
                <dt>Temp</dt><dd>{row.temperature}</dd>
                <dt>Cloudiness</dt><dd>{row.cloudiness}%</dd>
                </dl>
                """
    
    city_info.append(info_box)


# In[10]:


figure_layout = {
    'width': '800px',
    'height': '600px',
    'border': '1px solid black',
    'padding': '1px',
    'margin': '0 auto 0 auto'
}

fig = gmaps.figure(map_type="HYBRID", layout=figure_layout)

coordinates = ideal_cities[["latitude", "longitude"]]

marker_layer = gmaps.marker_layer(coordinates, info_box_content=city_info)
fig.add_layer(marker_layer)
fig


# ### Hotel Map
# * Store into variable named `hotel_df`.
# * Add a "Hotel Name" column to the DataFrame.
# * Set parameters to search for hotels with 5000 meters.
# * Hit the Google Places API for each city's coordinates.
# * Store the first Hotel result into the DataFrame.
# * Plot markers on top of the heatmap.

# In[11]:


ideal_cities.head(1)


# In[12]:


params = {"key": g_key}

base_url = "https://maps.googleapis.com/maps/api/geocode/json"

lat = ideal_cities["latitude"][1]
lng = ideal_cities["longitude"][1]

# update address key value
params['latlng'] = f"{lat},{lng}"

# make request
thing = requests.get(base_url, params=params)

thing = thing.json()
thing["results"][0]["address_components"]


for addressComp in thing["results"][0]["address_components"]:
    if addressComp["types"][0] == "country":
        print(addressComp["long_name"])


# In[13]:


def getCountryForCity(lat, long):    
    rtnCountry = ""
    
    params = {"key": g_key}

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    lat = ideal_cities["latitude"][indx]
    lng = ideal_cities["longitude"][indx]

    # update address key value
    params['latlng'] = f"{lat},{lng}"

    # make request
    thing = requests.get(base_url, params=params)

    thing = thing.json()
    thing["results"][0]["address_components"]


    for addressComp in thing["results"][0]["address_components"]:
        if addressComp["types"][0] == "country":
            rtnCountry = addressComp["long_name"]
            
    return rtnCountry


# In[14]:


countries = []
for indx, row in ideal_cities.iterrows():
    countries.append(getCountryForCity(row.latitude, row.longitude))


# In[15]:


countries


# In[16]:


params = {
    "radius": 5000,
    "types": "hotel",
    "keyword": "hotel",
    "key": g_key
}

lat = ideal_cities["latitude"][0]
lng = ideal_cities["longitude"][0]

params["location"] = f"{lat},{lng}"

base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

name_address = requests.get(base_url, params=params)
name_address = name_address.json()

name_address["results"][0]["name"]


# In[28]:


name_address["results"][0]


# In[18]:


# Use the lat/lng we recovered to identify airports

names = []
addresses = []
ratings = []

params = {
    "radius": 5000,
    "types": "hotel",
    "keyword": "hotel",
    "key": g_key
}

for index, row in ideal_cities.iterrows():
    # get lat, lng from df
    lat = row["latitude"]
    lng = row["longitude"]

    # change location each iteration while leaving original params in place
    params["location"] = f"{lat},{lng}"

    # Use the search term: "International Airport" and our lat/lng
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # make request and print url
    name_address = requests.get(base_url, params=params)

    # convert to json
    name_address = name_address.json()
    
    try:
        names.append(name_address["results"][0]["name"])
        addresses.append(name_address["results"][0]["vicinity"])
        ratings.append(name_address["results"][0]["rating"])
    except (KeyError, IndexError):
        print("Missing field/result... skipping.")
        names.append("")
        addresses.append("")
        ratings.append("")


# In[19]:


names


# In[20]:


ideal_cities["country"] = countries
ideal_cities["hotels"] = names
ideal_cities["addresses"] = addresses
ideal_cities["ratings"] = ratings

ideal_cities


# In[23]:


locations = df[["latitude", "longitude"]]

humid = df["humidity"]


# In[24]:


city_info = []

for indx, row in ideal_cities.iterrows():
    info_box = f"""
                <dl>
                <dt>Hotel Name</dt><dd>{row.hotels}</dd>
                <dt>City</dt><dd>{row.cities}</dd>
                <dt>Country</dt><dd>{row.country}</dd>
                </dl>
                """
    
    city_info.append(info_box)


# In[25]:


figure_layout = {
    'width': '800px',
    'height': '600px',
    'border': '1px solid black',
    'padding': '1px',
    'margin': '0 auto 0 auto'
}

# Plot Heatmap
fig = gmaps.figure(map_type="HYBRID", layout=figure_layout)

# Create heat layer
heat_layer = gmaps.heatmap_layer(locations, weights=humid, dissipating=True)


# Add layer
fig.add_layer(heat_layer)

#add points
coordinates = ideal_cities[["latitude", "longitude"]]
marker_layer = gmaps.marker_layer(coordinates, info_box_content=city_info)
fig.add_layer(marker_layer)

# Display figure
fig


# In[ ]:





# In[ ]:





# In[ ]:





# In[26]:


# NOTE: Do not change any of the code in this cell

# Using the template add the hotel marks to the heatmap
info_box_template = """
<dl>
<dt>Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{City}</dd>
<dt>Country</dt><dd>{Country}</dd>
</dl>
"""
# Store the DataFrame Row
# NOTE: be sure to update with your DataFrame name
hotel_info = [info_box_template.format(**row) for index, row in hotel_df.iterrows()]
locations = hotel_df[["Lat", "Lng"]]


# In[ ]:


# Add marker layer ontop of heat map


# Display figure


# In[ ]:




