# -*- coding: UTF-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                         #
#  Copyright (C) 2015-2018 Simon Stuerz <simon.stuerz@guh.io>             #
#                                                                         #
#  This file is part of guh-cli.                                          #
#                                                                         #
#  guh-cli is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, version 2 of the License.                #
#                                                                         #
#  guh-cli is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with guh. If not, see <http://www.gnu.org/licenses/>.            #
#                                                                         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import guh
import devices
import parameters

def get_actionType(actionTypeId):
    params = {}
    params['actionTypeId'] = actionTypeId
    response = guh.send_command("Actions.GetActionType", params)
    if not 'actionType' in response['params']:
        return None
    return response['params']['actionType']


def get_actionTypes(deviceClassId):
    params = {}
    params['deviceClassId'] = deviceClassId
    return guh.send_command("Devices.GetActionTypes", params)['params']['actionTypes']


def create_actions():
    enough = False
    actions = []
    while not enough:
        print "\n========================================================"
        raw_input("-> Press \"enter\" to create actions!  ")
        deviceId = devices.select_configured_device()
        if not deviceId:
            return None
        device = devices.get_device(deviceId)
        actionType = select_actionType(device['deviceClassId'])
        if not actionType:
            continue
        params = parameters.read_params(actionType['paramTypes'])
        action = {}
        action['deviceId'] = deviceId
        action['actionTypeId'] = actionType['id']
        if len(params) > 0:
            action['params'] = params
        actions.append(action)
        input = raw_input("Do you want to add another action? (y/N): ")
        if not input == "y":
            enough = True            
    return actions


def execute_action():
    deviceId = devices.select_configured_device()
    if deviceId == None:
        return None
    device = devices.get_device(deviceId)
    actionType = select_actionType(device['deviceClassId'])
    #print guh.print_json_format(actionType)
    if actionType == None:
        print "\n    This device has no actions"
        return None
    actionTypeId = actionType['id']
    params = {}
    params['actionTypeId'] = actionTypeId
    params['deviceId'] = deviceId
    actionType = get_actionType(actionTypeId)
    actionParams = parameters.read_params(actionType['paramTypes'])
    params['params'] = actionParams
    response = guh.send_command("Actions.ExecuteAction", params)
    if response:  
        guh.print_device_error_code(response['params']['deviceError'])
    
    
def select_actionType(deviceClassId):
    actions = get_actionTypes(deviceClassId)
    if not actions:
        return None
    actionList = []
    #print "got actions", actions
    for i in range(len(actions)):
        #print "got actiontype", actions[i]
        actionList.append(actions[i]['displayName'])
    selection = guh.get_selection("Please select an action type:", actionList)
    if selection != None:
        return actions[selection]
    return None


def print_actionList(actionList):
    for i in range(len(actionList)):
        action = actionList[i]
        device = devices.get_device(action['deviceId'])
        actionType = get_actionType(actionList[i]['actionTypeId'])
        actionParams = actionList[i]['params']
        print  "%5s. ->  %40s -> action: \"%s\"" %(i, device['name'], actionType['displayName'])
        for i in range(len(actionParams)):
            print "%50s: %s" %(actionParams[i]['displayName'], actionParams[i]['value'])


def print_actionType():
    deviceId = devices.select_configured_device()
    if deviceId == None:
        return None
    device = devices.get_device(deviceId)
    actionType = select_actionType(device['deviceClassId'])
    #print guh.print_json_format(actionType)
    if actionType == None:
        print "\n    This device has no actions"
        return None
    actionType = get_actionType(actionType['id'])
    guh.print_json_format(actionType)



