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

    # define dictionary URLs here
    empdict = "http://www.blacktraffic.co.uk/pw-dict-public/empdict.zip"
    JksPrivkPrepare = "https://github.com/floyd-fuh/JKS-private-key-cracker-hashcat/raw/master/JksPrivkPrepare.jar"
    # change this to your preferred hashcat version
    hashcat_latest = "https://hashcat.net/files/hashcat-6.1.1.7z"
    hashcat_file = "hashcat-6.1.1.7z"

    btexec('mkdir dict')
    #check for file existence and download
    print("Installing configparser and other dependencies - needs 'pip3' on path")
    btexec("pip3 install -r requirements.txt")

    print("Installing impacket - needs 'pip2' on path. this will only affect Windows IFM formats if it's not installed.")
    btexec("pip2 install impacket==0.9.19")
       
    print("Checking for dictionary files - will download some if not present...")
    if not is_non_zero_file('dict/breachcompilation.txt'):
        if not is_non_zero_file('empdict.zip'):
            try:
                urllib.request.urlretrieve (empdict, "empdict.zip")
            # add error handling so script doesn't break if URL not found    
            except urllib.error.HTTPError:
                print('Check the dictionary URLs has not been removed - HTTP error at f"{empdict}" ')
        print("Got dictionary zip, expanding...")    
        zip_ref = zipfile.ZipFile('empdict.zip', 'r')
        zip_ref.extractall('.')
        zip_ref.close()

    if not is_non_zero_file(hashcat_file):
        print("Got hashcat-5.1.0, expanding...")    
        urllib.request.urlretrieve(hashcat_latest, hashcat_file)
        btexec('7z x f"{hashcat_file}"')

    print("Getting JksPrivkPrepare.jar - for Java keystores")
    if not is_non_zero_file('JksPrivkPrepare.jar'):
        urllib.request.urlretrieve(JksPrivkPrepare,"JksPrivkPrepare.jar")

    print("Getting impacket-0.9.19 - might need to get a different one to match the pip install of impacket")
    if not is_non_zero_file('impacket_0_9_19.zip'):
        urllib.request.urlretrieve("https://github.com/CoreSecurity/impacket/archive/impacket_0_9_19.zip","impacket_0_9_19.zip")
        
    zip_ref = zipfile.ZipFile('impacket_0_9_19.zip', 'r')
    zip_ref.extractall('.')
    zip_ref.close()

    try:
        os.rename('impacket-impacket_0_9_19','impacket')
    except:
        print("Couldn't rename impacket - assuming already exists")

    if not is_non_zero_file('bleeding-jumbo.zip'):
        urllib.request.urlretrieve("https://github.com/magnumripper/JohnTheRipper/archive/bleeding-jumbo.zip","bleeding-jumbo.zip")
        
    zip_ref = zipfile.ZipFile('bleeding-jumbo.zip', 'r')
    zip_ref.extractall('.')
    zip_ref.close()

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
