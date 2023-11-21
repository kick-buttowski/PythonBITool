import http.client
import socket
socket.getaddrinfo('localhost', 8080)
conn = http.client.HTTPSConnection("topics-extraction.p.rapidapi.com")

headers = {
    'accept': "application/json;",
    'X-RapidAPI-Key': "8c6d690b69mshff215948e1ca03dp1e88b7jsn3d19f9b11e84",
    'X-RapidAPI-Host': "topics-extraction.p.rapidapi.com"
}

conn.request("GET", "/topics-2.0?lang=en&tt=a&txt=Show%20Sales%20By%20Fire%20Crackers.&uw=n&rt=n&dm=s&sdg=l&of=json&txtf"
                    "=plain&st=n", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))