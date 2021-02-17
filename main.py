from data import InertialData

dat1=InertialData('MT_037825B9_008-001.txt')

dat1.filtering('acc')
dat1.draw('acc')