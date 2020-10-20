# agrotec_image_filtering
Image filtering based on color detection. The package uses OpenCV package to obtain precise coordinates of the predefined color and draw boxes over it to visualize the result.

## ROS Interfaces
This part describes various ROS-related interfaces such as parameters and topics.

### Parameters

* `~visualization: bool`

    If true, the node publish visualized images to `~visualization` topic.
    Default: `true`

* `~lower_color_boundary: int[]`

    Minimum value of color in RGB to be detected.

* `~upper_color_boundary: int[]`

    Maximum value of color in RGB to be detected.

* `~box_color: int[]`

    Color of the box to be drawn over the detected object.

### Topics Published

* `~filtered_image: sensor_mgs/Image`

    Result of filtering (the image which contains a specified color)

* `~visualization: sensor_mgs/Image`

    Visualized result over an input image.

### Topics Subscribed

* `~input: sensor_msgs/Image`

    Input image to be proccessed


## Project structure
```
.
├── launch
│   └── filtering.launch
├── scripts
│   └── filter.py
├── CMakeLists.txt
├── LICENSE
├── package.xml
└── README.md

```

### Folders
*  `./launch`  - *.yaml roslaunch files
*  `./scripts`  - main folder of the project (contains executables)

### Files
The project uses following files

#### Launch
*  `filtering.launch`  - starting the filtering node

#### Package
*  `filter.py`  - image filtering node (performance tweak)

#### ROS
*  `CMakeLists.txt`  - package building instructions
*  `package.xml`  - data about the package
*  `setup.py`  - rospy instructions

## Example of use
That's not good to try detecting objects on pictures that aren't containing any desired objects. For optimization purposes, there should be a filter. This filter would try to detect some objects based on colors of the desired object and send the image further if there any object you would like it to be.

To start the filtering you should run : 
~~~bash
$ roslaunch agrotec_image_filtering filtering.launch
~~~
