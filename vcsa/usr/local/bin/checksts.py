#!/opt/vmware/bin/python


"""
Copyright 2020-2022 VMware, Inc.  All rights reserved. -- VMware Confidential
Author:  Keenan Matheny (keenanm@vmware.com)

"""
##### BEGIN IMPORTS #####

import os
import sys
import json
import subprocess
import re
import pprint
import ssl
from datetime import datetime, timedelta
import textwrap
from codecs import encode, decode
import subprocess
from time import sleep
try:
    # Python 3 hack.
    import urllib.request as urllib2
    import urllib.parse as urlparse
except ImportError:
    import urllib2
    import urlparse

sys.path.append(os.environ['VMWARE_PYTHON_PATH'])
from cis.defaults import def_by_os
sys.path.append(os.path.join(os.environ['VMWARE_CIS_HOME'],
                def_by_os('vmware-vmafd/lib64', 'vmafdd')))
import vmafd
from OpenSSL.crypto import (load_certificate, dump_privatekey, dump_certificate, X509, X509Name, PKey)
from OpenSSL.crypto import (TYPE_DSA, TYPE_RSA, FILETYPE_PEM, FILETYPE_ASN1 )

today = datetime.now()
today = today.strftime("%d-%m-%Y")

vcsa_kblink = "https://kb.vmware.com/s/article/76719"
win_kblink = "https://kb.vmware.com/s/article/79263"

##### END IMPORTS #####

class parseCert( object ):
    # Certificate parsing

    def format_subject_issuer(self, x509name): 
        items = []
        for item in x509name.get_components():
            items.append('%s=%s' %  (decode(item[0],'utf-8'), decode(item[1],'utf-8')))
        return ", ".join(items)

    def format_asn1_date(self, d):
        return datetime.strptime(decode(d,'utf-8'), '%Y%m%d%H%M%SZ').strftime("%Y-%m-%d %H:%M:%S GMT")

    def merge_cert(self, extensions, certificate):
        z = certificate.copy()
        z.update(extensions)
        return z

    def __init__(self, certdata):

        built_cert = certdata
        self.x509 = load_certificate(FILETYPE_PEM, built_cert)
        keytype = self.x509.get_pubkey().type()
        keytype_list = {TYPE_RSA:'rsaEncryption', TYPE_DSA:'dsaEncryption', 408:'id-ecPublicKey'}
        extension_list = ["extendedKeyUsage",
                        "keyUsage",
                        "subjectAltName",
                        "subjectKeyIdentifier",
                        "authorityKeyIdentifier"]
        key_type_str = keytype_list[keytype] if keytype in keytype_list else 'other'

        certificate = {}
        extension = {}
        for i in range(self.x509.get_extension_count()):
            critical = 'critical' if self.x509.get_extension(i).get_critical() else ''

            if decode(self.x509.get_extension(i).get_short_name(),'utf-8') in extension_list:
                extension[decode(self.x509.get_extension(i).get_short_name(),'utf-8')] = self.x509.get_extension(i).__str__()

        certificate = {'Thumbprint': decode(self.x509.digest('sha1'),'utf-8'), 'Version': self.x509.get_version(),
         'SignatureAlg' : decode(self.x509.get_signature_algorithm(),'utf-8'), 'Issuer' :self.format_subject_issuer(self.x509.get_issuer()), 
         'Valid From' : self.format_asn1_date(self.x509.get_notBefore()), 'Valid Until' : self.format_asn1_date(self.x509.get_notAfter()),
         'Subject' : self.format_subject_issuer(self.x509.get_subject())}
        
        combined = self.merge_cert(extension,certificate)
        cert_output = json.dumps(combined)

        self.subjectAltName = combined.get('subjectAltName')
        self.subject = combined.get('Subject')
        self.validfrom = combined.get('Valid From')
        self.validuntil = combined.get('Valid Until')
        self.thumbprint = combined.get('Thumbprint')
        self.subjectkey = combined.get('subjectKeyIdentifier')
        self.authkey = combined.get('authorityKeyIdentifier')
        self.combined = combined

