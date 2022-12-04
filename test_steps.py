import os
import re
import pathlib

class TestSteps():

    '''
    directory_start - the root directory to start. Make this the squish suite directory root
    dir_match - name of the directory to match
    file_name_match - name of the file to match
    str_match - regex of pattern to match
    '''

    def __init__(self, directory_start=pathlib.Path(os.getcwd()),
                dir_match="IVVP", file_name_match="test.py",
                str_match=re.compile(r".*test.log\(\s*\"\(\d+\)[ _a-zA-Z0-9]*\"\s*\)")
                ):

        self.directory_start = directory_start
        self.dir_match = dir_match
        self.file_name_match = file_name_match
        self.str_match = str_match

        self._show_params()

    def _show_params(self):
        print("Use params")
        print("base dir:", str(self.directory_start))
        print("dir_match:", str(self.dir_match))
        print("str_match:",str(self.str_match))


    def _create_directory_path(self, sub_path):
        new_dir = self.directory_start / sub_path
        print("Directory:" + str(new_dir))
        return new_dir

    def _create_file_path(self,sub_path,file_name):
        new_file_path = self.directory_start / sub_path / file_name
        print("File:" + str(new_file_path))
        return new_file_path

    def _collect_directories(self):
        dirs = []
        print(self.directory_start)
        with os.scandir(str(self.directory_start)) as it:
            for entry in it:
                if self.dir_match in entry.name and entry.is_dir():
                    dirs.append(self._create_directory_path(entry.name))
        return dirs

    def _get_test_steps(self,directory_name,file_name):
        '''
        iterates each line checking if it matches the regex for a test step
        :param directory_name:
        :param file_name:
        :return: List of strings of test steps
        '''
        test_steps=[]
        full_path = self._create_file_path(directory_name,file_name)
        with open(full_path,'r') as f:
            for line in f:
                #print(line)
                m = re.match(self.str_match,line)
                if m:
                    test_steps.append(m.string)
        return self._filter_steps(test_steps)

    def _filter_steps(self,test_steps):
        '''
        remove the test.log string from the test steps
        :param test_steps:
        :return: test steps without the test.log string
        '''
        tsf=[]
        for ts in test_steps:
            f = ts.find("\"")
            s = ts.find("\"",f+1)
            tsf.append(ts[f+1:s])
        return tsf

    def _output_to_text(self,directory,test_steps):
        '''
        Outputs each test step to a text file
        :param directory:
        :param test_steps:
        :return:
        '''
        output_path = self._create_file_path(str(directory),"test_steps.txt")
        with open(str(output_path),'w') as f:
            for ts in test_steps:
                f.write(ts + "\n")


    def create(self):
        '''
        Public method to create the test steps output file
        :return:
        '''
        dirs = self._collect_directories()
        for d in dirs:
            print("Checking directory ", str(d))
            with os.scandir(str(d)) as it:
                for entry in it:
                    if entry.name.endswith(".py") and entry.is_file() and entry.name == self.file_name_match:
                        print("Getting test steps for ", str(entry.name))
                        test_steps = self._get_test_steps(str(d),entry.name)
                        self._output_to_text(d,test_steps)

def main():
    i = TestSteps()
    i.create()

if __name__ == "__main__":
    main()
