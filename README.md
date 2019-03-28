# custom-vision-download-project
Example how to download the data in a custom vision project.

# How to use

## Install Python

*[Python](https://www.python.org/downloads/)
*[Pip](https://pip.pypa.io/en/stable/installing/)

## Get the Custom Vision SDK
```
pip install azure-cognitiveservices-vision-customvision
```
## Clone this repo
```
git clone https://github.com/areddish/custom-vision-download-project
```
## Find your project ID
1. Navigate to https://customvision.ai
2. Find the project you want to download
3. Click on the Project
4. Click on the gear icon (settings) and get the Project ID & your training key

## Run the tool
```
python project_downloader -p "<project id from previous step>" -k "<your training key>"
```

This will emit some project info download the project images with some metadata into the current directory. To change the directory it downloads to pass the -d "path to where to download to" on the command line.
