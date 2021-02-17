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
    '''坐标系转换'''
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
                acc,gyr,mag,quat = [],[],[],[]
                for line in lines:
                    tmp = list(map(float,line.split()))
                    acc.append(tmp[2:5])
                    gyr.append(tmp[5:8])
                    mag.append(tmp[8:11])
                    quat.append(tmp[11:15])
            self.data = {'acc':rotate(acc,quat),'gyr':rotate(gyr,quat),'mag':rotate(mag,quat)}
    
    def filtering(self,label):        
        self.data[label] = filtering(self.data[label])
        
    def get(self,label):
        return self.data[label]

    def draw(self,label):
        x_axis,y_axis,z_axis = [],[],[]
        for x,y,z in self.data[label]:
            x_axis.append(x)
            y_axis.append(y)
            z_axis.append(z)
        pl.figure(label + '_x')
        pl.plot(np.array(x_axis))
        pl.figure(label + '_y')
        pl.plot(np.array(y_axis))
        pl.figure(label + '_z')
        pl.plot(np.array(z_axis))
        pl.show()
