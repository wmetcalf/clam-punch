# clam-punch
If you are running ubuntu and you want to run these..
Edit the file /usr/share/clamav-unofficial-sigs/conf.d/00-clamav-unofficial-sigs.conf

and add the line..

add_dbs="https://raw.githubusercontent.com/wmetcalf/clam-punch/master/miscreantpunch099.ldb"

if you want to run the single byte EXE XOR sigs also add 

add_dbs="https://raw.githubusercontent.com/wmetcalf/clam-punch/master/exexor99.ldb"

Then

sudo -u clamav /usr/sbin/clamav-unofficial-sigs

I will no longer be updating the miscreantpunch.ldb file only the miscreantpunch099.ldb file which utilizes the 0.99 features.
