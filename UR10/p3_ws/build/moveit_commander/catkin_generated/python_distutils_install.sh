#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/moveit/moveit_commander"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/morten/UNI/P3/robot_handover/UR10/p3_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/morten/UNI/P3/robot_handover/UR10/p3_ws/install/lib/python3/dist-packages:/home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/moveit_commander/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/moveit_commander" \
    "/usr/bin/python3" \
    "/home/morten/UNI/P3/robot_handover/UR10/p3_ws/src/moveit/moveit_commander/setup.py" \
    egg_info --egg-base /home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/moveit_commander \
    build --build-base "/home/morten/UNI/P3/robot_handover/UR10/p3_ws/build/moveit_commander" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/morten/UNI/P3/robot_handover/UR10/p3_ws/install" --install-scripts="/home/morten/UNI/P3/robot_handover/UR10/p3_ws/install/bin"
