#!/usr/bin/env python



import rospy
import actionlib
import copy
from control_msgs.msg import FollowJointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryFeedback
from control_msgs.msg import FollowJointTrajectoryResult
from control_msgs.msg import FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from trajectory_msgs.msg import JointTrajectory
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Int32
import json
import cv2
import time 
import math

def invkin(xyz):
	"""
	Python implementation of the the inverse kinematics for the crustcrawler
	Input: xyz position
	Output: Angels for each joint: q1,q2,q3,q4
	
	You might adjust parameters (d1,a1,a2,d4).
	The robot model shown in rviz can be adjusted accordingly by editing au_crustcrawler_ax12.urdf
	"""

        d1 = 0.155 # cm (height of 2nd joint)
        a1 = 0.0 # (distance along "y-axis" to 2nd joint)
        a2 = 0.173 # (distance between 2nd and 3rd joints)
        d4 = 0.23 # (distance from 3rd joint to gripper center - all inclusive, ie. also 4th joint)

        xc = xyz[0];
        yc = xyz[1];
        zc = xyz[2];
    
        """ First angle """ 
        q1 = math.atan2(yc,xc);
    
        r2 = pow((xc - a1*math.cos(q1)), 2) + pow((yc-a1*math.sin(q1)),2)
        s = zc - d1
    
        """Determinant"""
        d = (r2+pow(s,2)-pow(a2,2)-pow(d4,2))/(2*a2*d4);
    
        """ The third angle """
        q3 = math.atan2(-math.sqrt(1-pow(d,2)),d);
    
        """ second angle """
        q2 = math.atan2(s,math.sqrt(r2)) - math.atan2(d4*math.sin(q3),a2+d4*math.cos(q3))-(math.pi/2)
    
        """ The last joint rotates around its own z axis"""
        """ Thus any angle """
        q4 = 0;
    
        #print("Q1: " + str(q1));
        #print("Q2: " + str(q2)); 
        #print("Q3: " + str(q3));

    	return [q1,q2,q3,q4]

def GetGrasp(size):
	"""This sections need to be tested and meassured"""
	"""maxGrasp = 0.10 #cm
	maxRadian = 1.0
	RadOffset = 0.0 # should the zero for grap be other than zero
	Cen2Rad = maxRadian/maxGrasp
    	
    	result = (Cen2Rad * size) + RadOffset
	print(result)"""
	size = size * 100
	size = size - 1.0
	result =(-0.0337*(size*size))+ 0.0848*size + 0.8211 
	print(result)
	return result

def maxGrasp():
	"""This sections need to be tested and meassured"""
	"""maxGrasp = 0.10 #cm
	maxRadian = 1.0
	RadOffset = 0.0 # should the zero for grap be other than zero
	Cen2Rad = maxRadian/maxGrasp
    	
    	result = (Cen2Rad * size) + RadOffset
	print(result)"""
	result = 0.1 
	#print(result)
	return result

def minGrasp():
	"""This sections need to be tested and meassured"""
	"""maxGrasp = 0.10 #cm
	maxRadian = 1.0
	RadOffset = 0.0 # should the zero for grap be other than zero
	Cen2Rad = maxRadian/maxGrasp
    	
    	result = (Cen2Rad * size) + RadOffset
	print(result)"""
	result = 0.01 
	#print(result)
	return result

