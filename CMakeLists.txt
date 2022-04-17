cmake_minimum_required(VERSION 2.8.9)
project (algorithmic_complexity_calculation)

add_compile_options(-std=c++11)

find_package(OpenCV REQUIRED)  

set(igraph OFF)
set(opencv_contrib OFF)
set(zbar_lib OFF)
set(DLib OFF)
    
add_executable(bb_matching 
    src/bb_matching.cpp
    src/lib/utils/geometry_utils.cpp
    src/lib/utils/contour_utils.cpp
    src/lib/types/ExtendedObjectInfo.cpp
    #${eod_srcs}
    #${tinyxml_srcs}
    )
    
target_include_directories(bb_matching
    PRIVATE    
    #src/lib/include
    #src/lib/detectors/include
    #src/lib/relations/include
    src/lib/utils/include
    src/lib/types/include
    ${OpenCV_INCLUDE_DIRS}
        
    )
    
target_link_libraries(bb_matching  
    ${OpenCV_LIBRARIES}      
)


