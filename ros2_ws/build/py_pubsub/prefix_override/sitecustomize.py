import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ezra/Desktop/learning-week-subsriber-publisher/ros2_ws/install/py_pubsub'
