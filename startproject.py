"""
Start Project generates a new project in the current directory
(Written in Python 3)

Start Project takes the following input:

    1.  Name -------------------- Project name
    2.  Language ---------------- Programming Language Name
    3.  Flag List (optional) ---- List of compiler flags for compiled languages

A new directory called [Name] will be made in the current directory.  This
subdirectory will also contain the following files:

    1.  .gitignore
    2.  .ycm_extra_conf.py
    3.  Makefile without dependencies

v.1.0, August 2016
By Joseph Franc
"""


import os
import sys
import shutil

HOME_DIRECTORY = os.path.expanduser('~')
YCM_FILE_NAME = '.ycm_extra_conf.py'
YCM_CONFIG_PATH = HOME_DIRECTORY + '/dotfiles/' + YCM_FILE_NAME
YCM_FLAG_VAR_NAME = 'flags'



def startProject(name, language, flags):

    # Create the appropriately named project directory
    src_directory = name+'/src'
    try: os.makedirs(src_directory)
    except OSError:
        sys.stderr.write('Could not make project directory\n')
        sys.exit(1)

    # Change to the root directory
    try: os.chdir(name)
    except OSError:
        sys.stderr.write('You got an impossible error\n')
        raise

    # Make .gitignore
    with open('.gitignore', 'w') as git_ignore:
        git_ignore.write('*.swp\n'
                         + '*.o\n'
                         + '*.gz\n'
                         + '*~\n'
                         + '.ycm_extra_conf.py\n'
                         + name)

    # If C++ project, create necessary files
    if language == 'cpp':
        with open('Makefile', 'w') as makefile:
            print('File opened')
           
            # Create a Makefile
            makefile.write('COMPILER = g++\nFLAGS =')
            # Enter each flag
            for flag in flags: makefile.write(' ' + flag)
            # Create some default commands
            makefile.write('\n'
                           + '.PHONY:\trelease debug clean profile\n'
                           + 'release:\tFLAGS+= -O3 -DNDEBUG\n'
                           + 'release:\tall\n'
                           + 'debug:\tFLAGS += -g3 -O0 -DDEBUG\n'
                           + 'clean:\n\trm -f ' + name + '*.o\n'
                           + 'profile:\tFLAGS += -pg\n'
                           + 'profile:\tall\n'
                           + 'all:\t' + name + '\n'
                           + '\n# DEPENDENCIES\n')

        # Write the .ycm config file for C-style langauges
        # Copy the template with the flags added in
        if flags:
            new_file = ''
            with open(YCM_CONFIG_PATH, 'r') as ycm_file:
                # Skip to flag var declaration in file
                for line in ycm_file:
                    new_file += line
                    if YCM_FLAG_VAR_NAME in line: break
                   
                # Write the flags into the new file
                for flag in flags[:-1]: new_file += '\n\t' + flag + ','
                # Write final flag without a comma
                new_file += '\n\t' + flags[-1]
                # Write the rest of the file
                for line in ycm_file: new_file += line 

            # Write the new file in the current dirctory
            with open(YCM_FILE_NAME, 'w') as new_ycm_file:
                new_ycm_file.write(new_file)

    # Return to the original directory
    os.chdir('..')



# Run when invoked as a program
if __name__ is '__main__':

    # Sanitize input
    if len(sys.argv) < 3:
        sys.stderr.write('Please supply required arguments\n')
        sys.exit(2)
    
    starting_directory = os.getcwd()
    # Try to run the script
    try: startProject(sys.argv[1], sys.argv[2], sys.argv[3:])
    # If the script failed, return to the original directory
    except:
        os.chdir(starting_directory)
        raise
