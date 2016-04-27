SFC103 Demo
===========

Overview
--------

SFC103 demo employs a Service Chain with 2 Service Functions (DPI and Firewall) and standalone SFC classifier.

This was modified from https://git.opendaylight.org/gerrit/p/sfc.git to fix some issues when running this demo on Windows environment.  

Topology
-------

                           +-----------------+
                           |       SFC       |
                           |   192.168.1.5   |
                           +-----------------+
                       /      |          |     \
                    /         |          |         \
                /             |          |             \
+---------------+  +--------------+   +--------------+  +---------------+
|  Classifier1  |  |    SFF1      |   |     SFF2     |  |  Classifier2  |
|  192.168.1.10 |  | 192.168.1.20 |   | 192.168.1.50 |  |  192.168.1.60 |
+---------------+  +--------------+   +--------------+  +---------------+
                              |          |
                              |          |
                   +---------------+  +--------------+
                   |     DPI-1     |  |     FW-1     |
                   | 192.168.1.30  |  | 192.168.1.40 |
                   +---------------+  +--------------+

Setup Demo
----------
1. Install virtualbox & vagrant in your environment
2. ./demo.sh


Cleanup Demo
------------
1. vagrant destroy -f


Trouble Shooting(TBD)
--------------------
1. vagrant ssh <vm-hostname>
2. check nohup.out file for erros
