PROJECT(ZipperPackageTest)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()


file(GLOB TEST_SOURCES
  ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp
)

ADD_EXECUTABLE(zipper_test ${TEST_SOURCES})
TARGET_LINK_LIBRARIES(zipper_test ${CONAN_LIBS})