class GripperExampleNode:
    
	N_JOINTS = 5
	def __init__(self,server_name):
		self.GripperPos = 0.5  
		self.xyzPosition =[0.0,0.3,0.2]
		self.pixelCenter = [345,312] #(y,x) of the image
		self.target={}
		self.MTransX = 0.112
		self.MTransY = 0.112
		self.transW = 1
		self.transH = 1
        
		self.client = actionlib.SimpleActionClient(server_name, FollowJointTrajectoryAction)

		self.joint_positions = []
		self.names =["joint1",
				"joint2",
				"joint3",
				"joint4",
                "gripper"]
		# the list of xyz points we want to plan
		'''xyz_positions = [
		[0.2, 0.0, 0.2],
		[0.25, 0.1, 0.2],
		[0.2, 0.2, 0.2]
		]
		# initial duration
		dur = rospy.Duration(1)
		p=invkin([0.2,-0.2,0.2])
		p.append(0.9)

		# construct a list of joint positions by calling invkin for each xyz point
		#for p in xyz_positions:
		jtp = JointTrajectoryPoint(positions=p,velocities=[2.0]*self.N_JOINTS ,time_from_start=dur)
		dur += rospy.Duration(2)
		self.joint_positions.append(jtp)

		self.jt = JointTrajectory(joint_names=self.names, points=self.joint_positions)
		self.goal = FollowJointTrajectoryGoal( trajectory=self.jt, goal_time_tolerance=dur+rospy.Duration(2) )'''
        
	def calibrateCenter(self):
            print("Calibrating Center")
            var1,var2,tempH,tempW = imgu.image_analyse()
            print(str(var1) + "(x), " + str(var2) + "(y)")
            self.transH, self.transW = imgu.calibrate(tempH,tempW,4.0,4.0)
            print(str(self.transW) + "(TransX), " + str(self.transH) + "(TransY)")
            #self.MTransX =0.125 #43 (336-293)
            #self.MTransY =0.125 #42 (189-145)

	def getBlockCenter(self):
            print("Getting Block")
            
            self.Object[1],self.Object[0],_,_ = imgu.image_analyse()
            print(str(self.Object[1]) + "(x), " + str(self.Object[0]) + "(y)")
            deltaX = self.pixelCenter[0] - self.Object[0]  
            deltaY =  self.pixelCenter[1] - self.Object[1] 
            print("delta pix X: " +str(deltaX))
            print("delta pix Y: " +str(deltaY))
            
            print("trasnX: " + str(self.transW))
            print("transY: " + str(self.transH))
            
            offsetX=(deltaX*self.MTransX)/100
            offsetY=(deltaY*self.MTransY)/100
            print("offsetX: " + str(offsetX))
            print("offsetY: " + str(offsetY))


            print("divisionX: " + str(deltaX*self.transH))
            print("divisionY: " + str(deltaY*self.transW)) 
            if(offsetY !=0):
                print("Hi from if ")
                node.fineGrasping([offsetX,offsetY,0.02],0.025,0.025)
            else:
                print("Hi from else ")
                node.fineGrasping([offsetX,offsetY,0.02],0.025,0.025)
            node.defaultPos()
            node.fineReleasing([0.2,0.2,0.02],0.04)
            node.defaultPos()
            
	def send_command(self):
            print("Step 1")
            self.client.wait_for_server()
            print("Step 2")
            print self.goal
            self.client.send_goal(self.goal)
            print("Step 3")
            self.client.wait_for_result()
            #print self.client.get_result()
            print("Step 4")
    
	def moveto(self,xyz):
            dur = rospy.Duration(2)
            #Descend positions
            #truct a list of joint positions by calling invkin for each xyz point
            #Phase 1: Hover above position.
            newxyz=copy.copy(xyz) 
            CalcPos = invkin(newxyz)
            CalcPos.append(self.GripperPos)
            print(CalcPos)
                
            jtp = JointTrajectoryPoint(positions=CalcPos,velocities=[1.0]*self.N_JOINTS ,time_from_start=dur)
            dur += rospy.Duration(4)
            newJTP = []
            newJTP.append(jtp)
            self.joint_positions = newJTP

            self.jt = JointTrajectory(joint_names=self.names, points=self.joint_positions)
            self.goal = FollowJointTrajectoryGoal( trajectory=self.jt, goal_time_tolerance=dur+rospy.Duration(4))
            self.send_command()
            self.xyzPosition = newxyz
            
            return
    
	def grasp(self,width):
            dur = rospy.Duration(2)
            #Descend positions
            #truct a list of joint positions by calling invkin for each xyz point
            #Phase 1: Hover above position.
            CalcPos = invkin(self.xyzPosition)
            newgrasp = GetGrasp(width)
            CalcPos.append(newgrasp)
            print(CalcPos)
                
            jtp = JointTrajectoryPoint(positions=CalcPos,velocities=[5.0]*self.N_JOINTS ,time_from_start=dur)
            dur += rospy.Duration(2)
            newJTP = []
            newJTP.append(jtp)
            self.joint_positions = newJTP

            self.jt = JointTrajectory(joint_names=self.names, points=self.joint_positions)
            self.goal = FollowJointTrajectoryGoal( trajectory=self.jt, goal_time_tolerance=dur+rospy.Duration(2))
            self.send_command()
            time.sleep(1)
            self.GripperPos = newgrasp
            
            return
    
	def hoverabove(self,xyz,height):
            assert (height > 0.005),"height given under 5mm"
            assert (height < 0.5),"height given over 50cm"
            dur = rospy.Duration(1)
            #Descend positions
            #truct a list of joint positions by calling invkin for each xyz point
            #Phase 1: Hover above position.
            newxyz=copy.copy(xyz)
            newxyz[2]=newxyz[2]+(height*2)
            CalcPos = invkin(newxyz)
            CalcPos.append(self.GripperPos)
            print(CalcPos)
                
            jtp = JointTrajectoryPoint(positions=CalcPos,velocities=[1.0]*self.N_JOINTS ,time_from_start=dur)
            dur += rospy.Duration(8)
            newJTP = []
            newJTP.append(jtp)
            self.joint_positions = newJTP

            self.jt = JointTrajectory(joint_names=self.names, points=self.joint_positions)
            self.goal = FollowJointTrajectoryGoal( trajectory=self.jt, goal_time_tolerance=dur+rospy.Duration(8))
            self.send_command()
            self.xyzPosition = newxyz
            
            return

	def defaultPos(self):
            dur = rospy.Duration(1)
            #CalcPos = invkin([0,0,0.563])
            #CalcPos.append(self.GripperPos)
            #print(CalcPos)
                
            jtp = JointTrajectoryPoint(positions=[0,0,0,0,1],velocities=[1.0]*self.N_JOINTS ,time_from_start=dur)
            dur += rospy.Duration(8)
            newJTP = []
            newJTP.append(jtp)
            self.joint_positions = newJTP

            self.jt = JointTrajectory(joint_names=self.names, points=self.joint_positions)
            self.goal = FollowJointTrajectoryGoal( trajectory=self.jt, goal_time_tolerance=dur+rospy.Duration(8))
            self.send_command()
            #self.xyzPosition = [0,0,0.563]
            return

        

	def fineGrasping(self, TargetPos, GraspWidth, ObsHeight):
            self.hoverabove(TargetPos,ObsHeight)
            self.grasp(maxGrasp())
            self.moveto(TargetPos)
            
            #print("Pixel position is: "+ str(self.Object))
            #print("Pixel position is: "+ str(TargetPos))
            #raw_input("Press Enter to Meassure Position...")
            self.grasp(GraspWidth)    
            self.hoverabove(TargetPos,ObsHeight)
            self.defaultPos()
            return

	def fineReleasing(self, TargetPos, ObsHeight):
            self.hoverabove(TargetPos,ObsHeight)
            self.moveto(TargetPos)    
            self.grasp(maxGrasp())
            self.hoverabove(TargetPos,ObsHeight)
            self.defaultPos()
            return
     
