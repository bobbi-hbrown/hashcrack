#
#Released as open source by NCC Group Plc - http://www.nccgroup.com/
#
#Developed by Jamie Riden, jamie.riden@nccgroup.com
#
#http://www.github.com/nccgroup/hashcrack
#
#This software is licensed under AGPL v3 - see LICENSE.txt
#

import os
import urllib.request
import urllib.error
import zipfile
import shutil

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def btexec( sexec ):
    print('RUN: '+sexec) 
    os.system(sexec)
    
def main():

    # TODO - convert these to environment variables
    # define dictionary URLs here
    empdict_filename = "empdict.zip"
    empdict_url = "http://www.blacktraffic.co.uk/pw-dict-public/empdict.zip"

    JksPrivkPrepare_filename = "JksPrivkPrepare.jar"
    JksPrivkPrepare_url = "https://github.com/floyd-fuh/JKS-private-key-cracker-hashcat/raw/master/JksPrivkPrepare.jar"

    impacket_filename = "impacket_0_9_19.zip"
    impacket_url = "https://github.com/CoreSecurity/impacket/archive/impacket_0_9_19.zip"

    bleeding_jumbo_filename = "bleeding-jumbo.zip"
    bleeding_jumbo_url = 
    # change this to your preferred hashcat version
    hashcat_url = "https://hashcat.net/files/hashcat-6.1.1.7z"
    hashcat_filename = "hashcat-6.1.1.7z"

    def download_files(filename, url, output_message):
        print(output_message) 
        if not is_non_zero_file(filename):
            try:   
                urllib.request.urlretrieve(url, filename)
            except urllib.error.HTTPError:
                print('Check you have supplied the correct URLs/filename versions on lines 26-31: f"{url}" ')  
    
    def extract_zip(filename):
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall('.')
        zip_ref.close()

    btexec('mkdir dict')
    #check for file existence and download
    print("Installing configparser and other dependencies - needs 'pip3' on path")
    btexec("pip3 install -r requirements.txt")

    print("Installing impacket - needs 'pip2' on path. this will only affect Windows IFM formats if it's not installed.")
    btexec("pip2 install impacket==0.9.19")

    # Download and unzip the dictionaries used for hashing
    download_files(empdict_filename, empdict_url, "Checking for dictionary files - will download some if not present...")
    extract_zip(empdict_filename)

    # Download and unzip your specified version of hashcat
    download_files(hashcat_filename, hashcat_url, 'Got f"{hashcat_filename}", expanding...')
    btexec('7z x f"{hashcat_file}"')

    # Download JksPrivkPrepare.jar file
    download_files(JksPrivkPrepare_filename, JksPrivkPrepare_url, "Getting JksPrivkPrepare.jar - for Java keystores")

    # Download and unzip your specified version of impacket, then rename
    download_files(impacket_filename, impacket_url, "Getting impacket-0.9.19 - might need to get a different one to match the pip install of impacket")
    extract_zip(impacket_filename)

    try:
        os.rename(impacket_filename,'impacket')
    except:
        print("Couldn't rename impacket - assuming already exists")

    download_files(bleeding_jumbo_filename, bleeding_jumbo_url, 'Got f"{bleeding_jumbo_filename}", expanding...' )
    extract_zip(bleeding_jumbo_filename)


    try:        
        os.rename('JohnTheRipper-bleeding-jumbo','john')
    except:
        print("Couldn't rename john - assuming already exists")
        
    shutil.copy2('rules/leet2.rule','hashcat-5.1.0/rules/')
    shutil.copy2('rules/allcase.rule','hashcat-5.1.0/rules/')
    shutil.copy2('rules/nsav2dive.rule','hashcat-5.1.0/rules/')
    shutil.copy2('rules/l33tpasspro.rule','hashcat-5.1.0/rules/')

    print("Done - now change the paths in hashcrack.cfg to point to dict, rules, hashcat")   

if __name__== "__main__":
  main()
