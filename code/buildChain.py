#!/usr/bin/env python
# coding: utf-8

# In[2]:


# %load /gpfs/commons/groups/gursoy_lab/aelhussein/Code/SAMChain/SAMchain/buildChain.py
'''
buildChain-mimic.py
Initializes an empty blockchain for storing comma-separated text file data
Usage: $ python buildChain-mimic.py <chainName> <data_path> <multichain_directory> 
modified by AE 02/2022
'''

import sys
import time
import math
import binascii
import argparse
import subprocess
from subprocess import Popen, PIPE
import os
import psutil
import time
import pandas as pd
#define global variables
chrType = -1


# In[ ]:


#create a chain given the name of the chain, the location of the multichain program, and the datadir in which to keep the chain
def createChain(chainName, multichainLoc, datadir):
    createCommand=multichainLoc+'multichain-util create {} -datadir={} -anyone-can-admin=true'.format(chainName, datadir)
    runCommand = multichainLoc+'multichaind {} -datadir={} -daemon'.format(chainName, datadir)

    #make the chain
    procCreate = subprocess.Popen(createCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_valc, stderr_valc = procCreate.communicate()
    if((b"error" in stderr_valc) or (b"ERROR" in stderr_valc)):
        print("Could not create chain (it probably already exists)")
    else:
        print("Created chain")

    #start the chain
    daemonOut = subprocess.call(runCommand.split()) #returns 0 whether or not it had an error; subprocess hangs 
    #because output is too long (known subprocess bug); just relying on chain creation to catch bug
    time.sleep(1)
    return


# In[ ]:


######################################################################################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-cn", "--chainName", help = "the name of the chain to store data", default = "chain1")
    parser.add_argument("-ml", "--multichainLoc", help = "path to multichain commands", default = "")
    parser.add_argument("-dr", "--datadir", help = "path to store the chain")
    args = parser.parse_args()

    start = time.time()
    try:
        #make a chain
        print("--CHAIN CREATION--")
        createChain(args.chainName, args.multichainLoc, args.datadir)
        print("Chain construction complete! Chain name: "+args.chainName)
        end = time.time()

        e = int(end - start)
        print('\n\n Time elapsed:\n\n')
        print( '{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

        process = psutil.Process(os.getpid())
        print('\n\n Total memory in bytes:\n\n')
        print(process.memory_info().rss)
    
    except:
        sys.stderr.write("\nERROR: Failed chain creation. Please try again.\n")
        quit()
        


# In[ ]:


if __name__ == "__main__":
    main()
