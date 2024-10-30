import time
import json
from hw_board import HWBoard
from appconfig import SftrailsConfig, SftrailsSensorTimers
import paho.mqtt.client as mqtt



def on_subscribe(client, userdata, mid, granted_qos):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    pass

def on_unsubscribe(client, userdata, mid):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    pass

def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    userdata.append(message.payload)



def on_connect(client, userdata, flags, rc):
    print(f"On connect: {str(rc)} ")



def on_publish(client, userdata, mid):
    try:
        print(f"Message {mid} published")
        userdata.remove(mid)
    except Exception as error:
        print(f"We have and error on removing the message {mid} from list. Error {error}")



def mqtt_thread(hwboard: HWBoard, config: SftrailsConfig, stop_event):
    """
    This functions is used to watch the BARRA IN gpio event, if the event is true
    play the sound to inform that the barra in event is detect
    Args:
        hwboard (HWBoard):  Hardware Description 
        config (SftrailsConfig): Configuration of the application
        stop_event (Event): Event that inidicate to exit the loop and finish the function
    """
    mqtt_config = config.get_mqtt_config()

    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_unsubscribe = on_unsubscribe
    mqttc.on_publish = on_publish
    unacked_msg = set()
    mqttc.user_data_set(unacked_msg)
    mqttc.username_pw_set(mqtt_config['username'], mqtt_config['password'])

    while not stop_event.is_set():
        msg = json.dumps(hwboard.get_all_sensors_values_as_json()))
        if mqtt_config['host'] and mqtt_config['port'] and mqtt_config['topic']:
            mqttc.connect(host=mqtt_config['host'], port=int(mqtt_config['port']))
            mqttc.loop_start()
            msg_info = mqttc.publish(mqtt_config['topic'], msg , qos=2)
            unacked_msg.add(msg_info.mid)
            msg_info.wait_for_publish()

            mqttc.disconnect()
            mqttc.loop_stop()


        time.sleep(int(mqtt_config['sleep_timer_s']))
