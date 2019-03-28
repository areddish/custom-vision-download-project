# Download a project

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient

import os
import sys
import requests
import argparse

def download_image(uri, name):
    req = requests.get(uri, stream=True)
    if req.status_code == 200:
        with open(name, 'wb') as image_file:
            for chunk in req.iter_content(1024):
                image_file.write(chunk)
    else:
        print("ERROR!: " + req.status_code)

def download_images(trainer, project_id, location):
    count = trainer.get_tagged_image_count(project_id)
    print ("Found:",count,"tagged images.")

    downloaded = 0
    while(count > 0):
        # Download the images in batches
        count_to_download = min(count, 50)
        print ("Getting", count_to_download, "images")
        images = trainer.get_tagged_images(project_id, take=count_to_download, skip=downloaded)
        for i in images:
            print ("Downloading", i.id, i.original_image_uri)
            download_image(i.original_image_uri, location+i.id)
            print ("Creating meta data for: ", i.id)
            with open(location+i.id+".metadata", 'wt') as image_file:
                print ("Tag Name, Tag Id", file=image_file)
                for t in i.tags:
                    print(t.tag_name, ",", t.tag_id, file=image_file)
                if i.regions:
                    print("Region Id, Tag Id, Left, Top, Width, Height", file=image_file)
                    for r in i.regions:
                        print (r.region_id, ",", r.tag_id, ",", r.left, ",", r.top, ",", r.width, ",", r.height, file=image_file)
                
        downloaded += count_to_download
        count -= count_to_download

    # Downlaod any untagged images that may exist.
    count = trainer.get_untagged_image_count(project_id)
    print ("Found:", count, "untagged images.")
    downloaded = 0
    while(count > 0):
        count_to_download = min(count, 50)
        print ("Getting", count_to_download, "images")
        images = trainer.get_untagged_images(project_id, take=count_to_download, skip=downloaded)
        for i in images:
            print ("Downloading", i.id, i.original_image_uri)
            download_image(i.original_image_uri, location+i.id)
        downloaded += count_to_download
        count -= count_to_download

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--project", action="store", type=str, help="Project ID", dest="project_id", default=None)
    arg_parser.add_argument("-k", "--key", action="store", type=str, help="Training-Key", dest="training_key", default=None)
    arg_parser.add_argument("-e", "--endpoint", action="store", type=str, help="Endoint", dest="endpoint", default="https://southcentralus.api.cognitive.microsoft.com")
    arg_parser.add_argument("-d", "--dir", action="store", type=str, help="Target directory", dest="dir", default=".\\")
    args = arg_parser.parse_args()

    if (not args.project_id or not args.training_key):
        arg_parser.print_help()
        exit(-1)

    print ("Collecting information for source project:", args.project_id)

    # Create hte client
    trainer = CustomVisionTrainingClient(args.training_key, endpoint=args.endpoint)

    # Get the project
    project = trainer.get_project(args.project_id)
    print ("Downloading project:", project.name)
    print ("\tDescription: ", project.description)
    print ("\tDomain: ", project.settings.domain_id)

    # get tags
    tags = trainer.get_tags(project.id)
    print ("Found:", len(tags), "tags.")
    with open("tags.txt", "wt") as tags_file:
        for tag in tags:
            print(tag.name, tag.id, tag.type, file = tags_file)

    download_images(trainer, project.id, args.dir)
