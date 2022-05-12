"""data acquisition for a 360° panorama scan with 600Khz 
"""
from projectservice import ProjectService
from scannerservice import ScannerService, RectScanPattern
from controlservice import ControlService
from threading import Event

def onDataAcquisitionFinished(arg0):
    if arg0 == ControlService.RC_SUCCESS:
        print("Data acquisition succeeded.")
    elif arg0 == ControlService.RC_CANCELED:
        print("Data acquisition canceled.")
    elif arg0 == ControlService.RC_ERROR:
        print("Data acquisition failed.")
    finishedEvent.set()
    
finishedEvent = Event()
projSvc= ProjectService("localhost: 20000")
scanSvc= ScannerService("localhost: 20000")
ctrlSvc= ControlService("localhost: 20000")

ctrlSvc.acquisitionFinished().connect(onDataAcquisitionFinished)

projSvc.createProject("myProject")
projSvc.loadProject("myProject")
projSvc.createScanposition("ScanPos001")
projSvc.selectScanposition("ScanPos001")

scanPattern= RectScanPattern()
scanPattern.thetaStart= 30.0
scanPattern.thetaStop= 130.0
scanPattern.thetaIncrement= 0.04
scanPattern.phiStart= 0.0
scanPattern.phiStop= 360.0
scanPattern.phiIncrement= 0.04
scanSvc.setRectScan(scanPattern,1)
scanSvc.setMeasurementProgram(2) #600Khz
 
ctrlSvc.startAcquisition(False, True, False, False)

finishedEvent.wait()

acqInfo= ctrlSvc.lastAcquisition()
if not acqInfo.success:
    print(acqInfo.errorMessage)
    