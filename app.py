#Importing packages and classes
from threading import Thread
import warnings
from appliances import Appliance
from flask import Flask,render_template,request,redirect,jsonify
import os
from logic import Logic,client1
from controller import Controller
import json

#Filtering out warnings
warnings.filterwarnings('ignore')
#Loading data files
filelist=os.listdir("data_file/")
#Creating appliance and backend instances
blender=Appliance(filelist[0])
coffee_maker=Appliance(filelist[1])
induction_cooker=Appliance(filelist[2])
air_fryer=Appliance(filelist[3])
kettle=Appliance(filelist[4])
oven=Appliance(filelist[5])
water_heater=Appliance(filelist[6])
fan=Appliance(filelist[7])
lamp=Appliance(filelist[8])
hair_dryer=Appliance(filelist[9])
#list of appliances object
appliance_list=[blender,coffee_maker,induction_cooker,air_fryer,kettle,
                oven,water_heater,fan,lamp,hair_dryer]

#Creating Control and Logic instances              
control=Controller(appliance_list)
lo=Logic(appliance_list)

#Creating threads for appliance power monitoring
blender_parameter=Thread(target=blender.get_Parameter)
coffee_maker_parameter=Thread(target=coffee_maker.get_Parameter)
induction_cooker_parameter=Thread(target=induction_cooker.get_Parameter)
air_fryer_parameter=Thread(target=air_fryer.get_Parameter)
kettle_parameter=Thread(target=kettle.get_Parameter)
oven_parameter=Thread(target=oven.get_Parameter)
water_heater_parameter=Thread(target=water_heater.get_Parameter)
fan_parameter=Thread(target=fan.get_Parameter)
lamp_parameter=Thread(target=lamp.get_Parameter)
hair_dryer_parameter=Thread(target=hair_dryer.get_Parameter)

#Creating threads for logic operations
getSumApparentPower=Thread(target=lo.getParameter)
getResult=Thread(target=lo.getEventDetection)
saveData=Thread(target=lo.saveData)


#topic for thingsboard telemetry
topic="v1/devices/me/telemetry"

#Defining Flask application
app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """Renders the main webpage template called "simulator.html".

    This function is the endpoint for the root URL ("/"). It handles both GET and POST
    requests. When a user accesses the root URL, the function renders the "simulator.html"
    template and returns it as an HTML response.

    Returns:
        html: The main webpage template rendered as an HTML response.
    """
    return render_template("simulator.html")


@app.route("/switch_on/<appliance>",methods=["GET"])
def switch_on(appliance:str):
    """
    The "/switch_on/<appliance>" route handles GET requests to switch on an appliance. 
    The switch_on function of the control object is called to switch on the specified appliance.
    A JSON response is returned indicating the appliance is turned on.

    Args:
        appliance (str): name of appliance

    Returns:
        json : appliance status
    """
    print(appliance)
    control.switch_on(appliance)
    return jsonify({"on":True})


@app.route("/switch_off/<appliance>",methods=["GET"])
def switch_off(appliance:str):
    """
    The "/switch_off/<appliance>" route handles GET requests to switch off an appliance. 
    The switch_off function of the control object is called to switch off the specified appliance. 
    A JSON response is returned indicating the appliance is turned off.

    Args:
        appliance (str): name of appliance

    Returns:
        json: appliance status
    """
    print(appliance)
    control.switch_off(appliance)
    return jsonify({"off":True})


@app.route('/chart',endpoint='chart')
def show_chart():
    return render_template('chart.html')

@app.route('/update_chart', methods=['POST'])
def update_chart():
    #switch_state = request.json.get('switch_state')  # Get the switch state from the request

    data = [lo.sumApparentPower,water_heater.apparent_power,oven.apparent_power,induction_cooker.apparent_power]

    return jsonify(data)




@app.before_request
def reset_state():
    """
    "Reset the state of all appliances and publish a message.

    This function is executed automatically before each request is processed by the application.
    It turns off multiple appliances and sends a message indicating that all appliances are off.
    """
    if request.endpoint == 'index':
        switch_off('blender')
        switch_off('coffee-maker')
        switch_off('induction-cooker')
        switch_off('air-fryer')
        switch_off('kettle')
        switch_off('oven')
        switch_off('water-heater')
        switch_off('fan')
        switch_off('lamp')
        switch_off('hair-dryer')
        client1.publish(topic,json.dumps({"appliance_active":"All Appliances are off"}))

    if request.endpoint == "chart":
        switch_off('blender')
        switch_off('coffee-maker')
        switch_off('induction-cooker')
        switch_off('air-fryer')
        switch_off('kettle')
        switch_off('oven')
        switch_off('water-heater')
        switch_off('fan')
        switch_off('lamp')
        switch_off('hair-dryer')


def run_flask():
    """This function starts all the threads for appliance power monitoring, backend operations, 
       and publishes a message indicating that all appliances are off. 
       The Flask application is run using app.run()
    """
    #appliance thread
    blender_parameter.start()
    coffee_maker_parameter.start()
    induction_cooker_parameter.start()
    air_fryer_parameter.start()
    kettle_parameter.start()
    oven_parameter.start()
    water_heater_parameter.start()
    fan_parameter.start()
    lamp_parameter.start()
    hair_dryer_parameter.start()
    saveData.start()
    #backend thread
    getSumApparentPower.start()
    getResult.start()
    #Initial message to appliance activation
    client1.publish(topic,json.dumps({"appliance_active":"All Appliances are off"}))
    #start flask app
    app.run(host="0.0.0.0",port=5000)


#main program
if __name__=="__main__":
    run_flask()