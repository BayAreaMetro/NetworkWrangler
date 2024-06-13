import os, sys
from .Faresystem import Faresystem
from .Linki import Linki
from .Network import Network
from .NetworkException import NetworkException
from .PTSystem import PTSystem
from .PNRLink import PNRLink
from .Supplink import Supplink

# add ..\_static for dataTable import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..","_static"))) # for dataTable

from .TransitAssignmentData import TransitAssignmentData ##
from .TransitCapacity import TransitCapacity
from .TransitLine import TransitLine
from .TransitLink import TransitLink
from .TransitNetwork import TransitNetwork
from .TransitParser import TransitParser
from .HighwayNetwork import HighwayNetwork
from .Logger import setupLogging, WranglerLogger
from .Node import Node
from .HwySpecsRTP import HwySpecsRTP


__all__ = ['NetworkException', 'setupLogging', 'WranglerLogger',
           'Network', 'TransitAssignmentData', 'TransitNetwork', 'TransitLine', 'TransitParser',
           'Node', 'TransitLink', 'Linki', 'PNRLink', 'Supplink', 'HighwayNetwork', 'HwySpecsRTP',
           'TransitCapacity', 'Faresystem', 'PTSystem'
]


if __name__ == '__main__':

    LOG_FILENAME = "Wrangler_main_%s.info.LOG" % time.strftime("%Y%b%d.%H%M%S")
    setupLogging(LOG_FILENAME, LOG_FILENAME.replace("info", "debug"))
    
    net = Network()
    net.cloneAndApplyProject(projectname="Muni_TEP")    
    net.cloneAndApplyProject(projectname="Muni_CentralSubway", tag="1-latest", modelyear=2030)
    net.cloneAndApplyProject(projectname="BART_eBART")    

    net.write(name="muni", writeEmptyFiles=False)
