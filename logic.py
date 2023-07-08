from datetime import datetime
import joblib
import time
import numpy as np
import paho.mqtt.client as paho 
import json
import csv
from random import uniform

#load Machine Learning model
model=joblib.load('model062023.pkl')

#Thingsboard client authenthication parameter
tb_token="demo-test"
broker="demo.thingsboard.io"
port=1883
topic="v1/devices/me/telemetry"
#Instantiated paho client
client1=paho.Client()
#Connect the Thingsboard
client1.username_pw_set(tb_token)
client1.connect(broker,port,keepalive=60)



class Logic:
    """
    Performs logic calculations and controls appliances.

    This class represents a logical component that performs calculations based on appliance data and controls the appliances accordingly.

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
        queueApparentPower (list): A list to store the apparent power values for calculating relative value.
        relativePower (int): The relative power value.
        label (int): The label representing the predicted appliance.
        sumApparentPower (int): The sum of apparent power values.

    Methods:
        getSumParameter(): Calculate the sum of apparent power, third harmonics, and fifth harmonics.
        getQueueApparentPower(sumApparentPower): manages a queue of apparent power values by adding new values to the queue for every second.
        getAppliancesContributionandPowerFactor(sumApparentPower): calculates the contribution of the top 3 appliances (water heater, induction cooker, and oven) 
                                                    and the power factor based on the total apparent power.
        getEventDetection(): Perform event detection based on the difference in apparent power.
        sendResult(transient, diffValue): Send the detection result and predicted appliance.
        saveData(): Save the sum of apparent power and the label to a CSV file.
        check_appliance(): Check the status of the active appliances.
    """
    def __init__(self,appliance_list:list):
        """_summary_

        Args:
            appliance_list (_type_): _description_
        """
        
        self.blender=appliance_list[0]
        self.coffee_maker=appliance_list[1]
        self.induction_cooker=appliance_list[2]
        self.air_fryer=appliance_list[3]
        self.kettle=appliance_list[4]
        self.oven=appliance_list[5]
        self.water_heater=appliance_list[6]
        self.fan=appliance_list[7]
        self.lamp=appliance_list[8]
        self.hair_dryer=appliance_list[9]

        self.queueApparentPower=[]
        self.relativePower=0
        self.label=0
        self.sumApparentPower=0
        
    def getParameter(self):
        """Calculate the sum of apparent power, third harmonics, and fifth harmonics.
            This function also stream data to Thingsboard for every 1 second
        """
        while True:
            #list of apparent power
            apparent_power_list=[self.blender.apparent_power,self.coffee_maker.apparent_power,self.induction_cooker.apparent_power,
                                    self.air_fryer.apparent_power,self.kettle.apparent_power,self.oven.apparent_power,self.water_heater.apparent_power,
                                    self.fan.apparent_power,self.lamp.apparent_power,self.hair_dryer.apparent_power]
            #list of 3rd Harmonics
            third_harmonics_list=[self.blender.third_harmonics,self.coffee_maker.third_harmonics,self.induction_cooker.third_harmonics,
                                    self.air_fryer.third_harmonics,self.kettle.third_harmonics,self.oven.third_harmonics,self.water_heater.third_harmonics,
                                    self.fan.third_harmonics,self.lamp.third_harmonics,self.hair_dryer.third_harmonics]
            #list of 5th Harmonics
            fifth_harmonics_list=[self.blender.fifth_harmonics,self.coffee_maker.fifth_harmonics,self.induction_cooker.fifth_harmonics,
                                    self.air_fryer.fifth_harmonics,self.kettle.fifth_harmonics,self.oven.fifth_harmonics,self.water_heater.fifth_harmonics,
                                    self.fan.fifth_harmonics,self.lamp.fifth_harmonics,self.hair_dryer.fifth_harmonics]
            #list if rms current
            rms_current_list=[self.blender.rms_current,self.coffee_maker.rms_current,self.induction_cooker.rms_current,
                                    self.air_fryer.rms_current,self.kettle.rms_current,self.oven.rms_current,self.water_heater.rms_current,
                                    self.fan.rms_current,self.lamp.rms_current,self.hair_dryer.rms_current]
            
            #sum of the parameters
            sumApparentPower=sum(apparent_power_list)
            
            sumThirdHarmonics=sum(third_harmonics_list)
            
            sumFifthHarmonics=sum(fifth_harmonics_list)

            sumRMSCurrent=sum(rms_current_list)

            #add apparent power for to list  
            self.getQueueApparentPower(sumApparentPower)
                
            #get the Apparent Power for saving the data
            self.sumApparentPower=sumApparentPower
            #print the value
            print(sumApparentPower)
            print(sumThirdHarmonics)
            print(sumFifthHarmonics)
            print(sumRMSCurrent)
            print(self.queueApparentPower)

            #get the value of water
            water_heater_cont,induction_cooker_cont,oven_cont,pf=self.getAppliancesContributionandPowerFactor(sumApparentPower)

            #stream data to Thingsboard
            client1.publish(topic,json.dumps({"Apparent Power":sumApparentPower,"water_heater":water_heater_cont,
                                              "induction_cooker":induction_cooker_cont,"oven_cont":oven_cont,"ThirdHarm":sumThirdHarmonics,
                                              "FifthHarm":sumFifthHarmonics,"PF":pf,"RMS_Current":sumRMSCurrent,"WH_P":self.water_heater.apparent_power,
                                              "OV_P":self.oven.apparent_power,"Ind_P":self.induction_cooker.apparent_power}))

            time.sleep(1)
    
    def getQueueApparentPower(self,sumApparentPower:float):
        """
        Manage a queue of apparent power values.

        This function adds the given `sumApparentPower` to the queue, following certain conditions.

        Args:
            sumApparentPower (float): The new apparent power value to be added to the queue.
        """
        #if list size < 2, append the sumApparentPower
        if len(self.queueApparentPower)<2:
            self.queueApparentPower.append(sumApparentPower)

        #if list size > 2, remove the first index and append new sumApparentPower
        elif len(self.queueApparentPower)==2:
            self.queueApparentPower.pop(0)
            self.queueApparentPower.append(sumApparentPower)   

    
    def getAppliancesContributionandPowerFactor(self, sumApparentPower: float):
        """Calculate the contribution of top 3 appliances and power factor.

        This function calculates the contribution of the top 3 appliances (water heater, induction cooker, and oven) 
        and the power factor based on the given `sumApparentPower` value.

        Args:
            sumApparentPower (float): The total apparent power.

        Returns:
            Tuple[float, float, float, float]: A tuple containing the contribution of the top 3 appliances 
            (water heater, induction cooker, and oven) and the power factor.

        """
        # Initial conditions for top 3 appliances
        water_heater_cont = 0
        induction_cooker_cont = 0
        oven_cont = 0

        # Initial condition for power factor
        pf = 0

        # If sumApparentPower is not zero, calculate the contribution of the top 3 appliances
        if sumApparentPower != 0:
            water_heater_cont = self.water_heater.apparent_power / sumApparentPower
            induction_cooker_cont = self.induction_cooker.apparent_power / sumApparentPower
            oven_cont = self.oven.apparent_power / sumApparentPower

            # Generate a random power factor between 99.30 and 99.70
            pf = uniform(99.30, 99.70)
        else:
            pf = 0

        return water_heater_cont, induction_cooker_cont, oven_cont, pf



    def getEventDetection(self):
        """
        Perform event detection based on the difference in apparent power.

        This method continuously checks for new apparent power values in the queue and 
        calculates the difference between the latest two values.
        If the absolute difference is greater than 80 and the difference is negative, 
        it calls the `sendResult` method with transient=0 and the difference value.
        If the absolute difference is greater than 80 and the difference is positive, 
        it calls the `sendResult` method with transient=1 and the difference value.

        This method runs in an infinite loop and pauses for 1 second between iterations.
        """
        while True:
            #check the size queueApparentPower list
            counters=len(self.queueApparentPower)

            # The calculation only start if the counters==2
            if counters==2:
                #calculate the difference of VA(t)-VA(t-1)
                diffValue = self.queueApparentPower[1] - self.queueApparentPower[0]
                
                #reshape the diffValue (float) to array with dimension (1,-1). This value will be feed 
                # to ML model. The value also absolute because the model is trained with positive value
                diffValueArr=np.asarray(abs(diffValue)).reshape(1,-1)

                #check the value of diffValue
                #if diffValue is more than 80 sendResult function is called and if diffValue<0
                #it indicate the switch off appliance occur
                if abs(diffValue)>80 and diffValue<0:
                    self.sendResult(0,diffValueArr)
                    
                #if diffValue is more than 80 sendResult function is called and if diffValue>0
                #it indicate the switch off appliance occur
                elif abs(diffValue)>80 and diffValue>0:
                    self.sendResult(1,diffValueArr)
                
            #1 second delay
            time.sleep(1)
    

    def sendResult(self, transient: int, diffValue: float):
        """Process and publish the result of an event detection.

        Args:
            transient (int): The type of transient (0 for OFF, 1 for ON).
            diffValue (float): The difference value used for prediction.
        """

        # Predict the appliance based on the difference value
        appliance_predict = model.predict(diffValue)
        appliance_predict = int(appliance_predict[0])

        # Print the transient type and predicted appliance
        print(transient)
        print(appliance_predict)

        # Update the label based on the predicted appliance
        if self.sumApparentPower != 0:
            self.label = appliance_predict
        else:
            self.label = 0

        # Define a mapping of transient types
        appliance_transient = {1: "ON", 0: "OFF"}

        # Define a mapping of appliance names
        appliance_result = {1: "Blender", 2: "Coffee Maker", 3: "Induction Cooker", 4: "Air Fryer",
                            5: "Kettle", 6: "Oven", 7: "Water Heater", 10: "An Appliance"}

        # Get the current timestamp
        str_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

        # Create a log message with appliance information
        message = {
            "Log": appliance_result[appliance_predict] + " " + "is switched " + appliance_transient[transient],
            "Time": str_time,
            "Relative Power": int(diffValue[0])
        }

        # Publish the log message to the topic
        client1.publish(topic, json.dumps(message))

        # Update the active appliances
        time.sleep(0.5)
        self.check_appliance()

    
    def saveData(self):
        """
        Continuously save the values of sumApparentPower and label to a CSV file.

        The function opens a CSV file named "save_power.csv" in append mode and writes
        a new row with the current values of sumApparentPower and label. The function
        sleeps for 4 seconds before repeating the process.
        """
        while True:
            # Open the CSV file in append mode
            with open("save_power.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                # Write a new row with the current values of sumApparentPower and label
                writer.writerow([self.sumApparentPower, self.label])
            # Sleep for 4 seconds
            time.sleep(4)

    def check_appliance(self):
        """
        Check the status of appliances and publish the active appliance information.

        The function initializes an empty list called app_active and sets the initial value
        of appliance_active to "All Appliances are off". It then checks the status of each
        appliance (blender, coffee_maker, induction_cooker, air_fryer, kettle, oven,
        water_heater, fan, lamp, hair_dryer) by accessing their switch_status attributes.

        If an appliance is switched on, its name is added to the app_active list. If any
        of the fan, lamp, or hair_dryer are switched on, "Other" is also added to the list.

        If the app_active list is empty, it means that all appliances are off, and the
        message "All Appliances are off" is printed and published to the specified topic.

        If "Other" is present in the app_active list, it checks whether the list only
        contains "Other". If it does, appliance_active is set to "Others". Otherwise, it
        removes "Other" from the list and joins the remaining appliance names with "+" and
        appends "+Others" to the end.

        Finally, the appliance_active information is packaged in a dictionary called
        apps_active and published to the specified topic.

        """
        app_active = []
        appliance_active = "All Appliances are off"

        blender_status = self.blender.switch_status
        coffee_maker_status = self.coffee_maker.switch_status
        induction_cooker_status = self.induction_cooker.switch_status
        air_fryer_status = self.air_fryer.switch_status
        kettle_status = self.kettle.switch_status
        oven_status = self.oven.switch_status
        water_heater_status = self.water_heater.switch_status
        fan_status = self.fan.switch_status
        lamp_status = self.lamp.switch_status
        hair_dryer_status = self.hair_dryer.switch_status

        if blender_status:
            app_active.append("Blender")
        if coffee_maker_status:
            app_active.append("Coffee Maker")
        if induction_cooker_status:
            app_active.append("Induction Cooker")
        if air_fryer_status:
            app_active.append("Air Fryer")
        if kettle_status:
            app_active.append("Kettle")
        if oven_status:
            app_active.append("Oven")
        if water_heater_status:
            app_active.append("Water Heater")
        if fan_status or lamp_status or hair_dryer_status:
            app_active.append("Other")


        if app_active == []:
            print("All Appliances are off")
            appliance_active = "All Appliances are off"
            client1.publish(topic, json.dumps({"appliance_active": appliance_active}))

        elif "Other" in app_active:
            if list(set(app_active)) == ['Other']:
                appliance_active = "Others"
            else:
                app_active.remove("Other")
                appliance_active = "+".join(app_active) + "+Others"
        else:
            appliance_active = "+".join(app_active)

        apps_active = {"appliance_active": appliance_active}

        client1.publish(topic, json.dumps(apps_active))






          
                
    

