import os
from shared_linux_const import LINUX_SYS_I2C_PATH
from sensor import Sensor, SensorData

class Pt100(Sensor):
    """
    This class works with the data from ads122c04
    Read the linux subsystem inside /sys and make all necessary
    data transformation

    Init args:
        sensor_name: The sensor name/nickname
        config: List if a dictionary of parameters {'name', 'ch1', 'ch2'}, 
                each one containing a given name for the pads and the channel config

    Raises:
        FileNotFound: When could not find the ads122c04 inside /sys
    """
    NAME="""AIN{mux1}_AVSS"""
    RAW_FILE="""in_voltage{mux1}_raw"""
    INPUT_FILE="""in_voltage{mux1}_input"""
    MUX_NAME="""AIN{mux1}_AIN{mux2}"""
    MUX_RAW_FILE="""in_voltage{mux1}-voltage{mux2}_raw"""
    MUX_INPUT_FILE="""in_voltage{mux1}-voltage{mux2}_input"""

    def __init__(self, sensor_name: str, config: list) -> None:
        super().__init__(sensor_name)
        self.__channels: list = []
        self.__dirpath: str = ""
        self.__get_dirpath()
        self.__create_channel_list(config)

    def __get_dirpath(self):
        for dirs in os.listdir(LINUX_SYS_I2C_PATH):
            sensor_name_file = os.path.join(LINUX_SYS_I2C_PATH, dirs, 'name')
            if os.path.isfile(sensor_name_file):
                try:
                    with open(sensor_name_file, 'r') as file:
                        sensor_name = file.read().strip()
                        if sensor_name == 'ads122c04':
                            for entry in os.listdir(os.path.join(LINUX_SYS_I2C_PATH, dirs)):
                                if entry.startswith('iio'):
                                    self.__dirpath = os.path.join(LINUX_SYS_I2C_PATH, dirs, entry)
                                    break
                except Exception:
                    continue

        if self.__dirpath == "":
            raise FileNotFoundError("Could not find ti-ads122c04 sys folder")

    def __create_channel_list(self, config: list):
        for entry in config:

            if 'name' not in entry or 'ch1' not in entry:
                print('pt100: Channel config does not have the minimal parameters')
                continue

            channel = SensorData(name=entry["name"])
            if 'ch2' in entry:    
                channel.hw_name = self.MUX_NAME.format(mux1=entry['ch1'], mux2=entry['ch2'])
                channel.raw_file = self.MUX_RAW_FILE.format(mux1=entry['ch1'], mux2=entry['ch2'])
                channel.input_file = self.MUX_INPUT_FILE.format(mux1=entry['ch1'], mux2=entry['ch2'])
            else:
                channel.hw_name = self.NAME.format(mux1=entry['ch1'])
                channel.raw_file = self.RAW_FILE.format(mux1=entry['ch1'])
                channel.input_file = self.INPUT_FILE.format(mux1=entry['ch1'])

            self.__channels.append(channel)

    def __update_data(self):
        for channel in self.__channels:
            print(channel.raw_file)
            print(channel.input_files)
            print(self.__dirpath)
            try:
                channel_raw_file = os.path.join(self.__dirpath, channel.raw_file)
                channel_input_file = os.path.join(self.__dirpath, channel.input_files)
                with open(channel_raw_file,'r') as file: 
                    channel.raw_value = int(file.read().strip())

                with open(channel_input_file,'r') as file: 
                    channel.input_value = int(file.read().strip())
            except Exception:
                print(f"PT100 could not take data from {channel.name}")
                continue

    def get_sensor_data(self):
        """ Get an update sensor data
            
        Returns:
            dictionary: containing the raw and input data from the sensor.
        """
        self.__update_data()
        return self.__channels
