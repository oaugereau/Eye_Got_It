import sys,os

import time, csv,threading
sys.path.insert(1,os.path.join( os.getcwd(),'64'))
import tobii_research as tr
if len(sys.argv)!=5 :
    sys.exit("error")

screen_width = int(sys.argv[1])
screen_height = int(sys.argv[2])
eyeTrackerCSV=sys.argv[3] #"eyeTracker.csv"
eyeTrackerHeadCSV=sys.argv[4]#"eyeTrackerHead.csv"

with open(eyeTrackerCSV, 'w', newline='') as csvfile:
        fileUser = csv.writer(csvfile, delimiter=',')
        fileUser.writerow(["x_gaze","y_gaze","validity_gaze","timestamp_us_gaze","unix_time_ms_gaze","left_pupil_diameter_millimeters","left_pupil_validity","right_pupil_diameter_millimeters","right_pupil_validity","left_eye_x_gaze","left_eye_y_gaze","left_eye_validity_gaze","right_eye_x_gaze","right_eye_y_gaze","right_eye_validity_gaze"])
        csvfile.close()


with open(eyeTrackerHeadCSV, 'w', newline='') as csvfile:
        fileUser = csv.writer(csvfile, delimiter=',')
        fileUser.writerow(["head_pos_x","head_pos_y","head_pos_z","validity_pos","timestamp_us_head","unix_time_ms_head","left_x_gaze_point_in_user_coordinate_system","left_y_gaze_point_in_user_coordinate_system","left_z_gaze_point_in_user_coordinate_system","left_gaze_origin_validity","right_x_gaze_point_in_user_coordinate_system","right_y_gaze_point_in_user_coordinate_system","right_z_gaze_point_in_user_coordinate_system","right_gaze_origin_validity","left_x_gaze_origin_in_trackbox_coordinate_system","left_gaze_y_origin_in_trackbox_coordinate_system","left_z_gaze_origin_in_trackbox_coordinate_system","right_x_gaze_origin_in_trackbox_coordinate_system","right_y_gaze_origin_in_trackbox_coordinate_system","right_z_gaze_origin_in_trackbox_coordinate_system"])
        csvfile.close() 

found_eyetrackers = tr.find_all_eyetrackers()
if not found_eyetrackers :
    print("eyeTracker pro not found")
    sys.exit()
my_eyetracker = found_eyetrackers[0]
"""
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)
"""
def execute(eyetracker):
    gaze_data(eyetracker)
 
global_gaze_data = None

