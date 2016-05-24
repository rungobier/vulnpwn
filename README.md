
# vulnpwn

[![Python 2.7](https://img.shields.io/badge/python-2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://github.com/open-security/vulnpwn/blob/master/LICENSE) [![Twitter](https://img.shields.io/badge/twitter-@vulnpwn-blue.svg)](https://twitter.com/nixawk)


## Overview

**vulnpwn** is a pythonic framework which is similar to [metasploit-framework](https://github.com/rapid7/metasploit-framework). If you are interested in python pragramming, please join us to create a good open-source project.



## Requirements

- Python 2.7+
- Works on Linux, Windows, Mac OSX, BSD

## Usage

The quick way:

```
vulnpwn [master] ./vulnpwn
vulnpwn > show modules
[*]
[*]     exploits/multi/http/apache_struts_dmi_rce
[*]
vulnpwn > use exploits/multi/http/apache_struts_dmi_rce
vulnpwn (exploits/multi/http/apache_struts_dmi_rce) > show options
[*]
[*]     Option     Current Setting                           Description
[*]     ---------  ----------------------------------------  ---------------------
[*]     TARGETURI  /struts2-blank/example/HelloWorld.action  target uri to request
[*]     RHOST      172.16.176.226                            the target host
[*]     RPORT      8080                                      the target port
[*]
vulnpwn (exploits/multi/http/apache_struts_dmi_rce) > run
[*] Exploiting - http://172.16.176.226:8080/struts2-blank/example/HelloWorld.action
[+] Target is vulanable
vulnpwn (exploits/multi/http/apache_struts_dmi_rce) > exit
vulnpwn > exit
```


## Documentation

Documentation is available in [wiki](https://github.com/open-security/vulnpwn/wiki) pages.

## How to Contribute

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork [the repository](https://github.com/open-security/vulnpwn) on GitHub to start making your changes to the **master** branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published. Make sure to add yourself to [THANKS](./THANKS.md).
