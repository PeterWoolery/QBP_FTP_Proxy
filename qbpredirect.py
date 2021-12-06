import pysftp
import traceback
import datetime
import os
import ftplib
import yaml




def main():
    ''' Check for any new poi file in the /home/accountnumber/out folder
            then process that file
    '''
    
    
    files = os.listdir('/home/{account}/out'.format(ftp_user))
    if len(files) == 0:
            print('No Files to Process')
            exit()
    file = str(files[0])
    input = open("/home/{}}/out/{}".format(ftp_user,file),'r')
    Lines = input.readlines()
    variables = {}
    items = []
    for line in Lines:
            linelist=line.strip().split(",")
            property = linelist[0]
            value = linelist[1]
            if property == 'CLNE':continue
            elif value == '3.0': value = '4.0'
            elif value == 'N30': value = 'N30:I'
            elif property[0] == 'L' and len(property) == 2:
                    quantity = linelist[2]
                    items.append(value+","+str(quantity))
                    variables["LINES"] = items
                    continue
            variables[property] = value
    order_qbp_submit(FT=variables["FT"]
                    ,FV=variables["FV"]
                    ,HEMA=variables["HEMA"]
                    ,HACN=variables["HACN"]
                    ,HLOG=variables["HLOG"]
                    ,HCTN=variables["HCTN"]
                    ,HCPO=variables["HCPO"]
                    ,HSHD=variables["HSHD"]
                    ,HSTO=variables["HSTO"]
                    ,HSVT=variables["HSVT"]
                    ,HTRM=variables["HTRM"]
                    ,CSUB=variables["CSUB"]
                    ,CREP=variables["CREP"]
                    ,CRDL=variables["CRDL"]
                    ,CFAL=variables["CFAL"]
                    ,LINES=variables["LINES"]
                    ,input_file=file)
    os.remove('/home/{}/out/{}'.format(ftp_user,file))

def order_qbp_submit(input_file='',
                    FT='PO',
                    FV='4.0',
                    HEMA='',
                    HACN='0000107206',
                    HLOG='',
                    HCTN='Default User',
                    HCPO=datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S"),
                    HSHD='',
                    HSTO='',
                    HSVT='F4',
                    HTRM='N30:I',
                    HCCA='no',
                    HCNA='',
                    HCRA='',
                    HCA1='',
                    HCA2='',
                    HCCI='',
                    HCST='',
                    HCCO='US',
                    HCZI='',
                    HCEM='',
                    HCPH='',
                    CSUB='yes',
                    CREP='email',
                    CRFM='written',
                    CRDL='detailed',
                    CFAL='ignore',
                    LINES=[]):
    '''Module to format and submit orders to QBP via FTP 
        Ascend's integration was broken and using the wrong format
        QBP provided the docs for this, so this module will be based on the corrections.
        LINES should be passed as follows: ["AB0123,1","AB4567,3","AC8901,7"...]
    '''
    if input_file == '': output = open("output.poi","w")
    else: 
        output = open(input_file,"w") # To-DO: parse input file to build variables, then rebuild package. This is to be able to fix Ascend's broken implementation.
    if len(LINES)==0:
        print('No SKUs to submit')
        return(1)
    output.write('FT,'+FT)
    output.write('\nFV,'+FV)
    output.write('\nHEMA,'+HEMA)
    output.write('\nHACN,'+HACN)
    if HLOG=='': pass
    else: output.write('\nHLOG,'+HLOG)
    output.write('\nHCTN,'+HCTN)
    output.write('\nHCPO,'+HCPO)
    if HSHD=='': pass
    else: output.write('\nHSHD,'+HSHD)
    output.write('\nHSTO,'+HSTO)
    output.write('\nHSVT,'+HSVT)
    output.write('\nHTRM,'+HTRM)
    if HCCA=='no': pass
    else: output.write('\nHCCA,'+HCCA)
    if HCCA=='no': pass
    else: output.write('\nHCNA,'+HCNA)
    if HCCA=='no': pass
    else: output.write('\nHCRA,'+HCRA)
    if HCCA=='no': pass
    else: output.write('\nHCA1,'+HCA1)
    if HCCA=='no': pass
    else: output.write('\nHCA2,'+HCA2)
    if HCCA=='no': pass
    else: output.write('\nHCCI,'+HCCI)
    if HCCA=='no': pass
    else: output.write('\nHCST,'+HCST)
    if HCCA=='no': pass
    else: output.write('\nHCCO,'+HCCO)
    if HCCA=='no': pass
    else: output.write('\nHCZI,'+HCZI)
    if HCCA=='no': pass
    else: output.write('\nHCEM,'+HCEM)
    if HCCA=='no': pass
    else: output.write('\nHCPH,'+HCPH)
    output.write('\nCSUB,'+CSUB)
    output.write('\nCREP,'+CREP)
    output.write('\nCRFM,'+CRFM)
    output.write('\nCRDL,'+CRDL)
    output.write('\nCFAL,'+CFAL)
    output.write('\nCLNE,'+str(len(LINES)))
    linenum = 1
    for line in LINES:
        output.write('\nL'+str(linenum)+','+line)
        linenum = linenum + 1
    output.close()
    ftp_server = ftplib.FTP(ftp_host,ftp_user,ftp_pass)
    ftp_server.encoding = 'utf-8'
    with open(input_file, "rb") as file:
        ftp_server.cwd('out')
        ftp_server.storbinary("STOR {}".format(input_file), file)
    return 0

def get_config():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config
config = get_config()
ftp_host = config['host']
ftp_user = config['account']
ftp_pass = config['password']
if __name__ == '__main__':
    main()