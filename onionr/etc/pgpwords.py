#!/usr/bin/env python
# -*- coding: utf-8 -*- (because 0xFF, even : "Yucatán")

import os, re, sys, binascii, base64

_words = [
    ["aardvark", "adroitness"],
    ["absurd", "adviser"],
    ["accrue", "aftermath"],
    ["acme", "aggregate"],
    ["adrift", "alkali"],
    ["adult", "almighty"],
    ["afflict", "amulet"],
    ["ahead", "amusement"],
    ["aimless", "antenna"],
    ["Algol", "applicant"],
    ["allow", "Apollo"],
    ["alone", "armistice"],
    ["ammo", "article"],
    ["ancient", "asteroid"],
    ["apple", "Atlantic"],
    ["artist", "atmosphere"],
    ["assume", "autopsy"],
    ["Athens", "Babylon"],
    ["atlas", "backwater"],
    ["Aztec", "barbecue"],
    ["baboon", "belowground"],
    ["backfield", "bifocals"],
    ["backward", "bodyguard"],
    ["banjo", "bookseller"],
    ["beaming", "borderline"],
    ["bedlamp", "bottomless"],
    ["beehive", "Bradbury"],
    ["beeswax", "bravado"],
    ["befriend", "Brazilian"],
    ["Belfast", "breakaway"],
    ["berserk", "Burlington"],
    ["billiard", "businessman"],
    ["bison", "butterfat"],
    ["blackjack", "Camelot"],
    ["blockade", "candidate"],
    ["blowtorch", "cannonball"],
    ["bluebird", "Capricorn"],
    ["bombast", "caravan"],
    ["bookshelf", "caretaker"],
    ["brackish", "celebrate"],
    ["breadline", "cellulose"],
    ["breakup", "certify"],
    ["brickyard", "chambermaid"],
    ["briefcase", "Cherokee"],
    ["Burbank", "Chicago"],
    ["button", "clergyman"],
    ["buzzard", "coherence"],
    ["cement", "combustion"],
    ["chairlift", "commando"],
    ["chatter", "company"],
    ["checkup", "component"],
    ["chisel", "concurrent"],
    ["choking", "confidence"],
    ["chopper", "conformist"],
    ["Christmas", "congregate"],
    ["clamshell", "consensus"],
    ["classic", "consulting"],
    ["classroom", "corporate"],
    ["cleanup", "corrosion"],
    ["clockwork", "councilman"],
    ["cobra", "crossover"],
    ["commence", "crucifix"],
    ["concert", "cumbersome"],
    ["cowbell", "customer"],
    ["crackdown", "Dakota"],
    ["cranky", "decadence"],
    ["crowfoot", "December"],
    ["crucial", "decimal"],
    ["crumpled", "designing"],
    ["crusade", "detector"],
    ["cubic", "detergent"],
    ["dashboard", "determine"],
    ["deadbolt", "dictator"],
    ["deckhand", "dinosaur"],
    ["dogsled", "direction"],
    ["dragnet", "disable"],
    ["drainage", "disbelief"],
    ["dreadful", "disruptive"],
    ["drifter", "distortion"],
    ["dropper", "document"],
    ["drumbeat", "embezzle"],
    ["drunken", "enchanting"],
    ["Dupont", "enrollment"],
    ["dwelling", "enterprise"],
    ["eating", "equation"],
    ["edict", "equipment"],
    ["egghead", "escapade"],
    ["eightball", "Eskimo"],
    ["endorse", "everyday"],
    ["endow", "examine"],
    ["enlist", "existence"],
    ["erase", "exodus"],
    ["escape", "fascinate"],
    ["exceed", "filament"],
    ["eyeglass", "finicky"],
    ["eyetooth", "forever"],
    ["facial", "fortitude"],
    ["fallout", "frequency"],
    ["flagpole", "gadgetry"],
    ["flatfoot", "Galveston"],
    ["flytrap", "getaway"],
    ["fracture", "glossary"],
    ["framework", "gossamer"],
    ["freedom", "graduate"],
    ["frighten", "gravity"],
    ["gazelle", "guitarist"],
    ["Geiger", "hamburger"],
    ["glitter", "Hamilton"],
    ["glucose", "handiwork"],
    ["goggles", "hazardous"],
    ["goldfish", "headwaters"],
    ["gremlin", "hemisphere"],
    ["guidance", "hesitate"],
    ["hamlet", "hideaway"],
    ["highchair", "holiness"],
    ["hockey", "hurricane"],
    ["indoors", "hydraulic"],
    ["indulge", "impartial"],
    ["inverse", "impetus"],
    ["involve", "inception"],
    ["island", "indigo"],
    ["jawbone", "inertia"],
    ["keyboard", "infancy"],
    ["kickoff", "inferno"],
    ["kiwi", "informant"],
    ["klaxon", "insincere"],
    ["locale", "insurgent"],
    ["lockup", "integrate"],
    ["merit", "intention"],
    ["minnow", "inventive"],
    ["miser", "Istanbul"],
    ["Mohawk", "Jamaica"],
    ["mural", "Jupiter"],
    ["music", "leprosy"],
    ["necklace", "letterhead"],
    ["Neptune", "liberty"],
    ["newborn", "maritime"],
    ["nightbird", "matchmaker"],
    ["Oakland", "maverick"],
    ["obtuse", "Medusa"],
    ["offload", "megaton"],
    ["optic", "microscope"],
    ["orca", "microwave"],
    ["payday", "midsummer"],
    ["peachy", "millionaire"],
    ["pheasant", "miracle"],
    ["physique", "misnomer"],
    ["playhouse", "molasses"],
    ["Pluto", "molecule"],
    ["preclude", "Montana"],
    ["prefer", "monument"],
    ["preshrunk", "mosquito"],
    ["printer", "narrative"],
    ["prowler", "nebula"],
    ["pupil", "newsletter"],
    ["puppy", "Norwegian"],
    ["python", "October"],
    ["quadrant", "Ohio"],
    ["quiver", "onlooker"],
    ["quota", "opulent"],
    ["ragtime", "Orlando"],
    ["ratchet", "outfielder"],
    ["rebirth", "Pacific"],
    ["reform", "pandemic"],
    ["regain", "Pandora"],
    ["reindeer", "paperweight"],
    ["rematch", "paragon"],
    ["repay", "paragraph"],
    ["retouch", "paramount"],
    ["revenge", "passenger"],
    ["reward", "pedigree"],
    ["rhythm", "Pegasus"],
    ["ribcage", "penetrate"],
    ["ringbolt", "perceptive"],
    ["robust", "performance"],
    ["rocker", "pharmacy"],
    ["ruffled", "phonetic"],
    ["sailboat", "photograph"],
    ["sawdust", "pioneer"],
    ["scallion", "pocketful"],
    ["scenic", "politeness"],
    ["scorecard", "positive"],
    ["Scotland", "potato"],
    ["seabird", "processor"],
    ["select", "provincial"],
    ["sentence", "proximate"],
    ["shadow", "puberty"],
    ["shamrock", "publisher"],
    ["showgirl", "pyramid"],
    ["skullcap", "quantity"],
    ["skydive", "racketeer"],
    ["slingshot", "rebellion"],
    ["slowdown", "recipe"],
    ["snapline", "recover"],
    ["snapshot", "repellent"],
    ["snowcap", "replica"],
    ["snowslide", "reproduce"],
    ["solo", "resistor"],
    ["southward", "responsive"],
    ["soybean", "retraction"],
    ["spaniel", "retrieval"],
    ["spearhead", "retrospect"],
    ["spellbind", "revenue"],
    ["spheroid", "revival"],
    ["spigot", "revolver"],
    ["spindle", "sandalwood"],
    ["spyglass", "sardonic"],
    ["stagehand", "Saturday"],
    ["stagnate", "savagery"],
    ["stairway", "scavenger"],
    ["standard", "sensation"],
    ["stapler", "sociable"],
    ["steamship", "souvenir"],
    ["sterling", "specialist"],
    ["stockman", "speculate"],
    ["stopwatch", "stethoscope"],
    ["stormy", "stupendous"],
    ["sugar", "supportive"],
    ["surmount", "surrender"],
    ["suspense", "suspicious"],
    ["sweatband", "sympathy"],
    ["swelter", "tambourine"],
    ["tactics", "telephone"],
    ["talon", "therapist"],
    ["tapeworm", "tobacco"],
    ["tempest", "tolerance"],
    ["tiger", "tomorrow"],
    ["tissue", "torpedo"],
    ["tonic", "tradition"],
    ["topmost", "travesty"],
    ["tracker", "trombonist"],
    ["transit", "truncated"],
    ["trauma", "typewriter"],
    ["treadmill", "ultimate"],
    ["Trojan", "undaunted"],
    ["trouble", "underfoot"],
    ["tumor", "unicorn"],
    ["tunnel", "unify"],
    ["tycoon", "universe"],
    ["uncut", "unravel"],
    ["unearth", "upcoming"],
    ["unwind", "vacancy"],
    ["uproot", "vagabond"],
    ["upset", "vertigo"],
    ["upshot", "Virginia"],
    ["vapor", "visitor"],
    ["village", "vocalist"],
    ["virus", "voyager"],
    ["Vulcan", "warranty"],
    ["waffle", "Waterloo"],
    ["wallet", "whimsical"],
    ["watchword", "Wichita"],
    ["wayside", "Wilmington"],
    ["willow", "Wyoming"],
    ["woodlark", "yesteryear"],
    ["Zulu", "Yucatán"]]

