#!/usr/bin/python3
import subprocess


class Controller:
    def __init__(self):
        self._params = {}
        self._params['infector_executable'] = ""
        self._params['source_file'] = ""
        self._params['destination_file'] = ""
        self._params['payload_file'] = ""
        self._params['method'] = "code"
        self._params['thread'] = False

    def setParams(self, args):
        self._params['infector_executable'] = args['infector_executable']
        self._params['source_file'] = args['source_file']
        self._params['destination_file'] = args['destination_file']
        self._params['payload_file'] = args['payload_file']
        self._params['method'] = args['method']
        self._params['thread'] = args['thread']

    def getParams(self):
        return self._params

    def generate(self):
        ret = 0
        #create cmd line and exec it
        cmd_options = [
             self._params['infector_executable'], "-i", self._params['source_file'],
             "-o", self._params['destination_file'], "-s", self._params['payload_file'],
             "-m", self._params['method']
            ]

        if self._params['thread']:
            cmd_options.append("-t")
        ret = self.__signed8(subprocess.run(cmd_options).returncode)

        return ret

    def __signed8(self, x):
        return (x - (1 << 8)) if ((x > 0) and (x < (1 << 8))) else x