class parseSts( object ):

    def __init__(self):
        self.processed = []
        self.results = {}
        self.results['expired'] = {}
        self.results['expired']['root'] = []
        self.results['expired']['leaf'] = []
        self.results['valid'] = {}
        self.results['valid']['root'] = []
        self.results['valid']['leaf'] = []

    def get_certs(self,force_refresh):
        urllib2.getproxies = lambda: {}
        vmafd_client = vmafd.client('localhost')
        domain_name = vmafd_client.GetDomainName()

        dc_name = vmafd_client.GetAffinitizedDC(domain_name, force_refresh)
        if vmafd_client.GetPNID() == dc_name:
            url = (
                'http://localhost:7080/idm/tenant/%s/certificates?scope=TENANT'
                % domain_name)
        else:
            url = (
                'https://%s/idm/tenant/%s/certificates?scope=TENANT'
                % (dc_name,domain_name))
        return json.loads(urllib2.urlopen(url).read().decode('utf-8'))

    def check_cert(self,certificate):
        cert = parseCert(certificate)
        certdetail = cert.combined

            #  Attempt to identify what type of certificate it is
        if cert.authkey:
            cert_type = "leaf"
        else:
            cert_type = "root"
        
        #  Try to only process a cert once
        if cert.thumbprint not in self.processed:
            # Date conversion
            self.processed.append(cert.thumbprint)
            exp = cert.validuntil.split()[0]
            conv_exp = datetime.strptime(exp, '%Y-%m-%d')
            exp = datetime.strftime(conv_exp, '%d-%m-%Y')
            now = datetime.strptime(today, '%d-%m-%Y')
            exp_date = datetime.strptime(exp, '%d-%m-%Y')
            
            # Get number of days until it expires
            diff = exp_date - now
            certdetail['daysUntil'] = diff.days

            # Sort expired certs into leafs and roots, put the rest in goodcerts.
            if exp_date <= now:
                self.results['expired'][cert_type].append(certdetail)
            else:
                self.results['valid'][cert_type].append(certdetail)
    
    def execute(self):

        json = self.get_certs(force_refresh=False)
        for item in json:
            for certificate in item['certificates']:
                self.check_cert(certificate['encoded'])
        return self.results

def main():

    warning = False
    warningmsg = '''
    WARNING! 
    You have expired STS certificates.  Please follow the KB corresponding to your OS:
    VCSA:  %s
    Windows:  %s
    ''' % (vcsa_kblink, win_kblink)
    parse_sts = parseSts()
    results = parse_sts.execute()
    valid_count = len(results['valid']['leaf']) + len(results['valid']['root'])
    expired_count = len(results['expired']['leaf']) + len(results['expired']['root'])
          
    
    #### Display Valid ####
    print("\n%s VALID CERTS\n================" % valid_count)
    print("\n\tLEAF CERTS:\n")
    if len(results['valid']['leaf']) > 0:
        for cert in results['valid']['leaf']:
            print("\t[] Certificate %s will expire in %s days (%s years)." % (cert['Thumbprint'], cert['daysUntil'], round(cert['daysUntil']/365)))
    else:
        print("\tNone")
    print("\n\tROOT CERTS:\n")
    if len(results['valid']['root']) > 0:
        for cert in results['valid']['root']:
            print("\t[] Certificate %s will expire in %s days (%s years)." % (cert['Thumbprint'], cert['daysUntil'], round(cert['daysUntil']/365)))
    else:
        print("\tNone")


    #### Display expired ####
    print("\n%s EXPIRED CERTS\n================" % expired_count)
    print("\n\tLEAF CERTS:\n")
    if len(results['expired']['leaf']) > 0:
        for cert in results['expired']['leaf']:
            print("\t[] Certificate: %s expired on %s!" % (cert.get('Thumbprint'),cert.get('Valid Until')))
            continue
    else:
        print("\tNone")

    print("\n\tROOT CERTS:\n")
    if len(results['expired']['root']) > 0:
        for cert in results['expired']['root']:
            print("\t[] Certificate: %s expired on %s!" % (cert.get('Thumbprint'),cert.get('Valid Until')))
            continue
    else:
        print("\tNone")

    if expired_count > 0:
        print(warningmsg)


if __name__ == '__main__':
    exit(main())

