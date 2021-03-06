# Author: Sarah Wassermann <sarah.wassermann@student.ulg.ac.be>

def parseProbeListOutput(output, verbose, mapp=None):
    """
    :param output: the output of probe-list.pl [args]
    :return: a string in the format 'probe1,probe2,...,probeN' probeN corresponding
             to the probe_ID
    """
    if not output:
        return ''
    else:
        output = output.decode("utf-8") 
        #print("output: " + output)
        resultLines = output.rsplit('\n')
        probes = list()
        try:
            ASMap = open('DisNETPerf/logs/ID_To_AS.log', 'a')
        except IOError:
            if verbose:
                print("error: Could not open file 'DisNETPerf/logs/ID_To_AS.log'\n")
            return None

        for line in resultLines:
            if not line:
                continue
            elements = line.split('\t')
            probes.append(elements[0])
            ASMap.write(elements[0] + '\t' + elements[3] + '\n')
            if mapp != None: #save AS to dict
                mapp[elements[0]] = elements[3]
        ASMap.close()
    return [probes[i:i + 500] for i in range(0, len(probes), 500)]

def findASNeighbourhood(ASN, verbose):
    """
    Finds neighbours of AS with ASN <ASN> according to CAIDA's relationship dataset.
    :param ASN: the ASN of the AS you want to find the neighbours for
    :param verbose: if true, an error message in case of an internal problem will be displayed, otherwise not
    :return: a list of the detected neighbours
    """
    try:
        file = open('DisNETPerf/lib/ASNeighbours.txt', 'r')
    except:
        if verbose:
            print("error: Could not open file 'DisNETPerf/lib/ASNeighbours.txt'\n")
        return None

    neighbours = set()
    for line in file:
        l = line.rstrip('\r\n')
        if not l or l.isspace() or l.startswith('#'):
            continue
        else:
            l = l.split('|')
            if ASN in l:
                if l[0] == ASN:
                    neighbours.add(l[1])
                else:
                    neighbours.add(l[0])
    file.close()
    return list(neighbours)
