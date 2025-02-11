import os
from os_shared import LINUX_SYS_I2C_PATH
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
    FILE="""in_voltage{mux1}_{filetype}"""
    MUX_NAME="""AIN{mux1}_AIN{mux2}"""
    MUX_FILE="""in_voltage{mux1}-voltage{mux2}_{filetype}"""

    def __init__(self, sensor_name: str, config: list, pt100_config: dict) -> None:
        super().__init__(sensor_name)
        self.__channels: list = []
        self.__dirpath: str = ""
        self.__get_dirpath()
        self.__create_channel_list(config)
        self.__pt100_config = pt100_config

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
                channel.raw_file = self.MUX_FILE.format(mux1=entry['ch1'], mux2=entry['ch2'],
                                                        filetype="raw")
                channel.scale_file = self.MUX_FILE.format(mux1=entry['ch1'], mux2=entry['ch2'],
                                                          filetype="scale")
            else:
                channel.hw_name = self.NAME.format(mux1=entry['ch1'])
                channel.raw_file = self.FILE.format(mux1=entry['ch1'], filetype="raw")
                channel.scale_file = self.FILE.format(mux1=entry['ch1'], filetype="scale")

            self.__channels.append(channel)

    def update_sensor_data(self):
        """
        Update sensor data
        Args:
            pt100_config(dict): Pt100 config for temperature calculation 
        """
        for channel in self.__channels:
            try:
                channel_raw_file = os.path.join(self.__dirpath, channel.raw_file)
                channel_scale_file = os.path.join(self.__dirpath, channel.scale_file)
                with open(channel_raw_file,'r') as file: 
                    channel.raw_value = int(file.read().strip())

                with open(channel_scale_file,'r') as file: 
                    channel.scale_value = float(file.read().strip())

                self.__calculate_converted_value(channel)

            except Exception as error:
                print(f"PT100 could not take data from {channel.name} using {channel.raw_file} \
                      {type(error).__name__} - {error}")
                continue

    def get_sensor_data(self):
        """ Get sensor data
            
        Returns:
            dictionary: containing the raw and input data from the sensor.
        """
        return self.__channels

    def get_sensor_raw_value_as_dict(self):
        """
        Return a dictionary with the name of channel as key
        and the raw_value as value
        """
        return {f'{channel.name}': channel.raw_value for channel in self.__channels}

    def __calculate_converted_value(self, channel: SensorData):
        rlead_min = int(self.__pt100_config["rlead_min"])
        rlead_max = int(self.__pt100_config["rlead_max"])
        rtd_min = int(self.__pt100_config["rtd_min"])
        rtd_max = int(self.__pt100_config["rtd_max"])
        min_temp = int(self.__pt100_config["min_temp"])
        max_temp = int(self.__pt100_config["max_temp"])
        rtd = self.__calculate_rtd(channel.raw_value)
        v_min = self.__calculate_vin(rlead_min, rtd_min)
        v_max = self.__calculate_vin(rlead_max, rtd_max)

        linear_const = self.__calculate_linear_interpolation_const(v_min, min_temp,
                                                                   v_max, max_temp)

        v_in = self.__calculate_vin((rlead_min + rlead_max)/2, rtd)

        print(f"**** PT100 Calculation ***** \
                RTD = {rtd}; \n \
                v_min = {v_min}; \n \
                v_max = {v_max}; \n \
                linear_const = {linear_const}; \n \
                v_in = {v_in}; \n \
                min_temp = {min_temp}\n")
        channel.value = min_temp + linear_const * (v_in - v_min)


    def __calculate_linear_interpolation_const(self, min_value: int, temp_min: int,
                                               max_value: int, temp_max: int) -> float:
        """
        Calculte the linear constant that could be different acording pt100 config
        Args:
            min (float): value (voltage or resistance) whean temperature reaches the minimal value
            temp_min (int): conifgured temperature minimal value in celsius
            max (float): value (voltage or resistance) whean temperature reaches the maximun value
            temp_max (int): conifgured temperature maximun value in celsius
        """
        return (temp_max - temp_min) / (max_value - min_value)
    
    def __calculate_vin(self, rlead: int , rtd: int) -> float:
        """
        Calculate the voltage when the temperature reaches the minimal
        V (MAX) = VREF + (Idac1 + Idac2) · Rlead + idac1 · (Rlead + Rrtd) 
        idac1 = idac2 = 500mV
        Args:
            rlead (float): Resistance value of the wire at determined temperature
            rtd (float): Resistance of the reference resistor at determined temperature

        Returns:
            float: the voltage at temperature
        """
        return (2500 + rlead + 0.5 * (rlead + rtd))

    def __calculate_rtd(self, raw_value: int) -> float:
        return ((2500 * raw_value)/ (2**22 * 8))

    def get_sensor_values_as_dict(self):
        """
        Return a dictionary with the name of channel as key
        and the converted value
        """
        return {f'{channel.name}': channel.value for channel in self.__channels}
