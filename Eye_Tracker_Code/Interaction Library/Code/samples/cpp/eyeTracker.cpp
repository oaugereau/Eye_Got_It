/*
COPYRIGHT 2018-2020  - PROPERTY OF TOBII AB
-------------------------------------
2018-2020 TOBII AB - KARLSROVAGEN 2D, DANDERYD 182 53, SWEDEN - All Rights Reserved.

NOTICE:  All information contained herein is, and remains, the property of Tobii AB and its suppliers, if any.
The intellectual and technical concepts contained herein are proprietary to Tobii AB and its suppliers and may be
covered by U.S.and Foreign Patents, patent applications, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material is strictly forbidden unless prior written
permission is obtained from Tobii AB.
*/

#include <iostream>
#include <fstream>
#include<string>
#include <stdio.h>
#include "eyeTracker.h"
#include <interaction_lib/InteractionLib.h>
#include <interaction_lib/misc/InteractionLibPtr.h>
#include <chrono>
#include <ctime>



uint64_t timeSinceEpochMillisec() {
    using namespace std::chrono;
    return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
}

int main(int argc, char *argv[])
{
    for(int i=0 ; i<argc ; ++i){
        std::cout <<argv[i]<<'\n';
    }

    const char* screenWidthTemp = argv[1];
    const char* screenHeightTemp = argv[2];
    //const char* offsetxTemp = argv[3];
    //const char* offsetyTemp = argv[4];
    //const char* widthAppTemp = argv[5];
    //const char* heightAppTemp = argv[6];
    dirGaze = argv[3];
    dirHead = argv[4];
    screenWidth  =  atof(screenWidthTemp);
    screenHeight = atof(screenHeightTemp);
    //offsetx = atof(offsetxTemp);
    //offsety = atof(offsetyTemp);
    //widthApp  = atof(widthAppTemp);
    //heightApp = atof(heightAppTemp);

    offsetx = 0;
    offsety = 0;
    
    std::fstream file;
    file.open (dirGaze, std::ios::out | std::ios::app);
    file << "x_gaze" << ",";
    file << "y_gaze" << ",";
    file << "validity_gaze" << ",";
    file << "timestamp_us_gaze" << ",";
    file << "unix_time_ms_gaze" << ";";
    file <<  std::endl;

    std::fstream fileHead;
    fileHead.open (dirHead, std::ios::out | std::ios::app);
    fileHead << "head_pos_x" << ",";
    fileHead << "head_pos_y" << ",";
    fileHead << "head_pos_z" << ",";
    fileHead << "validity_pos" << ",";
    fileHead << "timestamp_us_head" << ",";
    fileHead << "unix_time_ms_head" << ",";
    fileHead << "head_rot_x" << ",";
    fileHead << "head_rot_y" << ",";
    fileHead << "head_rot_z" << ",";
    fileHead << "validity_rot_x" << ",";
    fileHead << "validity_rot_y" << ",";
    fileHead << "validity_rot_z" << ";";
    fileHead <<  std::endl;

    // create the interaction library
    IL::UniqueInteractionLibPtr intlib(IL::CreateInteractionLib(IL::FieldOfUse::Interactive));
    intlib->CoordinateTransformAddOrUpdateDisplayArea(screenWidth, screenHeight);
    intlib->CoordinateTransformSetOriginOffset(offsetx, offsety);

    // subscribe to gaze point data; print data to stdout when called
    intlib->SubscribeGazePointData([](IL::GazePointData evt, void* context)
    {   
        std::cout
            << "x: " << evt.x
            << ", y: " << evt.y
            << ", validity: " << (evt.validity == IL::Validity::Valid ? "valid" : "invalid")
            << ", timestamp: " << evt.timestamp_us << " us"
            << "\n";

        std::fstream file;
        file.open (dirGaze, std::ios::out | std::ios::app);
        file <<  evt.x << ",";
        file <<  evt.y << ",";
        file << (evt.validity == IL::Validity::Valid ? "valid" : "invalid") << ",";
        file <<  evt.timestamp_us << ",";
        file << timeSinceEpochMillisec();
        file <<  std::endl;

    }, nullptr);

    intlib->SubscribeHeadPoseData([](IL::HeadPoseData evt, void* context)
    {
        std::fstream fileHead;
        fileHead.open (dirHead, std::ios::out | std::ios::app);
        fileHead <<  evt.position_xyz[0] << ",";
        fileHead <<  evt.position_xyz[1] << ",";
        fileHead <<  evt.position_xyz[2] << ",";
        fileHead << (evt.position_validity == IL::Validity::Valid ? "valid" : "invalid") << ",";
        fileHead <<  evt.timestamp_us << ",";
        fileHead << timeSinceEpochMillisec() << ",";
        fileHead << evt.rotation_xyz[0] << ",";
        fileHead << evt.rotation_xyz[1] << ",";
        fileHead << evt.rotation_xyz[2] << ",";
        fileHead <<  (evt.rotation_validity_xyz[0] == IL::Validity::Valid ? "valid" : "invalid") << ",";
        fileHead <<  (evt.rotation_validity_xyz[1] == IL::Validity::Valid ? "valid" : "invalid") << ",";
        fileHead <<  (evt.rotation_validity_xyz[2] == IL::Validity::Valid ? "valid" : "invalid");
        fileHead <<  std::endl;
    
    }, nullptr);

    std::cout << "Starting interaction library update loop.\n";
    
    while (1)
    {
        intlib->WaitAndUpdate();
    }
}