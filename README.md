# Sengled MQTT for Home Assistant

I created this python application in order to connect my Sengled Hub with Home Assistant via MQTT.

This is my first python app and I know there are a lot of improvements to be made. Any suggestions/improvements are welcomed.

### Main features
- Switch/Status MQTT topics based on device id
- Home Assistant light entities generator
- Dockerfile for easy deployment

### Current ToDo List
- Integration of Sengled Smart Plug (mine arrives next week), only works with lightbulbs currently.
- Brightness control (yet)

### Usage
The Dockerfile builds the docker image based on _python:alpine3.7_ and installs all the required python dependencies.

    docker build --tag sengledmqtt .

To setup your Sengled user credentials and MQTT Broker, you have to edit _appdata/cred_, which is a JSON file with the following structure

    {
        "user":"[Sengled User Email]",
        "pswd":"[Sengled User Password]",
        "mqtt":"[MQTT Broker IP/FQDN]"
    }

Once your credentials have been configured, you can start a Docker container with the following command

    docker run -v /[path to folder]/appdata:/config -d [your image name]

At startup, the application will connect to Sengled and generate a YAML file called _home_assistant.yaml_ in the _appdata_ folder which will contain all your Sengled devices as MQTT lights for Home Assitant, with this structure

    light:
    - command_topic: sengled/[Sengled Device ID]/switch
      name: [Sengled Device Name]
      optimistic: false
      payload_off: 'OFF'
      payload_on: 'ON'
      platform: mqtt
      state_topic: sengled/[Sengled Device ID]/status

### Used Python Libraries
- [sengled-client](https://github.com/vroy/python-sengled-client) (by Vincent Roy)
- [paho-mqtt](http://www.eclipse.org/paho/) (from Eclipse)
- [pyyaml](https://github.com/yaml/pyyaml) (from YAML)