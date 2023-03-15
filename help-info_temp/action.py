from main import BrocadeCmd
# Alias aufbau
# alias: t_dehze01_tpl013_d7
#                50:00:e1:11:c6:81:d0:ca
# alias: t_dehze01_tpl013_dx
#                50:00:e1:11:c6:81:d0:ca; 50:00:e1:11:c6:81:d0:b6;
#                50:00:e1:11:c6:81:d0:8e; 50:00:e1:11:c6:81:d0:7a

_alias_db = {}

def _alias_split(cache):
    """ helper function. splits the alias lines. add data to _alias_db"""
    del(cache[0]) # delete 'alias:'
    name = cache[0]
    del(cache[0]) # delete 'name'
    for wwn in cache:
        f = wwn.replace(';', '')
        _alias_db[f] = name

def command(cmd=None, outputfile=None):


    def writefile(line):
        if outputfile:
            outputfile.write(line)


    SKIPPING = True # Alle Zeilen die nicht zum Aliaseintrag gehören werden übersprungen.
    cache = [] # Temporärer Zwischenspeicher, in dem alle alias zwischengespeichert werden

    # Switchinfo abfragen.
    switch = BrocadeCmd()
    switch.open(switch="dehze01-ssw100", ip="10.4.248.11", user="admin", password="Passw0rd", logfile="brocade.log")
    lines = switch.run_cmd("zoneshow")
    switch.close()

    for line in lines:
        uline = line.strip()
        words = line.split()

        if SKIPPING: # Skip all lines without any alias information.
            if words[0] == 'alias:':
                SKIPPING = False
            else:
                continue

        if not SKIPPING: # found alias entry
            if len(words) == 0: # a blank line finishes the alias information

                writefile(' '.join(cache) + '\n')
                _alias_split(cache)
                return 0    # Succesfully job

            elif words[0] == 'alias:' :
                if cache != []: # Save the last alias information
                    writefile(' '.join(cache)+'\n')
                    _alias_split(cache)
                    cache = []
                cache.extend(words)
            elif line.startswith("   ") or line.startswith("	"):  # row content wwns for the alias
                cache.extend(words)
            else:
                print ('should not be here...', uline) # Somthing was going wrong
                return -1


if __name__ == "__main__":
    outfile = open('aliases', 'w')
    if command(outputfile=outfile) == 0:
        print(_alias_db)
        for wwn, name in _alias_db:
            print("%s, %s" % (wwn, name))