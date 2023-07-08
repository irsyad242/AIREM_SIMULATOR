document.getElementById("kettle-off").classList.add("button-disabled")
document.getElementById("water-heater-off").classList.add("button-disabled")
document.getElementById("blender-off").classList.add("button-disabled")
document.getElementById("coffee-maker-off").classList.add("button-disabled")
document.getElementById("induction-cooker-off").classList.add("button-disabled")
document.getElementById("air-fryer-off").classList.add("button-disabled")
document.getElementById("fan-off").classList.add("button-disabled")
document.getElementById("lamp-off").classList.add("button-disabled")
document.getElementById("hair-dryer-off").classList.add("button-disabled")
document.getElementById("oven-off").classList.add("button-disabled")

function turnOn(appliance) {
    $.get(`/switch_on/${appliance}`,function(){
    document.getElementById(appliance + "-on").classList.add("button-disabled");
    document.getElementById(appliance + "-off").classList.remove("button-disabled");
    document.getElementById(appliance + "-off").disabled = false;
    })
}


function turnOff(appliance) {
    $.get(`/switch_off/${appliance}`,function(){
        document.getElementById(appliance + "-off").classList.add("button-disabled");
        document.getElementById(appliance + "-on").classList.remove("button-disabled");
        document.getElementById(appliance + "-on").disabled = false;
    })
}
