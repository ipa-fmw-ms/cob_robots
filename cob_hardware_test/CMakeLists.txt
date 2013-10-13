cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

macro(rosbuild_add_rostest_env file robot)
  string(REPLACE "/" "_" _testname ${robot})
  _rosbuild_add_rostest_env(${file} ${robot})
  if(CMAKE_MINOR_VERSION LESS 6)
    add_custom_target(test)
  endif(CMAKE_MINOR_VERSION LESS 6)
  add_dependencies(test rostest_${_testname})
  _rosbuild_check_rostest_result(rostest_${_testname} ${PROJECT_NAME} ${file})
endmacro(rosbuild_add_rostest_env)
macro(_rosbuild_add_rostest_env file robot)
set(_file_name _file_name-NOTFOUND)
find_file(_file_name ${file} ${PROJECT_SOURCE_DIR} /)
if(NOT _file_name)
message(FATAL_ERROR "Can't find rostest file \"${file}\"")
  endif(NOT _file_name)
  string(REPLACE "/" "_" _testname ${robot}ENV${file})
  add_custom_target(rostest_${_testname}
                    COMMAND export ROBOT=${robot} && ${ARGN} rostest ${file}
                    DEPENDS ${file}
                    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
                    VERBATIM)
  if(NOT rosbuild_test_nobuild)
    add_dependencies(rostest_${_testname} tests)
  endif(NOT rosbuild_test_nobuild)
endmacro(_rosbuild_add_rostest_env)

macro(rosbuild_add_rostest_arg file robot)
  string(REPLACE "/" "_" _testname ${robot})
  _rosbuild_add_rostest_arg(${file} ${robot})
  if(CMAKE_MINOR_VERSION LESS 6)
    add_custom_target(test)
  endif(CMAKE_MINOR_VERSION LESS 6)
  add_dependencies(test rostest_${_testname})
  _rosbuild_check_rostest_result(rostest_${_testname} ${PROJECT_NAME} ${file})
endmacro(rosbuild_add_rostest_arg)
macro(_rosbuild_add_rostest_arg file robot)
set(_file_name _file_name-NOTFOUND)
find_file(_file_name ${file} ${PROJECT_SOURCE_DIR} /)
if(NOT _file_name)
message(FATAL_ERROR "Can't find rostest file \"${file}\"")
  endif(NOT _file_name)
  string(REPLACE "/" "_" _testname ${robot}ARG${file})
  add_custom_target(rostest_${_testname}
                    COMMAND ${ARGN} rostest ${file} ROBOT:=${robot}
                    DEPENDS ${file}
                    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
                    VERBATIM)
  if(NOT rosbuild_test_nobuild)
    add_dependencies(rostest_${_testname} tests)
  endif(NOT rosbuild_test_nobuild)
endmacro(_rosbuild_add_rostest_arg)

# Set the build type. Options are:
# Coverage : w/ debug symbols, w/o optimization, w/ code-coverage
# Debug : w/ debug symbols, w/o optimization
# Release : w/o debug symbols, w/ optimization
# RelWithDebInfo : w/ debug symbols, w/ optimization
# MinSizeRel : w/o debug symbols, w/ optimization, stripped binaries
#set(ROS_BUILD_TYPE RelWithDebInfo)

rosbuild_init()

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
#set the default path for built libraries to the "lib" directory
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

#uncomment if you have defined messages
#rosbuild_genmsg()
#uncomment if you have defined services
rosbuild_gensrv()

# rostest for robots
SET(robotlist
cob3-1
cob3-2
cob3-3
cob3-4
cob3-5
cob3-6
cob3-7
raw3-1
raw3-2
raw3-3
raw3-4
raw3-5
raw3-6
desire
)



# loop through list of robots for testing
FOREACH(robot ${robotlist})
MESSAGE("testing for robot: ${robot}")
# rosbuild_add_roslaunch_check(robots/${robot}_manual.test.xml robot:=${robot})
# rosbuild_add_rostest(robots/robot_auto_sim.test robot:=${robot} robot_env:=ipa-apartment)
# rosbuild_add_roslaunch_check(robots/robot_auto_sim.test)
# rosbuild_add_rostest_sim(components/laser_front.test ${robot})
rosbuild_add_rostest_arg(robots/robot_auto_sim.test ${robot})
rosbuild_add_rostest_env(robots/robot_auto_sim.test ${robot})
#rosbuild_add_rostest_sim(robots/robot_manual_sim.test ${robot})
# see macros in https://github.com/ros/ros/blob/groovy-devel/core/rosbuild/core/rosbuild/public.cmake
ENDFOREACH(robot)
