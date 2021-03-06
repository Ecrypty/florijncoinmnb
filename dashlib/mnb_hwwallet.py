import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))


from mnb_misc import *
from config import *

if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
    from btchip.btchip import *
    from btchip.btchipUtils import *

def chain_path(mpath):
    import re
    pathmatch = re.search("^(.*)'/(.*)'/(.*)'/(.*)$", mpath)
    if (pathmatch):
        purpose = pathmatch.group(1)
        coin_type = pathmatch.group(2)
        account = pathmatch.group(3)
        change = pathmatch.group(4)

        printdbg('chain_path : re.search : %s : %s : %s :%s' %
                 (int(purpose), int(coin_type), int(account), int(change)))
        return int(purpose), int(coin_type), int(account), int(change)

    else:
        err_msg = 'check bip32 mpath'
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)


def get_chain_pubkey(client):
    if not os.environ.get('FLRNMNB_DEBUG', None):

        from progress.bar import ChargingBar

    try:
        mpath = get_mpath()

        chain_pubkey = {}

        print('---> get address from hw wallet : %s' % max_gab)
        if not os.environ.get('FLRNMNB_DEBUG', None):
            chargingBar = ChargingBar('---> processing', max=max_gab)

        for i in range(max_gab):
            if not os.environ.get('FLRNMNB_DEBUG', None):
                chargingBar.next()
            child_path = '%s%s' % (mpath + '/', str(i))

            if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
                nodedata = client.getWalletPublicKey(child_path)
                publicnode = compress_public_key(nodedata.get('publicKey')).hex()
                address   = (nodedata.get('address')).decode("utf-8")

            else:
                address = client.get_address(
                    coin_name, client.expand_path(child_path))
                publicnode = client.get_public_node(
                    client.expand_path(child_path)).node.public_key.hex()

            chain_pubkey[address] = {"spath": i, "addrpubkey": publicnode}
            printdbg('get_chain_pubkey : %s %s %s' %
                     (child_path, address, publicnode[-10:]))

            if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
                time.sleep(1)

        if not os.environ.get('FLRNMNB_DEBUG', None):
            chargingBar.next()
            chargingBar.finish()

        printdbg(
            'get_chain_pubkey : chain_pubkey.keys() : %s' %
            chain_pubkey.keys())

        return chain_pubkey

    except AssertionError:
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)  # Fixed format
        tb_info = traceback.extract_tb(tb)
        filename, line, func, text = tb_info[-1]

        err_msg = 'An error occurred on line {} in statement {}'.format(
            line, text)
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


def get_mpath(default_account=False):
    # return without address_index

    #  Florijncoin  : 44'/5'/account'/0/0
    #  tFlorijncoin : 44'/1'/account'/0/0

    printdbg('get_mpath : default_account : %s' % bool(default_account))
    printdbg('get_mpath : network mainnet : %s' % MAINNET)

    if default_account:
        return "44'/5'/0'/0" if MAINNET else "44'/1'/0'/0"

    else:
        return "44'/5'/" + \
            str(account_no) + "'/0" if MAINNET else "44'/1'/" + str(account_no) + "'/0"


def list_coins(client):
    return [coin.coin_name for coin in client.features.coins]


def check_hw_wallet():
    printdbg('checking hw wallet')
    #client = None

    client = None
    signing = False

    if TYPE_HW_WALLET.lower().startswith("keepkey"):
        from keepkeylib.client import KeepKeyClient
        from keepkeylib.transport_hid import HidTransport
        import keepkeylib.ckd_public as bip32

        try:
            devices = HidTransport.enumerate()

        except Exception as e:
            err_msg = str(e.args)
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if len(devices) == 0:
            print('===> No HW Wallet found')
            signing = False

        else:

            try:
                print('===> keepkey HW Wallet found')
                transport = HidTransport(devices[0])
                client = KeepKeyClient(transport)
                signing = True

            except Exception as e:
                err_msg = str(e.args)
                print_err_exit(
                    get_caller_name(),
                    get_function_name(),
                    err_msg)

    elif TYPE_HW_WALLET.lower().startswith("trezor"):
        from trezorlib.client import TrezorClient
        from trezorlib.transport_hid import HidTransport
        import trezorlib.ckd_public as bip32

        try:
            devices = HidTransport.enumerate()

        except Exception as e:
            err_msg = str(e.args)
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if len(devices) == 0:
            print('===> No HW Wallet found')
            signing = False

        else:
            try:
                print('===> trezor HW Wallet found')
                transport = HidTransport(devices[0])
                client = TrezorClient(transport)
                signing = True

            except Exception as e:
                err_msg = str(e.args)
                print_err_exit(
                    get_caller_name(),
                    get_function_name(),
                    err_msg)


    elif TYPE_HW_WALLET.lower().startswith("ledgernanos"):
        #from btchip.btchip import *
        #from btchip.btchipUtils import *

        try:
            devices = getDongle(False)

        except Exception as e:
            err_msg = str(e.args)
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if not devices:
            print('===> No HW Wallet found')
            signing = False

        else:
            try:
                print('===> Ledger nano s HW Wallet found')
                client = btchip(devices)
                signing = True

            except Exception as e:
                err_msg = str(e.args)
                print_err_exit(
                    get_caller_name(),
                    get_function_name(),
                    err_msg)


    if client is not None:

        if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
            pass

        else:
            try:
                wallet_supported_coins = list_coins(client)
    
            except Exception as e:
                err_msg = str(e.args)
                print_err_exit(
                    get_caller_name(),
                    get_function_name(),
                    err_msg)
    
            if coin_name not in wallet_supported_coins:
                err_msg = 'only following coins supported by wallet\n\t' + \
                    str(wallet_supported_coins)
                print_err_exit(
                    get_caller_name(),
                    get_function_name(),
                    err_msg)

    else:
        err_msg = "Can't run florijncoinmnb without hw wallet"
        print_err_exit(
            get_caller_name(),
            get_function_name(),
            err_msg)

    if TYPE_HW_WALLET.lower().startswith("ledgernanos"):
        mpath = get_mpath()

        return client, signing, mpath

    else:
        try:
            mpath = get_mpath()
            bip32_path = client.expand_path(mpath)
            xpub = bip32.serialize(
                client.get_public_node(bip32_path).node,
                (0x0488B21E if MAINNET else 0x043587CF))
    
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

    printdbg('check_hw_wallet : signing : %s' % signing)
    printdbg('check_hw_wallet : xpub[:7] : %s' % xpub[:7])
    printdbg('check_hw_wallet : xpub[-7:] : %s' % xpub[-7:])
    printdbg('check_hw_wallet : mpath : %s' % mpath)

    return client, signing, bip32, mpath, xpub
