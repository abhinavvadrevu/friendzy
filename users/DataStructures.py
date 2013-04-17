"""
This class is used throughout models.py as a list implementation which Django is happy with.
"""

from django.db import models
import ast

##############
#  managers  #
##############


class DictyManager(models.Manager):
    def create_dicty(self, name):
        d = self.create(name=name)
        return d

class KeyValManager(models.Manager):
    def create_keyval(self, key, val):
        kv = self.create(key=key, value=val)
        return kv

##############
#  models  #
##############

class ListField(models.TextField):
    """
    List class
    """
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"
    
    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)
    
    def get_prep_value(self, value):
        if value is None:
            return value
        return unicode(value)
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class Dicty(models.Model):
    name      = models.CharField(max_length=50)
    
    objects = DictyManager()
    
    def appendkv(self,key, val):
        print 'APPENDED KEYVAL'
        print "appending key: " + key + ", value: " + val + " to: " + self.name
        kv = KeyVal()
        kv.key=key
        kv.value=val
        self.save()
        kv.container=self
        kv.save()
        self.save()
    def deletekey(self,key):
        try:
            key = KeyVal.objects.get(container=self,key=key)
        except KeyVal.DoesNotExist:
            print "TRIED TO DELETE KEY: "+key+" WHICH DOES NOT EXIST IN DICT: " + self.name
            return 
        except KeyVal.MultipleObjectsReturned: #SHOULD NEVER HAPPEN! ONLY USEFUL FOR DEBUGGING.
            key = KeyVal.objects.filter(container=self,key=key)[0]
        else:
            key.delete()
    
    def deletekeyval(self,key, val):
        try:
            keyval = KeyVal.objects.get(container=self,key=key, value=val)
        except KeyVal.DoesNotExist:
            print "TRIED TO DELETE KEY: "+key+" WHICH DOES NOT EXIST IN DICT: " + self.name
            return 
        except KeyVal.MultipleObjectsReturned: #SHOULD NEVER HAPPEN! ONLY USEFUL FOR DEBUGGING.
            keyval = KeyVal.objects.filter(container=self,key=key,value=val)[0]
        else:
            keyval.delete()

class KeyVal(models.Model):
    container = models.ForeignKey(Dicty)
    key       = models.CharField(max_length=240)
    value     = models.CharField(max_length=240)
    
    objects=KeyValManager()