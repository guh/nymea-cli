# -*- coding: UTF-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                         #
#  Copyright (C) 2016 Simon Stuerz <simon.stuerz@guh.guru>                #
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
import selector

        
def list_configurations():
    params = {}
    response = guh.send_command("Configuration.GetConfigurations", params)
    guh.print_json_format(response['params'])
        
        
def list_timezones():
    params = {}
    response = guh.send_command("Configuration.GetTimeZones", params)
    guh.print_json_format(response['params'])

def set_timezone():
    params = {}
    timeZones = []
    timeZones = get_timezones()
    selection = guh.get_selection("Please select one of following allowed values:", timeZones)
    if selection == None:
        return None
         
    params['timeZone'] = timeZones[selection]
    response = guh.send_command("Configuration.SetTimeZone", params)
    guh.print_json_format(response['params'])


def set_serverName():
    params = {}         
    params['serverName'] = raw_input("Please enter the server name:")
    response = guh.send_command("Configuration.SetServerName", params)
    guh.print_json_format(response['params'])


def get_timezones():
    params = {}
    response = guh.send_command("Configuration.GetTimeZones", params)
    return response['params']['timeZones']


def configure_tcpServer():
    params = {}
    params['host'] = raw_input("\nEnter the \"host\" of the TCP server (default \"0.0.0.0\"): ")
    params['port'] = raw_input("\nEnter the \"port\" of the TCP server (default 2222): ")
    response = guh.send_command("Configuration.SetTcpServerConfiguration", params)
    guh.print_json_format(response['params'])

def cloud_authenticate():
    params = {}
    params['username'] = raw_input("\nEnter the \"username\" of your cloud account: ")
    params['password'] = raw_input("\nEnter the \"password\" of your cloud account: ")
    response = guh.send_command("Cloud.Authenticate", params)
    guh.print_cloud_error_code(response['params']['cloudError'])
    
    
def print_cloud_status():
    params = {}
    response = guh.send_command("Cloud.GetConnectionStatus", params)
    guh.print_json_format(response['params'])

    
def enable_cloud_connection():
    params = {}
    response = guh.send_command("Cloud.Enable", params)
    guh.print_json_format(response['params'])


def disable_cloud_connection():
    params = {}
    response = guh.send_command("Cloud.Disable", params)
    guh.print_json_format(response['params'])
    

