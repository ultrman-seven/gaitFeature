import numpy as np
import matplotlib.pyplot as pl

def get_data(file_name):
    with open(file_name,'r',encoding = "utf-8")as f_data:
        lines = f_data.readlines()
        data,acc,gyr,mag,quat = [],[],[],[],[]
        for i in range(0,15):
            data.append([])
        for line in lines:
            tmp = list(map(float,line.split()))
            acc.append(tmp[2:5])
            gyr.append(tmp[5:8])
            mag.append(tmp[8:11])
            quat.append(tmp[11:15])
            for i in range(0,15):
                data[i].append(tmp[i])
    return {'original_data':data,'acc':acc,'gyr':gyr,'mag':mag,'quat':quat}


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
    count = 0
    sum = 0
    result = []
    for data in datas:
        if count != 5:
            count+=1
            sum+=data
        else:
            result.append(sum / 5)
            count = 0
            sum = 0
    if count:
        result.append(sum / count)
    return result


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

filename = 'MT_037825B9_008-001'

get = get_data(filename + '.txt')
dat = get['original_data']
x_max = len(dat[2])
start = 0
acc_x = np.array(dat[2][start:start + x_max])
acc_y = np.array(dat[3][start:start + x_max])
acc_z = np.array(dat[4][start:start + x_max])

ro_acc_x,ro_acc_y,ro_acc_z = [],[],[]
ro_acc = rotate(get['acc'][:] , get['quat'][:])
for i in range(0,len(dat[0])):
    ro_acc_x.append(ro_acc[i][0])
    ro_acc_y.append(ro_acc[i][1])
    ro_acc_z.append(ro_acc[i][2])

ro_acc_y = filtering(ro_acc_y)

ro_acc_x = np.array(ro_acc_x)
ro_acc_y = np.array(ro_acc_y)
ro_acc_z = np.array(ro_acc_z)

gyr_x = np.array(dat[5][start:start + x_max])
gyr_y = np.array(dat[6][start:start + x_max])
gyr_z = np.array(dat[7][start:start + x_max])

ang_x = np.array(integral(dat[5]))
ang_y = np.array(integral(dat[6]))
ang_z = np.array(integral(dat[7]))

pl.figure(filename + 'acc')
pl.plot(acc_x,'b',acc_y + 10,'r',acc_z + 20,'k')
pl.figure(filename + 'gyr')
pl.plot(gyr_x,'b-',gyr_y + 5,'r--',gyr_z + 10,'k-')
pl.figure(filename + 'ang')
#pl.plot(ro_acc_x,'r',ro_acc_y + 5,'b',ro_acc_z + 10,'k')
pl.plot(ro_acc_z,'b')
pl.show()
