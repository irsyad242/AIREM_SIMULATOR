import pandas as pd
import time

class Appliance:
    """
    Represents an appliance.

    This class represents an appliance and provides methods to retrieve its parameters based on the switch status.

    Attributes:
        __appliance (DataFrame): The appliance data read from a CSV file.
        __all_apparent_power (array): Array containing all the apparent power values.
        __all_third_harmonics (array): Array containing all the third harmonics values.
        __all_fifth_harmonics (array): Array containing all the fifth harmonics values.
        __all_power_factor (array): Array containing all the power factor values.
        __all_rms_current (array): Array containing all rms current values
        apparent_power (float): The current apparent power of the appliance.
        switch_status (bool): The switch status of the appliance.

    Methods:
        get_Parameter(): Get the parameters of the appliance based on the switch status.
        
    """
    def __init__(self, path: str):
        """
        Initialize an Appliance object.

        Args:
            path (str): The path to the data file.
        """
        self.__appliance = pd.read_csv("data_file/" + path)
        self.__all_apparent_power = self.__appliance.iloc[:, 0].values
        self.__all_third_harmonics = self.__appliance.iloc[:, 1].values
        self.__all_fifth_harmonics = self.__appliance.iloc[:, 2].values
        self.__all_power_factor = self.__appliance.iloc[:, 3].values
        self.__all_rms_current=self.__appliance.iloc[:,4].values
        self.apparent_power = 0
        self.switch_status = False

    def get_Parameter(self):
        """
        Get the parameters of the appliance.

        This method retrieves the parameters of the appliance based on the switch status.

        """
        i = 0

        while True:
            if self.switch_status:
                self.apparent_power = self.__all_apparent_power[i]
                self.third_harmonics = self.__all_third_harmonics[i]
                self.fifth_harmonics = self.__all_fifth_harmonics[i]
                self.power_factor = self.__all_power_factor[i]
                self.rms_current=self.__all_rms_current[i]
                i += 1
                if i == len(self.__all_apparent_power):
                    i = 0
            else:
                self.apparent_power = 0
                self.third_harmonics = 0
                self.fifth_harmonics = 0
                self.power_factor = 0
                self.rms_current=0
                i = 0

            time.sleep(1)  # Delay for 1 second to control the rate of parameter retrieval
