# Cisco-7906G-SIP
Cisco 7906G SIP Configuration Files (for 3rd party PBXs)

### TFTP/DHCP Configuration

During boot the handsets will discover the TFTP server via DHCP option 66 and/or DHCP option 150. For this example I set option 66 of our VoIP VLAN to the local IP address of our TFTP server. All of the configuration files, firmware files and other customisation files reside in the root directory of the TFTP server, in this case it was `\TFTPBOOT`.

### Base Configuration Files

Each handset will require an SEP configuration file. The filename must be `SEP000000000000.cnf.xml` where the `000000000000` is the MAC address of the Cisco handset.

In the example SEP configuration file, the following values have been set:

    sip.provider.com  <!-- This is the FQDN of the PBX, it can also be an IP address -->
    123.123.123.123   <!-- This is the public IP address of the network the handset resides on, this if for NAT and may not be needed -->
    222               <!-- This is the numerical extension number the handset will have, this must exist on the remote PBX first -->
    pbx-username      <!-- This is the register username for the extension -->
    Pa$$w0rd          <!-- This is the register password for the extension -->
    *55               <!-- This is the direct dial for the PBX's voicemail -->
    
All other settings can be ignored for the purpose of the inital configuration. You must change every occurance of the above settings throughout the configuration file.

### Firmware Versions and Upgrading

The firmware version that has been tested for these configuration files is `SIP11.9-4-2SR1-1S`. You can download the firmware files directly from Cisco - you will need to register for a free account. At the time of writing the link for the firmware files is [here](https://software.cisco.com/download/release.html?mdfid=280607214&softwareid=282074288&os=&release=9.4(2)SR3&relind=AVAILABLE&rellifecycle=&reltype=latest&i=!pp), however, I have included the firmware files in this repository for reference.



