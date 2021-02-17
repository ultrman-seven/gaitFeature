from data import InertialData

dat1=InertialData('MT_037825B9_008-001.txt')

dat1.filtering_acc()
dat1.draw_acc()