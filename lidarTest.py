import pickle
from rplidar import RPLidar
import numpy as np

lidar = RPLidar('/dev/ttyUSB0')

#info = lidar.get_info()
#print(info)

data = []

for i, scan in enumerate(lidar.iter_scans()):
	data.append(np.array(scan))
	#print('%d: Got %d measurements' % (i, len(scan)))
	if i > 10:
		break

#print(data)
pickle.dump(data, open("save6.p", "wb"))

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
