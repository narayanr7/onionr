'''
    Onionr - Private P2P Communication

    Create blocks with the client api server
'''
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
from flask import Blueprint, Response, abort
import core, onionrblockapi
from httpapi import apiutils
from onionrutils import stringvalidators

c = core.Core()

client_get_block = apiutils.GetBlockData(c)

client_get_blocks = Blueprint('miscclient', __name__)

@client_get_blocks.route('/getblocksbytype/<name>')
def getBlocksByType(name):
    blocks = c.getBlocksByType(name)
    return Response(','.join(blocks))

@client_get_blocks.route('/getblockbody/<name>')
def getBlockBodyData(name):
    resp = ''
    if stringvalidators.validate_hash(name):
        try:
            resp = onionrblockapi.Block(name, decrypt=True, core=c).bcontent
        except TypeError:
            pass
    else:
        abort(404)
    return Response(resp)

@client_get_blocks.route('/getblockdata/<name>')
def getData(name):
    resp = ""
    if stringvalidators.validate_hash(name):
        if name in c.getBlockList():
            try:
                resp = client_get_block.get_block_data(name, decrypt=True)
            except ValueError:
                pass
        else:
            abort(404)
    else:
        abort(404)
    return Response(resp)

@client_get_blocks.route('/getblockheader/<name>')
def getBlockHeader(name):
    resp = client_get_block.get_block_data(name, decrypt=True, headerOnly=True)
    return Response(resp)