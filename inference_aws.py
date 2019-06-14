##############################################
# this script runs inference
# to generate an image based on
# the following inputs
# 1. a text description of the object (MS AttnGAN)
# 2. a outline image of an object (Nvidia GauGan)

# to run this script on AWS Linux Set up the data folder to contain four things:
#
# 'train' folder. This contains 'filenames.pickle' for the training files 'test' folder. This should contain
#  'filenames.pickle' for the test files
#
# 'coco' folder. This should contain all the images from the coco dataset. (train, val and test)
#
# 'captions.pickle' (if you plan to use pre-trained models)
#  Update your configuration files in 'code/cfg/' to point to the parent
#
# directory of the 'coco' folder. E.g: if 'coco' folder is in 'data/coco/coco' path, put the 'data' path in your
# config files as 'data/coco'
#
# ensure that `sudo python3 -V` gives your python 3.6
#
# ensure that `sudo conda install --file requirements.txt` is successful then execute "sudo python3 inference_aws.py"
# #############################################

import os
import boto3

# Part 1
# download data from S3


# code adapted from https://stackoverflow.com/questions/49772151/boto3-download-folder-from-s3
# and https://www.mydatahack.com/comprehensive-guide-to-download-files-from-s3-with-python/


def download_directory_from_s3(bucket_name,
                               remote_directory_name):

    """
    :param bucket_name: string
    :param remote_directory_name: string
    :return: local_path
    """

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for key in bucket.objects.filter(Prefix=remote_directory_name):
        if not os.path.exists(os.path.dirname(key.key)):
            os.makedirs(os.path.dirname(key.key))
        bucket.download_file(key.key, key.key)
        print('Downloaded file with boto3 resource')
    local_path = os.path.dirname(key.key)
    return local_path


download_directory_from_s3('gauganspade', 'datasets_mini')

# add download for attnGAN in WK3

# Part 2-1
# AttnGAN

# to be added: a way to programmatically find the directory then save files

print("MS AttnGAN inference")

bashCommand = 'sudo python3 /home/ubuntu/DeepDeco/src/attngan/code/main.py --cfg ' \
              '/home/ubuntu/DeepDeco/src/attngan/code/cfg/eval_coco.yml --gpu 1 '
print("running bash command")

os.system(bashCommand)