import time
from hw_board import HWBoard
from appconfig import SftrailsConfig, SftrailsSensorTimers
import paho.mqtt.client as mqtt



def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")

def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    userdata.append(message.payload)



def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")



def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
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
    print(mqtt_config)

    #mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    #mqttc.on_connect = on_connect
    #mqttc.on_message = on_message
    #mqttc.on_subscribe = on_subscribe
    #mqttc.on_unsubscribe = on_unsubscribe
    #mqttc.on_publish = on_publish

    #unacked_msg = set()
    #mqttc.user_data_set(unacked_msg)
    #mqttc.connect("mqtt.eclipseprojects.io")
    #mqttc.loop_start()
    #while not stop_event.is_set():
        #msg = hwboard
        #msg_info = mqttc.publish("paho/test/topic", "my message", qos=1)
        #unacked_msg.add(msg_info.mid)
     #   msg_info.wait_for_publish()

    #mqttc.disconnect()
    #mqttc.loop_stop()
