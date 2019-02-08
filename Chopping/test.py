# Sources
# https://www.tutorialspoint.com/python3/python_command_line_arguments.htm

#!/usr/bin/python3
import subprocess, sys, getopt

def main(argv):
    input = 'unknown'
    output = 'unknown'
    dimensions = 0
    try:
        opts, args = getopt.getopt(argv, "i:o:d:", ["input=", "output=", "dimensions="])
    except getopt.GetoptError:
        print("test.py -i <inputfile> -o <outputfile> -d <dimensions>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("test.py -i <inputfile> -o <outputfile> -d <dimensions>")
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-d", "--dimensions"):
            dimensions = arg + 'x' + arg + '@'
    print ('Input file is', input)
    print ('Output file is', output)
    print ('Dimensions are', dimensions[:-1])
    # convert test_leaf.png: -crop 3x3@ +repage +adjoin test_leaf_3x3@_%d.png
    command = ['convert', input + '.png', '-crop', dimensions, '+repage', '+adjoin', output + '_' + dimensions + '_%d.png']
    subprocess.call(command, shell = False)

if __name__ == "__main__":
    main(sys.argv[1:])