def gaze_data_callback(gaze_data):
    global global_gaze_data,eyeTrackerCSV,eyeTrackerHeadCSV,screen_width,screen_height
    global_gaze_data = gaze_data
    #print(global_gaze_data)
    timestampEyeTracker = global_gaze_data["device_time_stamp"]
    unixTime = round(time.time() * 1000)

    
    x = ((global_gaze_data["left_gaze_point_on_display_area"][0] + global_gaze_data["right_gaze_point_on_display_area"][0]) / 2)*screen_width
    y = ((global_gaze_data["left_gaze_point_on_display_area"][1] + global_gaze_data["right_gaze_point_on_display_area"][1]) / 2)*screen_height

    validity_gaze=""
    if global_gaze_data["left_gaze_point_validity"] == 1 and global_gaze_data["right_gaze_point_validity"] == 1:
        validity_gaze = "valid"
        

    elif global_gaze_data["left_gaze_point_validity"] == 1 and global_gaze_data["right_gaze_point_validity"] == 0:
        validity_gaze = "valid"
        x = global_gaze_data["left_gaze_point_on_display_area"][0]*screen_width
        y = global_gaze_data["left_gaze_point_on_display_area"][1]*screen_height

    elif global_gaze_data["left_gaze_point_validity"] == 0 and global_gaze_data["right_gaze_point_validity"] == 1:
        validity_gaze = "valid"
        x = global_gaze_data["right_gaze_point_on_display_area"][0]*screen_width
        y = global_gaze_data["right_gaze_point_on_display_area"][1]*screen_height

    else :
        validity_gaze = "invalid"

    with open(eyeTrackerCSV, 'a', newline='') as csvfile:
        fileUser = csv.writer(csvfile, delimiter=',')
        fileUser.writerow([x,y,validity_gaze,timestampEyeTracker,unixTime,global_gaze_data["left_pupil_diameter"],global_gaze_data["left_pupil_validity"],global_gaze_data["right_pupil_diameter"],global_gaze_data["right_pupil_validity"],global_gaze_data["left_gaze_point_on_display_area"][0]*screen_width,global_gaze_data["left_gaze_point_on_display_area"][1]*screen_height,global_gaze_data["left_gaze_point_validity"],global_gaze_data["right_gaze_point_on_display_area"][0]*screen_width,global_gaze_data["right_gaze_point_on_display_area"][1]*screen_height,global_gaze_data["right_gaze_point_validity"]])
        csvfile.close()


    x_position = ((global_gaze_data["left_gaze_origin_in_user_coordinate_system"][0] + global_gaze_data["right_gaze_origin_in_user_coordinate_system"][0]) /2)
    y_position = ((global_gaze_data["left_gaze_origin_in_user_coordinate_system"][1] + global_gaze_data["right_gaze_origin_in_user_coordinate_system"][1]) /2)
    z_position = ((global_gaze_data["left_gaze_origin_in_user_coordinate_system"][2] + global_gaze_data["right_gaze_origin_in_user_coordinate_system"][2]) /2)
    
    pos_valid = ""
    if global_gaze_data["left_gaze_origin_validity"] == 1 and global_gaze_data["right_gaze_origin_validity"] == 1:
        pos_valid = "valid"
    elif global_gaze_data["left_gaze_origin_validity"] == 1 and global_gaze_data["right_gaze_origin_validity"] == 0:
        pos_valid = "valid"
        x_position = global_gaze_data["left_gaze_origin_in_user_coordinate_system"][0]
        y_position = global_gaze_data["left_gaze_origin_in_user_coordinate_system"][1]
        z_position = global_gaze_data["left_gaze_origin_in_user_coordinate_system"][2]

    elif global_gaze_data["left_gaze_origin_validity"] == 0 and global_gaze_data["right_gaze_origin_validity"] == 1:
        pos_valid = "valid"
        x_position = global_gaze_data["right_gaze_origin_in_user_coordinate_system"][0]
        y_position = global_gaze_data["right_gaze_origin_in_user_coordinate_system"][1]
        z_position = global_gaze_data["right_gaze_origin_in_user_coordinate_system"][2]
    
    else :
        pos_valid = "invalid"

    with open(eyeTrackerHeadCSV, 'a', newline='') as csvfile:
        fileUser = csv.writer(csvfile, delimiter=',')
        fileUser.writerow([x_position,y_position,z_position,pos_valid,timestampEyeTracker,unixTime,global_gaze_data["left_gaze_origin_in_user_coordinate_system"][0],global_gaze_data["left_gaze_origin_in_user_coordinate_system"][1],global_gaze_data["left_gaze_origin_in_user_coordinate_system"][2],global_gaze_data["left_gaze_origin_validity"],global_gaze_data["right_gaze_origin_in_user_coordinate_system"][0],global_gaze_data["right_gaze_origin_in_user_coordinate_system"][1],global_gaze_data["right_gaze_origin_in_user_coordinate_system"][2],global_gaze_data["right_gaze_origin_validity"],global_gaze_data["left_gaze_origin_in_trackbox_coordinate_system"][0],global_gaze_data["left_gaze_origin_in_trackbox_coordinate_system"][1],global_gaze_data["left_gaze_origin_in_trackbox_coordinate_system"][2],global_gaze_data["right_gaze_origin_in_trackbox_coordinate_system"][0],global_gaze_data["right_gaze_origin_in_trackbox_coordinate_system"][1],global_gaze_data["right_gaze_origin_in_trackbox_coordinate_system"][2]])
        csvfile.close()

    print("x_gaze : " + str(x) + " y_gaze : " + str(y) + " validity_gaze : " + str(validity_gaze) + " timestamp_us_gaze : " + str(timestampEyeTracker) + " unix_time_ms_gaze : " + str(unixTime))

 
def gaze_data(eyetracker):
    global global_gaze_data, global_user_position_guide
    
    #print("Subscribing to gaze data for eye tracker with serial number {0}.".format(eyetracker.serial_number))

    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    
    while True:
        time.sleep(0.5)
        
    # Wait while some gaze data is collected.
    #time.sleep(2)
    
    #eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    
    #print("Unsubscribed from gaze data.")

    #print("Last received gaze package:")
    #print(global_gaze_data)
    
# <EndExample>

execute(my_eyetracker)
