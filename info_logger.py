''' This module contains all functions and setup required for the programs logging '''

# External Libraries
import os
import logging
import datetime
import csv

# My Modules
import variables

my_path = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename='logging/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log', level=logging.DEBUG)

def init():
    ''' This function creates a new log with current date time '''
    logging.info(' ')
    logging.info('------')
    logging.info('Start: %s', str(datetime.datetime.now()))

def decode_fourcc(v):
  v = int(v)
  return ''.join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

def camera_settings(camera, capture):
    ''' This function writes the camera settings to the log '''
    logging.debug(' ')
    logging.debug('Camera ' + str(camera) + ' Settings: ')
    for camera_setting in range(len(variables.CAMERA_VARIABLES)):
        cam_var =  str(variables.CAMERA_VARIABLES[camera_setting])
        cam_setting = str(capture.get(camera_setting))
        decode_cam = ''

        if variables.CAMERA_VARIABLES[camera_setting] == 'CAP_PROP_FOURCC':
            decode_cam = ' (' + str(decode_fourcc(capture.get(camera_setting))) + ')'

        logging.debug('\t' + cam_var + ' - ' + cam_setting + decode_cam)

def shutdown():
    ''' This function writes the shutdown information to the log '''
    logging.info('End: %s', str(datetime.datetime.now()))
    logging.info('------')
    logging.info(' ')