hexre = re.compile("[a-fA-F0-9]+")

def wordify(seq):
    seq = filter(lambda x: x not in (' ', '\n', '\t'), seq)
    seq = "".join(seq) # Python3 compatibility

    if not hexre.match(seq):
        raise Exception("Input is not a valid hexadecimal value.")

    if len(seq) % 2:
        raise Exception("Input contains an odd number of bytes.")

    ret = []
    for i in range(0, len(seq), 2):
        ret.append(_words[int(seq[i:i+2], 16)][(i//2)%2])
    return ret

def hexify(seq, delim=' '):
    ret = b''
    sentence = seq
    try:
        sentence = seq.split(delim)
    except AttributeError:
        pass
    count = 0
    for word in sentence:
        count = 0
        for wordPair in _words:
            if word in wordPair:
                ret += bytes([(count)])
            count += 1
    return binascii.hexlify(ret)

def usage():
    print("Usage:")
    print("  {0} [fingerprint...]".format(os.path.basename(sys.argv[0])))
    print("")
    print("If called with multiple arguments, they will be concatenated")
    print("and treated as a single fingerprint.")
    print("")
    print("If called with no arguments, input is read from stdin,")
    print("and each line is treated as a single fingerprint.  In this")
    print("mode, invalid values are silently ignored.")
    exit(1)

if __name__ == '__main__':
    if 1 == len(sys.argv):
        fps = sys.stdin.readlines()
    else:
        fps = [" ".join(sys.argv[1:])]
    for fp in fps:
        try:
            words = wordify(fp)
            print("\n{0}: ".format(fp.strip()))
            sys.stdout.write("\t")
            for i in range(0, len(words)):
                sys.stdout.write(words[i] + " ")
                if (not (i+1) % 4) and  not i == len(words)-1:
                    sys.stdout.write("\n\t")
            print("")

        except Exception as e:
            if len(fps) == 1:
                print (e)
                usage()

    print("")

