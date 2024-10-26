import subprocess
import os
import glob
import time

def Compress(handbrake, source, destination):

    try:
        
        # Finding all Video files
        directoryList = os.listdir(source)

    except Exception as error:
        print(f"An error occurred {error}")
        raise SystemExit

    # Looping through each file
    for file in directoryList:

        # Creating the full pathway for handbrake to find the file
        sourceFullPathway = os.path.join(source, file)

        # Creating the full pathway for handbrake to know where to place the file and name it correctly
        destinationFullpath = os.path.join(destination, file.replace(".mkv", ".mp4"))

        print(f"Converting {sourceFullPathway} to {destinationFullpath}")

        # Finding all Videos with the mkv extention
        if sourceFullPathway.endswith(".mkv"):
            exsists = IfFileExsist(file, destinationFullpath)
            if exsists == "N":
                print(f"Skipping over {file}")
                time.sleep(3)
            else:
                # Creating the handbrake commands so it knows which setting to apply to the videos
                handBrakeCommand = [f"{handbrake}", "-i", f"{sourceFullPathway}", "-o", f"{destinationFullpath}", "--preset=Fast 1080p30", "-e", "x264", "-q", "22", "-B", "160", "--all-audio", "--all-subtitles",  "--subtitle-burned=none"]
                
                # Running handbrake in the shell
                subprocess.run(handBrakeCommand, shell=True)
                print(f"Finished Coverting {destinationFullpath}")

    print("Done!")

def IfFileExsist(file, directory):

    override = True
    # Checking pathway to make sure there is no file there with the same name
    if os.path.exists(directory):
        print(f"This {file.replace(".mkv", ".mp4")} already exists")
        while override:

            #Asking if you want to Override the file with the same name
            overrideFile = input(f"Do you want to Override {directory} Y or N: ")

            # Checking if you wanted to override or not
            if overrideFile.upper() == "N":
                override = False
                return "N"
            elif overrideFile.upper() == "Y":
                override = False
                return "Y"
            else:
                print(f"That is not a valid {overrideFile} input please try again!")

def Setup():

    # Home Directory
    homeDirectory = os.path.expanduser('~')

    # Finding Where HandBrakeCLI is located
    findHandBrake = glob.glob(f"{homeDirectory}/**/HandBrakeCLI.*", recursive=True)
    
    # Checking to make sure HandBrakeCLI has been found
    if (findHandBrake == []):
        print(f"Couldn't find HandBrakeCLI. Please make sure that you have HandBrakeCLI in someplace like {os.path.join(homeDirectory, "Downloads")}")
        raise SystemExit()
    else:
        handBrake = findHandBrake[0]

    # Default Pathway
    defaultPathway = os.path.join(homeDirectory, "Videos")

    # Asking Where the Videos are located
    sourceDirectory = input(f"Press Enter to use Default Video Source {defaultPathway} or Enter 1 for Custom : ")
    if sourceDirectory == "1":
        sourceDirectory = input("Enter your Custom pathway to your Videos: ")
        print(f"Using {sourceDirectory}")
    else:
        sourceDirectory = defaultPathway
        print("Using Default Pathway")
        
    # Asking Where the Videos should go after being compressed
    destinationDirectory = input(f"Press Enter to use Default Video Destination {defaultPathway} or Enter 1 for Custom : ")
    if destinationDirectory == "1":
        destinationDirectory = input("Enter your Custom pathway to where you want your videos placed: ")
        print(f"Using {destinationDirectory}")
    else:
        destinationDirectory = defaultPathway
        print("Using Default Pathway")
    
    Compress(handBrake, sourceDirectory, destinationDirectory)

Setup()