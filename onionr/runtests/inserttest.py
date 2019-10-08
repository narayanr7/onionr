import os

import onionrblocks
import logger
import coredb

def insert_bin_test(testmanager):
    data = os.urandom(32)
    b_hash = onionrblocks.insert(data, )
    
    if not b_hash in coredb.blockmetadb.get_block_list():
        logger.error(str(b_hash) + 'is not in bl')
        raise ValueError