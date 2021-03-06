from conans.model.conan_file import ConanFile
from conans import CMake, tools
import os


############### CONFIGURE THESE VALUES ##################
default_user = "lasote"
default_channel = "testing"
#########################################################

channel = os.getenv("CONAN_CHANNEL", default_channel)
username = os.getenv("CONAN_USERNAME", default_user)


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "libpng/1.6.23@%s/%s" % (username, channel)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir="./")
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")
        
    def test(self):
        # if not tools.cross_building(self.settings):
        if not self.settings.os == "Android":
            self.run("cd bin && .%smain" % os.sep)
        assert os.listdir(os.path.join(self.deps_cpp_info["libpng"].rootpath, "licenses"))
