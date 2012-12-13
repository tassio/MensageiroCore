#-*- coding: utf-8 -*-
'''
Created on 25/07/2012

@author: tassio
'''

from PyQt4.QtGui import QIcon, QPixmap, QImage

import os
from settings import PROJECT_ROOT


class ResourceUtil(object):
    @staticmethod
    def getResource(resource):
        return os.path.join(PROJECT_ROOT, resource)

    @staticmethod
    def getIcon(resource):
        return QIcon(ResourceUtil.getResource(resource))

    @staticmethod
    def getPixmap(resource):
        return QPixmap(ResourceUtil.getResource(resource))

    @staticmethod
    def getImage(resource):
        return QImage(ResourceUtil.getResource(resource))

