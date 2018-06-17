#!/usr/bin/python
# Authoer: Spencer.Luo
# Date: 5/27/2018

# Version 1.0
#=======================================================================================================================
# class PowerBank:
#     "移动电源"
#
#     def __init__(self, serialNum, electricQuantity):
#         self.__serialNum = serialNum
#         self.__electricQuantity = electricQuantity
#         self.__user = ""
#
#     def getSerialNum(self):
#         return self.__serialNum
#
#     def getElectricQuantity(self):
#         return self.__electricQuantity
#
#     def setUser(self, user):
#         self.__user = user
#
#     def getUser(self):
#         return self.__user
#
#     def showInfo(self):
#         print("序列号:" + str(self.__serialNum) + "  电量:" + str(self.__electricQuantity) + "%  使用者:" + self.__user)


class ObjectPack:
    "对象的包装类，封装指定的对象(如充电宝)是否被使用中"
    def __init__(self, obj, inUsing = False):
        self.__obj = obj
        self.__inUsing = inUsing

    def inUsing(self):
        return self.__inUsing

    def setUsing(self, isUsing):
        self.__inUsing = isUsing

    def getObj(self):
        return self.__obj

class PowerBankBox:
    "存放移动电源的智能箱盒"

    def __init__(self):
        self.__pools = {}
        self.__pools["0001"] = ObjectPack(PowerBank("0001", 100))
        self.__pools["0002"] = ObjectPack(PowerBank("0002", 100))

    def borrow(self, serialNum):
        "使用移动电源"
        item = self.__pools.get(serialNum)
        result = None
        if(item is None):
            print("没有可用的电源！")
        elif(not item.inUsing()):
            item.setUsing(True)
            result = item.getObj()
        else:
            print(str(serialNum) + "电源已被借用！")
        return result

    def giveBack(self, serialNum):
        "归还移动电源"
        item = self.__pools.get(serialNum)
        if(item is not None):
            item.setUsing(False)
            print(str(serialNum) + "电源已归还!")

# Version 2.0
#=======================================================================================================================
# 代码框架
#==============================
from abc import ABCMeta, abstractmethod
# 引入ABCMeta和abstractmethod来定义抽象类和抽象方法
import logging
# 引入logging模块用于输出日志信息
import time
# 引入时间模块

class PooledObject:
    "池对象,也称池化对象"

    def __init__(self, obj):
        self.__obj = obj
        self.__busy = False

    def getObject(self):
        return self.__obj

    def setObject(self, obj):
        self.__obj = obj

    def isBusy(self):
        return self.__busy

    def setBusy(self, busy):
        self.__busy = busy


class ObjectPool(metaclass=ABCMeta):
    "对象池"

    "对象池初始化大小"
    InitialNumOfObjects = 10
    "对象池最大的大小"
    MaxNumOfObjects = 50

    def __init__(self):
        self.__pools = []
        for i in range(0, ObjectPool.InitialNumOfObjects):
            obj = self.createPooledObject()
            self.__pools.append(obj)

    @abstractmethod
    def createPooledObject(self):
        "子类提供创建对象的方法"
        pass

    def borrowObject(self):
        # 如果找到空闲对象，直接返回
        obj = self._findFreeObject()
        if(obj is not None):
            logging.info("%s对象已被借用, time:%d", id(obj), time.time())
            return obj

        # 如果对象池未满，则添加新的对象
        if(len(self.__pools) < ObjectPool.MaxNumOfObjects):
            pooledObj = self.addObject()
            if (pooledObj is not None):
                pooledObj.setBusy(True)
                logging.info("%s对象已被借用, time:%d", id(pooledObj.getObject()), time.time())
                return pooledObj.getObject()

        # 对象池已满且没有空闲对象，则返回None
        return None

    def returnObject(self, obj):
        for pooledObj in self.__pools:
            if(pooledObj.getObject() == obj):
                pooledObj.setBusy(False)
                logging.info("%s对象已归还, time:%d", id(pooledObj.getObject()), time.time())
                break


    def addObject(self):
        obj = None
        if(len(self.__pools) < ObjectPool.MaxNumOfObjects):
            obj = self.createPooledObject()
            self.__pools.append(obj)
            logging.info("添加新对象%s, time:%d", id(obj), time.time())
        return obj

    def clear(self):
        self.__pools.clear()

    def _findFreeObject(self):
        "查找空闲的对象"
        obj = None
        for pooledObj in self.__pools:
            if(not pooledObj.isBusy()):
                obj = pooledObj.getObject()
                pooledObj.setBusy(True)
                break
        return obj



# 基于框架的实现
#==============================
class PowerBank:
    "移动电源"

    def __init__(self, serialNum, electricQuantity):
        self.__serialNum = serialNum
        self.__electricQuantity = electricQuantity
        self.__user = ""

    def getSerialNum(self):
        return self.__serialNum

    def getElectricQuantity(self):
        return self.__electricQuantity

    def setUser(self, user):
        self.__user = user

    def getUser(self):
        return self.__user

    def showInfo(self):
        print("序列号:%03d  电量:%d%%  使用者:%s" % (self.__serialNum, self.__electricQuantity, self.__user))

class PowerBankPool(ObjectPool):

    __serialNum = 0

    @classmethod
    def getSerialNum(cls):
        cls.__serialNum += 1
        return cls.__serialNum


    def createPooledObject(self):
        powerBank = PowerBank(PowerBankPool.getSerialNum(), 100)
        return PooledObject(powerBank)

# Test
#=======================================================================================================================
def testPowerBank():
    box = PowerBankBox()
    powerBank1 = box.borrow("0001")
    if(powerBank1 is not None):
        powerBank1.setUser("Tony")
        powerBank1.showInfo()
    powerBank2 = box.borrow("0002")
    if(powerBank2 is not None):
        powerBank2.setUser("Sam")
        powerBank2.showInfo()
    powerBank3 = box.borrow("0001")
    box.giveBack("0001")
    powerBank3 = box.borrow("0001")
    if(powerBank3 is not None):
        powerBank3.setUser("Aimee")
        powerBank3.showInfo()


def testObjectPool():
    powerBankPool = PowerBankPool()
    powerBank1 = powerBankPool.borrowObject()
    if (powerBank1 is not None):
        powerBank1.setUser("Tony")
        powerBank1.showInfo()
    powerBank2 = powerBankPool.borrowObject()
    if (powerBank2 is not None):
        powerBank2.setUser("Sam")
        powerBank2.showInfo()
    # powerBank3 = powerBankPool.borrowObject()
    powerBankPool.returnObject(powerBank1)
    powerBank3 = powerBankPool.borrowObject()
    if (powerBank3 is not None):
        powerBank3.setUser("Aimee")
        powerBank3.showInfo()

class Person:
    height = 152

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

def testObj():
    p1 = Person("Spanecer", 22)
    p2 = Person("Spanecer", 22)
    print(p1.height)
    p1.height = 160
    print(p2.height)
    a = "I'm %s. I'm %04d year old" % ('Vamei', 99)
    print(a)
    print("I'm %(name)s. I'm %(age)d year old" % {'name': 'Vamei', 'age': 99})

# testPowerBank()
testObjectPool()
# testObj()
