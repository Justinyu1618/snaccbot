from rplidar_library import RPLidar
lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

try:
    for i, scan in enumerate(lidar.iter_scans()):
        print(scan)
        if i > 1000:
            break
except Exception as err:
    print(err)
finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

