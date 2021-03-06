#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mnb.py

# code from https://github.com/florijncoinpay/electrum-florijncoin
# most bitcoin code from https://github.com/vbuterin/pybitcointools
# ref :
# https://github.com/florijncoinpay/florijncoin/blob/v0.12.1.x/florijncoin-docs/protocol-documentation.md
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'florijncoinlib'))

import argparse
import time
import signal
import ssl
from collections import Counter

from florijncoin_b58 import *
from florijncoin_ecdsa import *
from florijncoin_hashs import *
from florijncoin_jacobian import *
from florijncoin_keys import *
from florijncoin_script import *
from florijncoin_tx import *
from florijncoin_utils import *
from mnb_explorer import *
from mnb_hwwallet import *
from mnb_makemnb import *
from mnb_maketx import *
from mnb_makevote import *
from mnb_misc import *
from mnb_mnconf import *
from mnb_rpc import *
from mnb_signing import *
from mnb_sshtunnel import *
from mnb_start import *
from mnb_vote import *
from mnb_xfer import *

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


def main(args):

    logo_show(True)

    ssl._create_default_https_context = ssl._create_unverified_context

    serverURL = 'https://' + rpcuser + ':' + rpcpassword + '@' + rpcbindip + \
        ':' + str(rpcport if USE_SSH_TUNNEL is False else SSH_LOCAL_PORT)

    access = AuthServiceProxy(serverURL)

    if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
        client, signing, mpath = check_hw_wallet()

    else:
        client, signing, bip32, mpath, xpub = check_hw_wallet()

    if client is None:
        sys.exit()

    if len(args.account_number) > 0:
        for i in args.account_number:
            account_no = i

            bip32_path = "44'/5'/" + str(account_no) + "'/0" if MAINNET else "44'/1'/" + str(account_no) + "'/0"
        
            if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
                
                try:
        
                    print('**** ====> account_no : %s' % i)
            
                    for i in range(max_gab):
                        addr_path = bip32_path + '/' + str(i)
                        nodedata = client.getWalletPublicKey(addr_path)
                        address   = (nodedata.get('address')).decode("utf-8")
            
                        addr_balance = round(
                            Decimal(
                                getaddressbalancewithoutexcept(
                                    address,
                                    access) / 1e8),
                            8)
                
                        print(
                            coin_name +
                            ' address: ' +
                            '{:20}'.format(addr_path) +
                            ' ' +
                            address +
                            ' ' +
                                '{:13.8f}'.format(addr_balance))            
                    print()
            
                except AssertionError as e:
                    err_msg = str(e.args)
                    print_err_exit(
                        get_caller_name(),
                        get_function_name(),
                        err_msg)
            
                except Exception as e:
                    err_msg = str(e.args)
                    print_err_exit(
                        get_caller_name(),
                        get_function_name(),
                        err_msg)
            
                except KeyboardInterrupt:
                    print_err_exit(
                        get_caller_name(),
                        get_function_name(),
                        "KeyboardInterrupt")
        
            else:
                keypath = bip32_path
            
                try:
                    #bip32_path = client.expand_path(keypath)
                    # xpub = bip32.serialize(
                    #    client.get_public_node(bip32_path).node,
                    #    (0x0488B21E if MAINNET else 0x043587CF))
            
            
                    print('**** ====> account_no : %s' % i)
            
                    for i in range(max_gab):
                        child_path = '%s%s' % (keypath + '/', str(i))
                        address = client.get_address(
                            coin_name, client.expand_path(child_path))
                        publicnode = client.get_public_node(
                            client.expand_path(child_path)).node.public_key.hex()

            
                        addr_balance = round(
                            Decimal(
                                getaddressbalancewithoutexcept(
                                    address,
                                    access) / 1e8),
                            8)
            
                        print(
                            coin_name +
                            ' address: ' +
                            '{:20}'.format(child_path) +
                            ' ' +
                            address +
                            ' ' +
                            '{:13.8f}'.format(addr_balance))
                        
                except AssertionError as e:
                    err_msg = str(e.args)
                    print_err_exit(
                        get_caller_name(),
                        get_function_name(),
                        err_msg)
            
                except Exception as e:
                    err_msg = str(e.args)
                    print_err_exit(
                        get_caller_name(),
                        get_function_name(),
                        err_msg)
            
                except KeyboardInterrupt:
                    print_err_exit(
                        get_caller_name(),
                        get_function_name(),
                        "KeyboardInterrupt")
        


    else:
        print('--> enter at leat one account_number')
        sys.exit()


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(dest='account_number',
                        metavar='account_number[s] to check',
                        nargs='*')


    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()

    return parser.parse_args()



if __name__ == "__main__":
    if (sys.version_info < (3, 5, 1)):
        sys.exit('need python 3.5.1')

    args = parse_args()
    main(args)
