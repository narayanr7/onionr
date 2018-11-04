'''
    Onionr - P2P Anonymous Storage Network

    This default plugin handles private messages in an email like fashion
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

# Imports some useful libraries
import logger, config, threading, time, readline, datetime
from onionrblockapi import Block
import onionrexceptions, onionrusers
import locale, sys, os

locale.setlocale(locale.LC_ALL, '')

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import sentboxdb # import after path insert

plugin_name = 'pms'
PLUGIN_VERSION = '0.0.1'

def draw_border(text):
    #https://stackoverflow.com/a/20757491
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)


class MailStrings:
    def __init__(self, mailInstance):
        self.mailInstance = mailInstance

        self.programTag = 'OnionrMail v%s' % (PLUGIN_VERSION)
        choices = ['view inbox', 'view sentbox', 'send message', 'quit']
        self.mainMenuChoices = choices
        self.mainMenu = '''\n
-----------------
1. %s
2. %s
3. %s
4. %s''' % (choices[0], choices[1], choices[2], choices[3])

class OnionrMail:
    def __init__(self, pluginapi):
        self.myCore = pluginapi.get_core()
        self.strings = MailStrings(self)

        self.sentboxTools = sentboxdb.SentBox(self.myCore)
        self.sentboxList = []
        self.sentMessages = {}
        return
    
    def inbox(self):
        blockCount = 0
        pmBlockMap = {}
        pmBlocks = {}
        logger.info('Decrypting messages...')
        choice = ''
        displayList = []

        # this could use a lot of memory if someone has recieved a lot of messages
        for blockHash in self.myCore.getBlocksByType('pm'):
            pmBlocks[blockHash] = Block(blockHash, core=self.myCore)
            pmBlocks[blockHash].decrypt()

        while choice not in ('-q', 'q', 'quit'):
            blockCount = 0
            for blockHash in pmBlocks:
                if not pmBlocks[blockHash].decrypted:
                    continue
                blockCount += 1
                pmBlockMap[blockCount] = blockHash
                
                block = pmBlocks[blockHash]
                senderKey = block.signer
                try:
                    senderKey = senderKey.decode()
                except AttributeError:
                    pass
                senderDisplay = onionrusers.OnionrUser(self.myCore, senderKey).getName()
                if senderDisplay == 'anonymous':
                    senderDisplay = senderKey

                blockDate = pmBlocks[blockHash].getDate().strftime("%m/%d %H:%M")
                displayList.append('%s. %s - %s: %s' % (blockCount, blockDate, senderDisplay[:12], blockHash))
            #displayList.reverse()
            for i in displayList:
                print(i)
            try:
                choice = logger.readline('Enter a block number, -r to refresh, or -q to stop: ').strip().lower()
            except (EOFError, KeyboardInterrupt):
                choice = '-q'

            if choice in ('-q', 'q', 'quit'):
                continue

            if choice in ('-r', 'r', 'refresh'):
                # dirty hack
                self.inbox()
                return

            try:
                choice = int(choice)
            except ValueError:
                pass
            else:
                try:
                    pmBlockMap[choice]
                    readBlock = pmBlocks[pmBlockMap[choice]]
                except KeyError:
                    pass
                else:
                    cancel = ''
                    readBlock.verifySig()
                    print('Message recieved from %s' % (self.myCore._utils.bytesToStr(readBlock.signer,)))
                    print('Valid signature:', readBlock.validSig)
                    if not readBlock.validSig:
                        logger.warn('This message has an INVALID signature. ANYONE could have sent this message.')
                        cancel = logger.readline('Press enter to continue to message, or -q to not open the message (recommended).')
                    if cancel != '-q':
                        print(draw_border(self.myCore._utils.escapeAnsi(readBlock.bcontent.decode().strip())))
        return
    
    def sentbox(self):
        '''
            Display sent mail messages
        '''
        entering = True
        while entering:
            self.getSentList()
            print('Enter block number or -q to return')
            try:
                choice = input('>')
            except (EOFError, KeyboardInterrupt) as e:
                entering = False
            else:
                if choice == '-q':
                    entering = False
                else:
                    try:
                        self.sentboxList[int(choice) - 1]
                    except IndexError:
                        print('Invalid block')
                    else:
                        logger.info('Sent to: ' + self.sentMessages[self.sentboxList[int(choice) - 1]][1])
                        # Print ansi escaped sent message
                        print(self.myCore._utils.escapeAnsi(self.sentMessages[self.sentboxList[int(choice) - 1]][0]))
                        input('Press enter to continue...')

        return
    
    def getSentList(self):
        count = 1
        for i in self.sentboxTools.listSent():
            self.sentboxList.append(i['hash'])
            self.sentMessages[i['hash']] = (i['message'], i['peer'])
            print('%s. %s - %s - %s' % (count, i['hash'], i['peer'][:12], i['date']))
            count += 1

    def draftMessage(self):
        message = ''
        newLine = ''
        recip = ''
        entering = True

        while entering:
            try:
                recip = logger.readline('Enter peer address, or q to stop:').strip()
                if recip in ('-q', 'q'):
                    raise EOFError
                if not self.myCore._utils.validatePubKey(recip):
                    raise onionrexceptions.InvalidPubkey('Must be a valid ed25519 base32 encoded public key')
            except onionrexceptions.InvalidPubkey:
                logger.warn('Invalid public key')
            except (KeyboardInterrupt, EOFError):
                entering = False
            else:
                break
        else:
            # if -q or ctrl-c/d, exit function here, otherwise we successfully got the public key
            return

        print('Enter your message, stop by entering -q on a new line.')
        while newLine != '-q':
            try:
                newLine = input()
            except (KeyboardInterrupt, EOFError):
                pass
            if newLine == '-q':
                continue
            newLine += '\n'
            message += newLine

        print('Inserting encrypted message as Onionr block....')

        blockID = self.myCore.insertBlock(message, header='pm', encryptType='asym', asymPeer=recip, sign=True)
        self.sentboxTools.addToSent(blockID, recip, message)
    def menu(self):
        choice = ''
        while True:

            print(self.strings.programTag + '\n\nOur ID: ' + self.myCore._crypto.pubKey + self.strings.mainMenu.title()) # print out main menu

            try:
                choice = logger.readline('Enter 1-%s:\n' % (len(self.strings.mainMenuChoices))).lower().strip()
            except (KeyboardInterrupt, EOFError):
                choice = '5'

            if choice in (self.strings.mainMenuChoices[0], '1'):
                self.inbox()
            elif choice in (self.strings.mainMenuChoices[1], '2'):
                self.sentbox()
            elif choice in (self.strings.mainMenuChoices[2], '3'):
                self.draftMessage()
            elif choice in (self.strings.mainMenuChoices[3], '4'):
                logger.info('Goodbye.')
                break
            elif choice == '':
                pass
            else:
                logger.warn('Invalid choice.')
        return


def on_init(api, data = None):
    '''
        This event is called after Onionr is initialized, but before the command
        inputted is executed. Could be called when daemon is starting or when
        just the client is running.
    '''

    pluginapi = api
    mail = OnionrMail(pluginapi)
    api.commands.register(['mail'], mail.menu)
    api.commands.register_help('mail', 'Interact with OnionrMail')
    return