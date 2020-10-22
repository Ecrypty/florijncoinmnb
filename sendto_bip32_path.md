### to use bip32 xpub when transfering mn earnings

* Advanced user only
* fee is fixed to 0.000025

- remove receiving_address from masternode.conf if configured
- use python trezorctl/keepkeyctl to get first address and xpub

        cd florijncoinmnb
        . venv3/bin/activate      
        trezorctl get_address -n "44'/5'/1'/0/0" -c Florijncoin
        trezorctl get_public_node -n “44'/5'/1'/0"


- edit config.py, add xpub as default_receiving_address
- run florijncoinmnb -c, check if match an address shown