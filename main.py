import os
import configparser

configParser = configparser.RawConfigParser()
configFilePath = r'./variables-config.txt'
configParser.read(configFilePath)

directory_to_search = configParser.get('Setup', 'directory_path')


class DirWalker(object):

    def walk(self, source_directory, callback):
        # walks a directory, and executes a callback on each file

        directory = os.path.abspath(source_directory)
        for file in [file for file in os.listdir(directory) if not file in [".", ".."]]:
            file_full_path = os.path.join(directory, file)

            if os.path.isdir(file_full_path):
                self.walk(file_full_path, callback)
            else:
                callback(file_full_path)


def replace_colors_with_variables(file):
    with open(file, 'r') as input_file:
        file_data = input_file.read()

    variables_dictionary = dict(configParser.items('Variables'))

    for key, value in variables_dictionary.items():
        file_data = file_data.replace(value, 'var(--' + key + ')')

    with open(file, 'w') as output_file:
        output_file.write(file_data)


DirWalker().walk(directory_to_search, replace_colors_with_variables)
