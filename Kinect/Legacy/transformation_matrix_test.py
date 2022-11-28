import numpy as np 
from math import cos, sin, radians
import scipy.linalg as linalg

#input is an angle in deg, it outputs the cos and sine to the angle 
def trig(angle):
    r = radians(angle)
    return cos(r), sin(r)

#creates a rotation matrix around y with input deg 
def roty_matrix(rotation):
    yC, yS = trig(rotation)
    Rotate_Y_matrix = np.array([[yC, 0, yS, 0],
                                [0, 1, 0, 0],
                                [-yS, 0, yC, 0],
                                [0, 0, 0, 1]])
    return Rotate_Y_matrix

def rotx_matrix(rotation):
    xC, xS = trig(rotation)
    Rotate_X_matrix = np.array([[1, 0, 0, 0],
                                [0, xC, -xS, 0],
                                [0, xS, xC, 0],
                                [0, 0, 0, 1]])
    return Rotate_X_matrix


#creates a transformation matrix from translation and rotation around y 
def create_transformation_matrix(translation_vector, rotation_y = 0, rotation_x = 0):
    transformation_matrix = np.identity(4)
    print(translation_vector)
    transformation_matrix[:,3] = translation_vector 
    transformation_matrix[0:3,0:3]=roty_matrix(rotation_y)[0:3,0:3]
    transformation_matrix = np.dot(transformation_matrix,rotx_matrix(rotation_x))
    return transformation_matrix

#testing the functions 
kinect_to_mark = create_transformation_matrix(np.array([-0.09,0.47,-1.75,1]),-3.1)


vector_to_glove = np.array([-0.66,0.55,-1.38,1])
print(vector_to_glove.T)


#to use the transformation matrix 
#kinect_to_mark = np.dot(linalg.inv(KTU),vector_to_glove.T)

mark_to_ur = create_transformation_matrix(np.array([0,0,-0.10,1]),45,90)

kinect_to_ur = np.dot(kinect_to_mark, mark_to_ur)

UTHV2 = np.dot(linalg.inv(kinect_to_ur),vector_to_glove.T)



print(f"UTHV \n {UTHV}")
print(f"UTHV2 \n {UTHV2}")

