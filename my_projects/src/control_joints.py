#! /usr/bin/env python 
import rospy 
import tf
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from std_msgs.msg import Float64

rospy.init_node('control_joint_manipulator')
pub1 = rospy.Publisher('/manipulator/first_joint_position_controller/command', Float64, queue_size=1)
pub2 = rospy.Publisher('/manipulator/second_joint_position_controller/command', Float64, queue_size=1)
pub3 = rospy.Publisher('/manipulator/third_joint_position_controller/command', Float64, queue_size=1)

count = 0
rate = rospy.Rate(5)
listener = tf.TransformListener()
x = []
y = [] 
z = []
ctrl_c = False

while not ctrl_c: 
	motion1 = Float64(); motion2 = Float64(); motion3 = Float64() 
	for i in np.arange(0,6.3,0.15): 
		motion1.data = i
		for j in np.arange(0,1.8,0.2): 
			motion2.data = j
			for k in np.arange(0,3.2,0.02): 
				motion3.data = k
				pub1.publish(motion1)
				pub2.publish(motion2)
				pub3.publish(motion3)
				rate.sleep()
				listener.waitForTransform('/world','/third_link',rospy.Time(), rospy.Duration(4.0))
				(trans, rot) = listener.lookupTransform('world','/third_link',  rospy.Time(0))
				x.append(trans[0]); y.append(trans[1]); z.append(trans[2])
	rospy.loginfo("All coordinates obtained. Closing program")
	ctrl_c = True


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(x, y, z, c=z, cmap='Greens');
plt.show()

