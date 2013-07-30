#!/usr/bin/env python

import roslib
roslib.load_manifest('cob_hardware_test')
import sys
import rospy
import wx
from cob_hardware_test.srv import *
#from PyQt4 import QtGui, QtCore
from python_qt_binding import *
from python_qt_binding.QtGui import *

class MessageBox(QtGui.QWidget):
 
    def __init__ (self, parent=None):
        #super(MessageBox, self).__init__()
        #QtGui.QWidget.__init__(self, parent) 
        #self.setGeometry(300, 300, 250, 150)
        #self.setWindowTitle('Message Box')
        
        rospy.init_node('dialog_server')
        s = rospy.Service('dialog', Dialog, self.handle_dialog)
        print "Ready to ask(1) or confirm(0)!"
        
        rospy.spin()
        
            
    def handle_dialog(self, req):
        return DialogResponse(True)
    
        QtGui.QWidget.__init__(self, None) 
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Message Box')
        self.show()
        if req.type == 1:
                print "Asking: %s" % (req.message)
                reply = QtGui.QMessageBox.question(self,  'Message',  'Are you sure to quit?',  QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                        answer = True
                else:
                        answer = False

                return DialogResponse(answer)
    
        if req.type == 0:
                print "Confirm: %s" % (req.message)
                ex = wx.App()
                dial = wx.MessageDialog(None, req.message, 'Confirm',
                                wx.OK | wx.ICON_WARNING)
                ret = dial.ShowModal()
                if ret == wx.ID_OK:
                        answer = True
                else:
                        answer = False
    
            #TODO exit properly
            #self.Destroy()
            #ex.Destroy()        
            #dial.Destroy()
                return DialogResponse(answer)


if __name__ == "__main__":
    #dialog_server()
    app = QtGui.QApplication(sys.argv)
    qb = MessageBox()


    sys.exit(app.exec_())