def callback(data,robot):
            #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
            print(data.data)
            print(data)
            #temp = json.dumps(data.data)
            jcommands = json.loads(data.data)
            #jcommands=json.loads(jraw)
            cnt=0
            for pos in jcommands["T"]:
                print(pos)
                if(cnt == 0):
                    pos["command"] = "putdown"
                    robot.target = pos #now first pos in arr is our target pos
                else:
                    func = swictherhandler(pos,robot)
                    robot.target["h"] = pos["h"]*(cnt+0.8) #adjust new height 
                    func = swictherhandler(robot.target,robot)
                cnt = cnt+1
            robot.defaultPos()
            print("All Done")
            return
            # Execute the function
            
def swictherhandler(jcommands,robot):
            
            def pickupobj(jcommands):
                #print("Hello World 1, " + jcommands["from"])
                deltaX = robot.pixelCenter[0] - int(jcommands["Y"])  
                deltaY =  robot.pixelCenter[1] - int(jcommands["X"]) 
                print("delta pix X: " +str(deltaX))
                print("delta pix Y: " +str(deltaY))
            
                print("trasnX: " + str(robot.transW))
                print("transY: " + str(robot.transH))
            
                offsetX=(deltaX*robot.MTransX)/100
                offsetY=(deltaY*robot.MTransY)/100
                print("offsetX: " + str(offsetX))
                print("offsetY: " + str(offsetY))


                print("divisionX: " + str(deltaX*robot.transH))
                print("divisionY: " + str(deltaY*robot.transW))
                rw = (int(jcommands["w"])*robot.MTransX)/100.0
                rh = (int(jcommands["h"])*robot.MTransX)/100.0
                zh = ((int(jcommands["h"])*robot.MTransX)/100.0)/2
                robot.fineGrasping([offsetX,offsetY,zh],rw,rh)
                
            def abs_pickupobj(jcommands):
                TargetPos = [float(jcommands["X"]),float(jcommands["Y"]),float(jcommands["Z"])]
                robot.fineGrasping(TargetPos,float(jcommands["w"]),float(jcommands["h"]))

                
            def putdownobj(jcommands):
                print("Hello World 3")
                deltaX = robot.pixelCenter[0] - int(jcommands["Y"])  
                deltaY =  robot.pixelCenter[1] - int(jcommands["X"]) 
                print("delta pix X: " +str(deltaX))
                print("delta pix Y: " +str(deltaY))
            
                print("trasnX: " + str(robot.transW))
                print("transY: " + str(robot.transH))
            
                offsetX=(deltaX*robot.MTransX)/100
                offsetY=(deltaY*robot.MTransY)/100
                print("offsetX: " + str(offsetX))
                print("offsetY: " + str(offsetY))


                print("divisionX: " + str(deltaX*robot.transH))
                print("divisionY: " + str(deltaY*robot.transW))
                rw = (int(jcommands["w"])*robot.MTransX)/100.0
                rh = (int(jcommands["h"])*robot.MTransX)/100.0
                robot.fineReleasing([offsetX,offsetY,rh],rw)
                
            def abs_putdownobj(jcommands):
                TargetPos = [float(jcommands["X"]),float(jcommands["Y"]),float(jcommands["Z"])]
                robot.fineReleasing(TargetPos,float(jcommands["w"]),float(jcommands["h"]))
                
            def default(jcommands):
                robot.default()
                
            switcher = {
                    "pickup": pickupobj,
                    "abspickup": abs_pickupobj,
                    "putdown": putdownobj,
                    "absputdown": abs_putdownobj,
                    "default": default
                    }
            func = switcher.get(jcommands["command"], "nothing")
            
            return func(jcommands)


            
