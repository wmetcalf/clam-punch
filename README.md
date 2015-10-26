# clam-punch
If you are running ubuntu and you want to run these..
Edit the file /usr/share/clamav-unofficial-sigs/conf.d/00-clamav-unofficial-sigs.conf

and add the line..

add_dbs="https://raw.githubusercontent.com/wmetcalf/clam-punch/master/miscreantpunch.ldb"

Then

sudo -u clamav /usr/sbin/clamav-unofficial-sigs
