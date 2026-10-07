cmake_minimum_required(VERSION 3.16)
project(sim800_at_timeouts LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(sim800_at_timeouts INTERFACE)
target_include_directories(sim800_at_timeouts INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

enable_testing()
add_executable(test_generated_headers tests/test_generated_headers.cpp)
target_link_libraries(test_generated_headers PRIVATE sim800_at_timeouts)
add_test(NAME test_generated_headers COMMAND test_generated_headers)

add_executable(test_doc_examples tests/test_doc_examples.cpp)
target_link_libraries(test_doc_examples PRIVATE sim800_at_timeouts)
add_test(NAME test_doc_examples COMMAND test_doc_examples)
