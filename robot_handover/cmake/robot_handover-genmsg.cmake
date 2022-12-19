# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "robot_handover: 2 messages, 0 services")

set(MSG_I_FLAGS "-Irobot_handover:/home/andreas/robot_handover_ros/src/robot_handover/msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(robot_handover_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg" NAME_WE)
add_custom_target(_robot_handover_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "robot_handover" "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg" ""
)

get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg" NAME_WE)
add_custom_target(_robot_handover_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "robot_handover" "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/robot_handover
)
_generate_msg_cpp(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/robot_handover
)

### Generating Services

### Generating Module File
_generate_module_cpp(robot_handover
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/robot_handover
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(robot_handover_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(robot_handover_generate_messages robot_handover_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_cpp _robot_handover_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_cpp _robot_handover_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robot_handover_gencpp)
add_dependencies(robot_handover_gencpp robot_handover_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robot_handover_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/robot_handover
)
_generate_msg_eus(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/robot_handover
)

### Generating Services

### Generating Module File
_generate_module_eus(robot_handover
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/robot_handover
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(robot_handover_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(robot_handover_generate_messages robot_handover_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_eus _robot_handover_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_eus _robot_handover_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robot_handover_geneus)
add_dependencies(robot_handover_geneus robot_handover_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robot_handover_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/robot_handover
)
_generate_msg_lisp(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/robot_handover
)

### Generating Services

### Generating Module File
_generate_module_lisp(robot_handover
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/robot_handover
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(robot_handover_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(robot_handover_generate_messages robot_handover_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_lisp _robot_handover_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_lisp _robot_handover_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robot_handover_genlisp)
add_dependencies(robot_handover_genlisp robot_handover_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robot_handover_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/robot_handover
)
_generate_msg_nodejs(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/robot_handover
)

### Generating Services

### Generating Module File
_generate_module_nodejs(robot_handover
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/robot_handover
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(robot_handover_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(robot_handover_generate_messages robot_handover_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_nodejs _robot_handover_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_nodejs _robot_handover_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robot_handover_gennodejs)
add_dependencies(robot_handover_gennodejs robot_handover_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robot_handover_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robot_handover
)
_generate_msg_py(robot_handover
  "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robot_handover
)

### Generating Services

### Generating Module File
_generate_module_py(robot_handover
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robot_handover
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(robot_handover_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(robot_handover_generate_messages robot_handover_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/position.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_py _robot_handover_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/andreas/robot_handover_ros/src/robot_handover/msg/joint_angles.msg" NAME_WE)
add_dependencies(robot_handover_generate_messages_py _robot_handover_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(robot_handover_genpy)
add_dependencies(robot_handover_genpy robot_handover_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS robot_handover_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/robot_handover)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/robot_handover
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(robot_handover_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(robot_handover_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/robot_handover)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/robot_handover
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(robot_handover_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(robot_handover_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/robot_handover)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/robot_handover
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(robot_handover_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(robot_handover_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/robot_handover)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/robot_handover
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(robot_handover_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(robot_handover_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robot_handover)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robot_handover\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/robot_handover
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(robot_handover_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(robot_handover_generate_messages_py std_msgs_generate_messages_py)
endif()
