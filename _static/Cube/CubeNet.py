# -*- coding: utf-8 -*-
"""

 This is based on scripts/walkSkims/gothroughme/cube/cubeNet.py
 But I left the original in place because of the dependency on the network object, which I didn't want
 to bring in here (as the functionality we want is more simplistic).
  -Lisa 2012.03.12

"""
import copy, os, re, time
from socket import gethostname, getfqdn

CUBE_COMPUTER = "vanness"
CUBE_SUCCESS = re.compile("\s*(VOYAGER)\s+(ReturnCode)\s*=\s*([01])\s+")

def getCubeHostnames():
    """
    Cube hostnames in Y:\COMMPATH\HostnamesWithCube.txt
    """
    hostnames = []
    fqdn = getfqdn().lower() # fully qualified domain name

    # at mtc, assume cube license is available
    if fqdn.endswith("mtc.ca.gov"): return [ gethostname().lower() ]
    env = copy.copy(os.environ)
    f = open(env['CUBE_HOST_FILE'])
    for line in f:
        if line[0] == "#": continue
        hostnames.append(line.split()[0])  # use the first token of non-comment lines
    f.close()
    return hostnames
    
def export_cubenet_to_csvs(file, extra_link_vars=[], extra_node_vars=[], 
                              links_csv=None, nodes_csv=None):
    """
    Export cube network to csv files
    If *links_csv* and *nodes_csv* filenames passed, will use those.
    Otherwise, will output into %TEMP%\link.csv and %TEMP%\node.csv
    
    options:
        extra_link_vars, extra_node_vars: list extra variables to export
    """
    import subprocess
    script   = os.path.join(os.path.dirname(os.path.abspath(__file__)),"exportHwyfromPy.s")
    
    #set environment variables
    env = copy.copy(os.environ)
    
    env['CUBENET']=file 
    env['PATH'] = os.environ['PATH'] # inherit this
    
    if links_csv:
        env["CUBELINK_CSV"] = links_csv
    else:
        env["CUBELINK_CSV"] = os.path.join(os.environ["TEMP"], "link.csv")
    if nodes_csv:
        env["CUBENODE_CSV"] = nodes_csv
    else:
        env["CUBENODE_CSV"] = os.path.join(os.environ["TEMP"], "node.csv")
        
    if len(extra_link_vars)>0:
        extra_vars_str=","
        extra_vars_str+=extra_vars_str.join(extra_link_vars)
        env['XTRALINKVAR']=extra_vars_str
    else:
        env['XTRALINKVAR']=''

    if len(extra_node_vars)>0:
        extra_vars_str=","
        extra_vars_str+=extra_vars_str.join(extra_node_vars)
        env['XTRANODEVAR']=extra_vars_str
    else:
        env['XTRANODEVAR']=' '    
    
    #run it on CUBE_COMPUTER; cube is installed there
    filedir = os.path.dirname(os.path.abspath(file))
    hostname = gethostname().lower()

    # retry in case of a license error
    NUM_RETRIES = 5
    for attempt in range(1,NUM_RETRIES+1):

        cube_stdout = []
        license_error = False
        if hostname not in getCubeHostnames():
            if links_csv == None or nodes_csv == None:
                print("export_cubenet_to_csvs requires a links_csv and nodes_csv output file if dispatching to {} (temp won't work)".format(CUBE_COMPUTER))
                sys.exit(2)
             
            env["MACHINES"] = CUBE_COMPUTER

            cmd = f'runtpp "{script}"'
            proc = subprocess.Popen( cmd, cwd = filedir, stdout=subprocess.PIPE, stderr=subprocess.PIPE )#, env=env)
            for line in proc.stdout:
                if type(line)==bytes: line = line.decode()  # convert to string, not byetes
                line = line.strip('\r\n')
                print("stdout: {}".format(line))
                cube_stdout.append(line)
                if line=="RUNTPP: Licensing error": license_error = True
        else:
            cmd = 'runtpp.exe ' + script 
            print(cmd)
            print(filedir)
        
            proc = subprocess.Popen( cmd, cwd = filedir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            for line in proc.stdout:
                if type(line)==bytes: line = line.decode()  # convert to string, not byetes
                line = line.strip('\r\n')
                print("stdout: {}".format(line))
                cube_stdout.append(line)
                if line=="RUNTPP: Licensing error": license_error = True

        print("EXPORTING CUBE NETWORK: {}".format(env['CUBENET']))
        print("...adding variables {}, {}:".format(env['XTRALINKVAR'], env['XTRANODEVAR']))
        print("...running script: \n      {}".format(script))

        # retry on license error
        if license_error:
            print("Received license error")
            if attempt == NUM_RETRIES:
                print("Out of retry attempts")
                sys.exit(2)

            # retry
            print("Retrying {} ...".format(attempt))
            time.sleep(1)
            continue
     
        retStderr = []
        for line in proc.stderr:
            if type(line)==bytes: line = line.decode()  # convert to string, not byetes
            line = line.strip('\r\n')
            print("stderr: {}".format(line))
        retcode  = proc.wait()

        if (retcode != 0) and len(cube_stdout)>0:
            # retcode may be wrong -- check last stdout
            print("checking cube_stdout[-1]: {}".format(cube_stdout[-1]))
            # print("match: {}".format(re.match(retcode,cube_stdout[-1])))
            if re.match(CUBE_SUCCESS,cube_stdout[-1]):
                print("Overriding cuberet {} with 0 due to last cubeStdout line".format(retcode))
                retcode = 0

        # success -- stop looping
        if retcode == 0: break

        # not license error -- break
        if retcode != 0: raise


    print("Received {} from [{}]".format(retcode, cmd))
    print("Exported network to: {}, {}".format(env["CUBELINK_CSV"], env["CUBENODE_CSV"]))

    
def import_cube_nodes_links_from_csvs(cubeNetFile,
                                          extra_link_vars=[], extra_node_vars=[],
                                          links_csv=None, nodes_csv=None,
                                          exportIfExists=True):
    """
    Imports cube network from network file and returns (nodes_dict, links_dict).
    
    Nodes_dict maps node numbers to [X, Y, vars given by *extra_node_vars*]
    
    Links_dict maps (a,b) to [DISTANCE, *extra_link_vars*]
    """

    if not links_csv:
        links_csv=os.path.join(os.environ['TEMP'],"node.csv")
    if not nodes_csv:
        nodes_csv=os.path.join(os.environ['TEMP'],"link.csv")

    # don't export if
    if (not exportIfExists and links_csv and nodes_csv and 
        os.path.exists(links_csv) and os.path.exists(nodes_csv)):
        pass # don't need to do anything
    else:
        export_cubenet_to_csvs(cubeNetFile,extra_link_vars, extra_node_vars, links_csv=links_csv, nodes_csv=nodes_csv)

    
    # Open node file and read nodes
    nodes_dict = {}    
    F=open(nodes_csv,mode='r')
    for rec in F:
        r=rec.strip().split(',')
        n=int(r[0])
        x=float(r[1])
        y=float(r[2])
        node_array = [x,y]
        node_array.extend(r[3:])
        
        nodes_dict[n] = node_array
    F.close()
    
    # Open link file and read links
    links_dict = {}
    F=open(links_csv,mode='r')
    for rec in F:
        r=rec.strip().split(',')
        
        #add standard fields
        a=int(r[0])
        b=int(r[1])
        dist=float(r[2])

        #add additional fields        
        link_array = [dist]
        link_array.extend(r[3:])
        
        links_dict[(a,b)] = link_array
    F.close()

    return (nodes_dict, links_dict)


