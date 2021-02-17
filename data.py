import numpy as np
import matplotlib.pyplot as pl

def quaternion(quat):
    '''四元数用四阶矩阵表达'''
    a,b,c,d = quat
    Q = np.array([[a,-b,d,c],
        [b,a,-c,-d],
        [-d,c,a,-b],
        [c,d,b,a]])
    return Q


def rotate(vector,quat):
    '''旋转'''
    ro = []
    for i in range(0,len(vector)):
        vector[i].insert(0,0)
        W = quaternion(vector[i])
        Q = quaternion(quat[i])
        v = np.dot(Q,np.dot(W,np.linalg.inv(Q)))
        a,b,c,d = v[0]
        ro.append([-b,c,d])
    return ro


def integral(accumulated):
    '''积分'''
    time = 0.01
    inte = [0]
    for point in accumulated:
        inte.append(inte[-1] + point * time)
    del inte[0]
    return inte


def filtering(datas):
    '''滤波'''
    count ,sumx,sumy,sumz = 0,0,0,0
    result = []
    for x,y,z in datas:
        if count != 5:
            count += 1
            sumy += y
            sumx += x
            sumz += z
        else:
            result.append([sumx / 5,sumy / 5,sumz / 5])
            count ,sumx,sumy,sumz = 0,0,0,0
    if count:
        result.append([sumx / count,sumy / count,sumz / count])
    return result


class InertialData:
    def __init__(self, filename):
            with open(filename,'r',encoding = "utf-8")as f_data:
                lines = f_data.readlines()
                self.acc,self.gyr,self.mag,quat = [],[],[],[]
                for line in lines:
                    tmp = list(map(float,line.split()))
                    self.acc.append(tmp[2:5])
                    self.gyr.append(tmp[5:8])
                    self.mag.append(tmp[8:11])
                    quat.append(tmp[11:15])
                self.acc = rotate(self.acc,quat)
                self.gyr = rotate(self.gyr,quat)
                self.mag = rotate(self.mag,quat)

    def filtering_acc(self):
        self.acc = filtering(self.acc)

    def filtering_gyr(self):
        self.gyr = filtering(self.gyr)

    def filtering_acc(self):
        self.mag = filtering(self.mag)
        
    def get_gyr(self):
        return self.gyr

    def get_acc(self):
        return self.acc

    def get_mag(self):
        return self.mag

    def draw_acc(self):
        accx,accy,accz = [],[],[]
        for x,y,z in self.acc:
            accx.append(x)
            accy.append(y)
            accz.append(z)
        pl.figure('acc_x')
        pl.plot(np.array(accx))
        pl.figure('acc_y')
        pl.plot(np.array(accy))
        pl.figure('acc_z')
        pl.plot(np.array(accz))
        pl.show()