if __name__ == "__main__":
    rospy.init_node("Final_Project_Robot_Listener")
    print("Ready")
    #data =  '{ "command":"hello1", "from":"Yours Truly"}'
    #callback(data, "none")
    
    # 2 nodes double the trouble
    node = GripperExampleNode("/arm_controller/follow_joint_trajectory")
    node.defaultPos()
    rospy.Subscriber("blockinfo", String, callback,node)
    rospy.spin()
    

    """
	#node= ActionExampleNode("/arm_controller/follow_joint_trajectory")
	#node.send_command()    
    node = GripperExampleNode("/arm_controller/follow_joint_trajectory")
    print("Sleeping and starting finegrasp")
    node.defaultPos()
    raw_input("Press Enter to Calibrate...")
    node.calibrateCenter()        
    raw_input("Press Enter to Finding Pos ")
    node.getBlockCenter()
    print("The end")
    """
    
    
    """ Testing the encapsulations for readabliity
    node.fineGrasping([0.2,0.2,0.02],0.025,0.025)
    node.defaultPos()
    node.fineReleasing([0.2,0.0,0.02],0.025)
    node.defaultPos()    
    """
    
    """ First combined movement with abstracted functions
    node.hoverabove([0.2,0.0,0.02],0.04)
    node.grasp(maxGrasp())
    node.moveto([0.2,0.0,0.02])
    node.grasp(0.04)    
    node.hoverabove([0.2,0.0,0.02],0.04)
    node.moveto([0.2,-0.2,0.2])
    node.grasp(maxGrasp())"""
