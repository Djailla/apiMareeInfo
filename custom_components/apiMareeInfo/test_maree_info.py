import json
import apiMareeInfo
import sensorApiMaree


def testPort():

    # with open("../../Tests/json/SJM.json") as f:
    #     data = json.load(f)

    _myMaree = apiMareeInfo.ApiMareeInfo()
    lat, lng = "46.7711", "-2.05306"
    lat, lng = "46.4967", "-1.79667"
    _myMaree.setport(lat, lng)
    # _myMaree.getInformationPort( outfile = "file.json" )
    _myMaree.getinformationport()
    print(_myMaree.getinfo())
    print(_myMaree.getnomduport())
    print(_myMaree.getdatecourante())
    _sAM = sensorApiMaree.manageSensorState()
    _sAM.init(_myMaree)
    state, attributes = _sAM.getstatus()
    sensorApiMaree.logSensorState(attributes)


def testListePorts():
    _myPort = apiMareeInfo.ListePorts()
    a = _myPort.getlisteport("olonne")
    print(a)


testPort()
testListePorts()
