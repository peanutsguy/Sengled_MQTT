import sengled
import json
import yaml
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    api = sengled.api(
        username=j["user"],
        password=j["pswd"],
        session_path="/config/sengled.pickle"
    )
    device = api.get_device_details()
    for entry in device:
        devid = entry.id
        switch = "sengled/"+devid+"/switch"
        status = "sengled/"+devid+"/status"
        #print(switch)
        client.subscribe(switch)
        if entry.onoff:
            client.publish(status,"ON")
        else:
            client.publish(status,"OFF")
    

def on_message(client, userdata, msg):
    api = sengled.api(
        username=j["user"],
        password=j["pswd"],
        session_path="/config/sengled.pickle"
    )
    mensaje = msg.payload.decode("utf-8")
    canal = msg.topic
    foco = canal.split('/')[1]
    command = canal.split('/')[2]
    bulb = api.find_by_id(foco)
    bstatus = "sengled/"+foco+"/status"
    
    #print(msg.topic+" "+str(msg.payload))

    if command == "status":
        if bulb.onoff:
            client.publish(bstatus,"ON")
        else:
            client.publish(bstatus,"OFF")
    else:
        if mensaje == "ON":
            #print("TURN ON - "+foco)
            status = bulb.on()
        elif mensaje == "OFF":
            #print("TURN OFF - "+foco)
            status = bulb.off()
        
        if status.onoff:
            client.publish(bstatus,"ON")
        else:
            client.publish(bstatus,"OFF")

f=open("/config/cred","r")
j=json.load(f)
host=j["mqtt"]

api = sengled.api(
    username=j["user"],
    password=j["pswd"],
    session_path="/config/sengled.pickle"
)

i = 0
homeassistant = {"light":[]}
device = api.get_device_details()
for entry in device:
    devid = entry.id
    name = entry.name
    switch = "sengled/"+devid+"/switch"
    status = "sengled/"+devid+"/status"
    homeassistant["light"].insert(i,{"platform":"mqtt","name":name,"state_topic":status,"command_topic":switch,"payload_on":"ON","payload_off":"OFF","optimistic":False})
    i = i+1

ff = open('/config/home_assistant.yaml', 'w')
yaml.dump(homeassistant,ff)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host,1883,60)
client.loop_forever()