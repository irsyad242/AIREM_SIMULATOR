from tapo import*
from tapo_plug import tapoPlugApi


class Controller:
    """Manages a list of appliances.

    This class represents a controller that manages a list of appliances. 
    Some of the attributes are integrated with Tapo smart plug api

    Attributes:
        blender (Appliance): The blender appliance.
        coffee_maker (Appliance): The coffee maker appliance.
        induction_cooker (Appliance): The induction cooker appliance.
        air_fryer (Appliance): The air fryer appliance.
        kettle (Appliance): The kettle appliance.
        oven (Appliance): The oven appliance.
        water_heater (Appliance): The water heater appliance.
        fan (Appliance): The fan appliance.
        lamp (Appliance): The lamp appliance.
        hair_dryer (Appliance): The hair dryer appliance.

    Methods:
        switch_on(appliance: str): Switch on the specified appliance.
        switch_off(appliance: str): Switch off the specified appliance.
    """
    
    def __init__(self, appliance_list:list):
        """Initialize a Controller object.

        Args:
            appliance_list (list): A list of Appliance objects.
        """
        self.blender = appliance_list[0]
        self.coffee_maker = appliance_list[1]
        self.induction_cooker = appliance_list[2]
        self.air_fryer = appliance_list[3]
        self.kettle = appliance_list[4]
        self.oven = appliance_list[5]
        self.water_heater = appliance_list[6]
        self.fan = appliance_list[7]
        self.lamp = appliance_list[8]
        self.hair_dryer = appliance_list[9]

    def switch_on(self, appliance: str):
        """Switch on the specified appliance.

        Args:
            appliance (str): The name of the appliance to switch on.
        """
        appliances = {
            "blender": self.blender,
            "coffee-maker": self.coffee_maker,
            "induction-cooker": self.induction_cooker,
            "air-fryer": self.air_fryer,
            "kettle": self.kettle,
            "oven": self.oven,
            "water-heater": self.water_heater,
            "fan": self.fan,
            "lamp": self.lamp,
            "hair-dryer": self.hair_dryer
        }

         # if the appliance is one of them tapo plug will switch on

        # if appliance == "kettle":
        #     tapoPlugApi.plugOn(plug1)

        # if appliance == "air-fryer":
        #     tapoPlugApi.plugOn(plug2)

        # if appliance == "fan":
        #     tapoPlugApi.plugOn(plug3)


        #turn the appliance switch_status to True
        appliances[appliance].switch_status = True

    def switch_off(self, appliance: str):
        """Switch off the specified appliance.

        Args:
            appliance (str): The name of the appliance to switch off.
        """
        appliances = {
            "blender": self.blender,
            "coffee-maker": self.coffee_maker,
            "induction-cooker": self.induction_cooker,
            "air-fryer": self.air_fryer,
            "kettle": self.kettle,
            "oven": self.oven,
            "water-heater": self.water_heater,
            "fan": self.fan,
            "lamp": self.lamp,
            "hair-dryer": self.hair_dryer
        }

        # if the appliance is one of them tapo plug will switch off
        # if appliance=="kettle":
        #     tapoPlugApi.plugOff(plug1)

        # if appliance=="air-fryer":
        #     tapoPlugApi.plugOff(plug2)
        
        # if appliance=="fan":
        #     tapoPlugApi.plugOff(plug3)
        
        #turn the appliance switch_status to False
        appliances[appliance].switch_status=False

    

    
