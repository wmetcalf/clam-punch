# clam-punch

A highly curated set of signatures for ClamAV 0.99+. MiscreantPunch099-Low.ldb is the marquee ruleset here, is optimized for multiple engines, and uses the newest features. This ruleset is updated often, and would be considered "Low" FPs. 

There are several other rulesets here I would consider looking into adding as well. More info can be found in: https://github.com/wmetcalf/clam-punch/blob/master/MiscreantPunch-Info.txt

If you are running ubuntu and you want to run these..
Edit the file /usr/share/clamav-unofficial-sigs/conf.d/00-clamav-unofficial-sigs.conf

and add the line..

add_dbs="https://raw.githubusercontent.com/wmetcalf/clam-punch/master/MiscreantPunch099-Low.ldb"

if you want to run the single byte EXE XOR sigs also add 

add_dbs="
https://raw.githubusercontent.com/wmetcalf/clam-punch/master/miscreantpunch099.ldb
https://raw.githubusercontent.com/wmetcalf/clam-punch/master/exexor99.ldb
"
Then

sudo -u clamav /usr/sbin/clamav-unofficial-sigs

We will no longer be updating the miscreantpunch.ldb file only the 'MiscreantPunch099-Low.ldb' files which utilizes the 0.99 features.
