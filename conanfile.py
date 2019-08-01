#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile, tools, CMake


class LibZipperConan(ConanFile):

    name = "zipper"
    version = "0.9.1"
    url = "http://github.com/fbergmann/conan-zipper"
    homepage = "https://github.com/fbergmann/zipper/"
    author = "Frank Bergmann"
    license = "MIT"

    description = ("C++ wrapper around minizip compression library"
                    ""
                    "Zipper's goal is to bring the power and simplicity of minizip to a more object oriented/c++ user friendly library. It was born out of the necessity of a compression library that would be reliable, simple and flexible. By flexibility I mean supporting all kinds of inputs and outputs, but specifically been able to compress into memory instead of been restricted to file compression only, and using data from memory instead of just files as well.")

    settings = "os", "arch", "compiler", "build_type"

    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }

    default_options = (
        "shared=False",
        "fPIC=True"
    )

    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

        self.requires("zlib/1.2.11@conan/stable")
        self.options['zlib'].shared = self.options.shared

    def source(self):
        git = tools.Git("src")
        git.clone("https://github.com/fbergmann/zipper/")
        git.run('submodule init')
        git.run('submodule update')
        tools.replace_in_file('src/CMakeLists.txt', "project(zipper)", '''project(zipper)

include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure(self, cmake):
        args = ['-DBUILD_TEST=OFF']
        if self.settings.compiler == 'Visual Studio' and 'MT' in self.settings.compiler.runtime:
            args.append('-DWITH_STATIC_RUNTIME=ON')
        if not self.options.shared:
            args.append('-DBUILD_SHARED_VERSION=OFF')

        cmake.configure(build_folder="build", args=args, source_folder="src")

    def build(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.install()
        self.copy("*.lib", dst="lib", keep_path=False)
        if self.settings.os == "Windows":
            self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):

        libfile = "libZipper"

        if not self.settings.os == "Windows":
            if self.options.shared:
                if self.settings.os == "Linux":
                    libfile += ".so"
                if self.settings.os == "Macos":
                    libfile += ".dylib"
            else:
                libfile += "-static.a"
        else:
            if self.options.shared:
                libfile += ".dll"
            else:
                libfile += "-static.lib"

        self.cpp_info.libs = [libfile]
