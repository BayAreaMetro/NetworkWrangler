import copy, os, pathlib, re, shutil, string, subprocess, sys, tempfile
from .Logger import WranglerLogger
from .NetworkException import NetworkException
from .Regexes import git_commit_pattern

__all__ = ['Network']

class Network(object):

    MODEL_TYPE_CHAMP        = "CHAMP"           # SFCTA travel model
    MODEL_TYPE_TM1          = "TravelModelOne"  # MTC/ABAG Travel Model One
    MODEL_TYPE_TM2          = "TravelModelTwo"  # MTC/ABAG Travel Model Two

    WRANGLER_VERSION        = 2.0
    NETWORK_BASE_DIR        = r"Y:\networks"
    NETWORK_PROJECT_SUBDIR	= ""
    NETWORK_PLAN_SUBDIR     = ""
    NETWORK_SEED_SUBDIR     = ""
    # static variable
    allNetworks = {}

    def __init__(self, modelType, modelVersion, tempdir=None, networkBaseDir=None, networkProjectSubdir=None,
                 networkSeedSubdir=None, networkPlanSubdir=None, networkName=None):
        """
        *modelType* should be MODEL_TYPE_CHAMP, MODEL_TYPE_TM1, or MODEL_TYPE_TM2
        *modelVersion* should be numeric and is used for compatibility checks.
        *tempdir* is where projects will be git cloned

        Currently this should be 4.3 or newer for CHAMP.
        Pass *networkName* to be added to the Networks dictionary
        """
        if modelType not in [Network.MODEL_TYPE_CHAMP, Network.MODEL_TYPE_TM1, Network.MODEL_TYPE_TM2]:
            raise NetworkException("Do not understand modelType {}".format(modelType))
        if type(modelVersion) != type(0.0):
            raise NetworkException("Do not understand modelVersion {}".format(modelVersion))

        self.modelType = modelType
        self.modelVersion = modelVersion
        self.wranglerVersion = self.WRANGLER_VERSION
        self.appliedProjects = {}
        if tempdir and tempdir not in sys.path: sys.path.insert(0,tempdir)
        if networkBaseDir: Network.NETWORK_BASE_DIR = networkBaseDir
        if networkProjectSubdir: Network.NETWORK_PROJECT_SUBDIR = networkProjectSubdir
        if networkSeedSubdir: Network.NETWORK_SEED_SUBDIR = networkSeedSubdir
        if networkPlanSubdir: Network.NETWORK_PLAN_SUBDIR = networkPlanSubdir
        if networkName: Network.allNetworks[networkName] = self

    def _runAndLog(self, cmd, run_dir=".", logStdoutAndStderr=False, env=None):
        """
        Runs the given command in the given *run_dir*.  Returns a triple:
         (return code, stdout, stderr)
        where stdout and stderr are lists of strings.
        """
        myenv = None
        retcode = None
        retStdout = []
        retStderr = []
        if env:
            myenv = copy.deepcopy(os.environ)
            myenv.update(env)
            # WranglerLogger.debug("Using environment {}".format(myenv))

        try:
            proc = subprocess.Popen( cmd, cwd = run_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=myenv )

            stdout, stderr = proc.communicate()

            for line in stdout.decode().splitlines():
                if len(line) == 0: continue
                if logStdoutAndStderr: WranglerLogger.debug("stdout: " + line)
                retStdout.append(line)

            for line in stderr.decode().splitlines():
                if len(line) == 0: continue
                if logStdoutAndStderr: WranglerLogger.debug("stderr: " + line)
                retStderr.append(line)

            retcode = proc.returncode
            WranglerLogger.debug(f"Received {retcode} from [{cmd}] run in [{run_dir}]")
            # WranglerLogger.debug(f"retStdout: {retStdout}")
            # WranglerLogger.debug(f"retStderr: {retStderr}")
        
        except Exception as inst:
            WranglerLogger.error('Exception caught')
            WranglerLogger.error(type(inst))    # the exception instance
            WranglerLogger.error(inst.args)     # arguments stored in .args
            WranglerLogger.error(inst)          # __str__ allows args to be printed directly,
        return (retcode, retStdout, retStderr)

    def getReqs(self, networkdir, projectsubdir=None, tag=None, projtype=None, tempdir=None):
        """
        Checks project for pre-requisites, co-requisites, and conflicts

        See :py:meth:`Wrangler.Network.applyProject` for argument details.
        """
        (parentdir, networkdir, gitdir, projectsubdir) = self.getClonedProjectArgs(networkdir, projectsubdir, projtype, tempdir)
        prereqs     = self.getAttr('prereqs',  parentdir, networkdir, gitdir, projectsubdir)
        coreqs      = self.getAttr('coreqs',   parentdir, networkdir, gitdir, projectsubdir)
        conflicts   = self.getAttr('conflicts',parentdir, networkdir, gitdir, projectsubdir)
        return (prereqs, coreqs, conflicts)

    def getClonedProjectArgs(self, networkdir, projectsubdir=None, projtype=None, tempdir=None):
        """
        Gets project arguments to clone and apply projects

        See :py:meth:`Wrangler.Network.applyProject` for argument details.
        """
        if tempdir:
            if projtype=='plan':
                joinedBaseDir = os.path.join(Network.NETWORK_BASE_DIR,Network.NETWORK_PLAN_SUBDIR)
                joinedTempDir = os.path.join(tempdir, Network.NETWORK_PLAN_SUBDIR)
            elif projtype=='project':
                joinedBaseDir = os.path.join(Network.NETWORK_BASE_DIR,Network.NETWORK_PROJECT_SUBDIR)
                joinedTempDir = os.path.join(tempdir, Network.NETWORK_PROJECT_SUBDIR)
            elif projtype=='seed':
                joinedBaseDir = os.path.join(Network.NETWORK_BASE_DIR,Network.NETWORK_SEED_SUBDIR)
                joinedTempDir = os.path.join(tempdir, Network.NETWORK_SEED_SUBDIR)
            else:
                joinedBaseDir = Network.NETWORK_BASE_DIR
                joinedTempDir = tempdir
                
            gitdir = os.path.join(joinedTempDir, networkdir)
        else:
            # need if for projtype... and joinedTempDir
            tempdir = tempfile.mkdtemp(prefix="Wrangler_tmp_", dir=".")
            joinedTempDir = tempdir
            WranglerLogger.debug("Using tempdir %s" % tempdir)
            gitdir = os.path.join(tempdir, networkdir)

        try:
            commitstr = self.getCommit(gitdir)
        except:
            gitdir = os.path.join(gitdir, projectsubdir)
            commitstr = self.getCommit(gitdir)
            
        return (joinedTempDir, networkdir, gitdir, projectsubdir)
        
    def getAttr(self, attr_name, parentdir, networkdir, gitdir, projectsubdir=None):
        """        
        Returns attribute for this project based on attr_name
        attr_name: the name of the attribute to get
        parentdir: the directory where the project is found
        networkdir: the directory of the project within parentdir
        gitdir: the checkout location of the network project
        projectsubdir: the subdir if it exists, None otherwise
        """
        # WranglerLogger.debug(f"Network.getAttr() with {type(self)=} {attr_name=} {parentdir=} {networkdir=} {gitdir=} {projectsubdir=}")
        if attr_name not in ['year', 'desc', 'modelType', 'modelVersion', 'wranglerVersion', 'prereqs', 'coreqs', 'conflicts', 'networks','primaryNetwork']:
            WranglerLogger.fatal('%s is not a valid attribute type for a network project' % (attr_name))
            return
        
        WranglerLogger.debug(f"getAttr({attr_name=},{parentdir=},{networkdir=},{projectsubdir=})")
        if projectsubdir:
            projectname = projectsubdir
            # sys.path.append(os.path.join(os.getcwd(), parentdir, networkdir))
        else:
            projectname = networkdir
            # this should already be done
            # sys.path.append(os.path.join(os.getcwd(), parentdir))

        try:
            evalstr = "import %s" % projectname
            exec(evalstr)
            WranglerLogger.debug("Successfully imported {}".format(projectname))
        except Exception as e:
            WranglerLogger.fatal("Failed to import {}:".format(projectname))
            WranglerLogger.fatal(e)
            raise ImportError

        # note: I removed the bit here that feel back to the following code when there's an exception:
        #
        # s_projectname = "s"+str(projectname)
        # evalstr = "%s = __import__('%s')" % (s_projectname, projectname)
        # exec(evalstr)
        # WranglerLogger.debug("Successfully imported {}".format(s_projectname))
        #
        # The problem being that it would successfully import a bad project without giving any information
        # about the problem...  For now, a failed import is a hard fail.
        # I'm not sure about the use case with the  __import__ call.

        evalstr = "dir(%s)" % projectname
        projectdir = eval(evalstr)
        # WranglerLogger.debug("projectdir = {}".format(projectdir))

        attr_value = (eval("%s.%s()" % (projectname ,attr_name)))
        # todo: if try champVersion if modelType is CHAMP and modelVersion is sought
        return attr_value

    def getModelVersion(self, parentdir, networkdir, gitdir, projectsubdir=None):
        """
        Returns modelVersion range for this project

        See :py:meth:`Wrangler.Network.applyProject` for argument details.
        """
        return getAttr('modelVersion',parentdir, networkdir,gitdir, projectsubdir)

    def getWranglerVersion(self, parentdir, networkdir, gitdir, projectsubdir=None):
        """        
        Returns wranglerVersion range for this project

        See :py:meth:`Wrangler.Network.applyProject` for argument details.
        """
        return getAttr('wranglerVersion',parentdir, networkdir,gitdir, projectsubdir)
    
    def checkVersion(self, version, parentdir, networkdir, gitdir, projectsubdir=None):
        """
        Verifies that this project is compatible with the modelVersion or wranglerVersion, raises an exception
          if not

        See :py:meth:`Wrangler.Network.applyProject` for argument details.
        """
        if version not in ['modelVersion','wranglerVersion']:
            Wrangler.WranglerLogger.fatal("%s is not a valid version.  Must be 'modelVersion' or 'wranglerVersion'" % str(version))

        versions = {'modelVersion':self.modelVersion, 'wranglerVersion':self.wranglerVersion}

        # if we're checking model version, check model type as well
        if version == "modelVersion":
            # legacy: assume TM1
            project_model_type = Network.MODEL_TYPE_TM1
            try:
                project_model_type = self.getAttr("modelType", parentdir=parentdir, networkdir=networkdir, gitdir=gitdir, projectsubdir=projectsubdir)
                # WranglerLogger.debug("Found project_model_type {}".format(project_model_type))
            except ImportError as ie:
                # consider this fatal
                sys.exit(2)
            except:
                WranglerLogger.debug("Failed to find project model type. Exception: {}".format(sys.exc_info()[0]))
                pass
            if project_model_type != self.modelType:
                raise NetworkException("Project model type ({}) not compatible with this model type {}".format(project_model_type, self.modelType))

        projVersion = self.getAttr(version, parentdir=parentdir, networkdir=networkdir,
                                   gitdir=gitdir, projectsubdir=projectsubdir)
        # WranglerLogger.debug(f"Checking {version} compatibility of project ({projVersion}) with requirement ({versions[version]})")

        minVersion = projVersion[0]
        maxVersion = projVersion[1]
        
        if maxVersion == None:
            if versions[version] >= minVersion:
                return
        else:
            if versions[version] >= minVersion and versions[version] <= maxVersion:
                return

        raise NetworkException("Project version range (%d, %d) not compatible with this %s version %d"
                               % (minVersion,maxVersion,version.replace("Version","").upper(),versions[version]))

    def getNetTypes(self, parentdir, networkdir, projectsubdir=None):
        """
        Gets a list of network types for this project

        See :py:meth:`Wrangler.Network.applyProject` for argument details.
        """
        if projectsubdir:
            projectname = projectsubdir
            sys.path.append(os.path.join(os.getcwd(), parentdir, networkdir))
        else:
            projectname = networkdir
            sys.path.append(os.path.join(os.getcwd(), parentdir))

        try:
            s_projectname = None
            evalstr = "import %s" % projectname
            exec(evalstr)
        except Exception as e:
            #WranglerLogger.debug("error importing module")
            s_projectname = "s"+str(projectname)
            evalstr = "%s = __import__('%s')" % (s_projectname, projectname)
            exec(evalstr)

        evalstr = "dir(%s)" % (projectname if not s_projectname else s_projectname)
        projectdir = eval(evalstr)
        
        # WranglerLogger.debug("projectdir = " + str(projectdir))
        netTypes = (eval("%s.networks()" % (projectname if not s_projectname else s_projectname)))
        return netTypes
        
    def applyProject(self, parentdir, networkdir, gitdir, projectsubdir=None, **kwargs):
        """
        Implemented by subclasses.  Args are as follows:

        * *parentdir* is the directory we're checking stuff out into (e.g. a temp dir)
        * *networkdir* is the name of the dir within ``Y:\\networks``
        * *gitdir* is the git repo; either the same as *networkdir* if the git repo is at
           that level (the typical case), or it's *networkdir\projectsubdir*
        * *projectsubdir* is an optional subdir of *networkdir*; If the ``apply.s`` or ``__init__.py``
          is in a subdir, this is how it's specified
        * *kwargs* are additional keyword args to pass into the apply()
        
        Returns the SHA1 hash ID of the git commit of the project applied
        """
        pass

    def cloneProject(self, networkdir, projectsubdir=None, tag=None, branch='master', projtype=None, tempdir=None, **kwargs):
        """
        * *networkdir* corresponds to the dir relative to ``Y:\\networks``
        * *projectsubdir* is a subdir within that, or None if there's no subdir
        * *tag* is "1.0" or "1-latest", or None for just the latest version
        * *tempdir* is the parent dir to put the git clone dir; pass None for python to just choose
        * *kwargs* are additional args for the apply
        
        Returns the SHA1 hash ID of the git commit of the project applied
        """


        if tempdir:
            if projtype=='plan':
                joinedBaseDir = os.path.join(Network.NETWORK_BASE_DIR,Network.NETWORK_PLAN_SUBDIR)
                joinedTempDir = os.path.join(tempdir, Network.NETWORK_PLAN_SUBDIR)
            elif projtype=='project':
                joinedBaseDir = os.path.join(Network.NETWORK_BASE_DIR,Network.NETWORK_PROJECT_SUBDIR)
                joinedTempDir = os.path.join(tempdir, Network.NETWORK_PROJECT_SUBDIR)
            elif projtype=='seed':
                joinedBaseDir = os.path.join(Network.NETWORK_BASE_DIR,Network.NETWORK_SEED_SUBDIR)
                joinedTempDir = os.path.join(tempdir, Network.NETWORK_SEED_SUBDIR)
            else:
                joinedBaseDir = Network.NETWORK_BASE_DIR
                joinedTempDir = tempdir
                
            gitdir = os.path.join(joinedTempDir, networkdir)
            
            if not os.path.exists(joinedTempDir):
                os.makedirs(joinedTempDir)
                
            # if the tempdir exists and it's already here and the projectsubdir is present, 
            # then we already checked it out
            elif projectsubdir and os.path.exists(os.path.join(joinedTempDir,networkdir,projectsubdir)):
                WranglerLogger.debug("Skipping checkout of %s, %s already exists" % 
                                     (networkdir, os.path.join(joinedTempDir,networkdir,projectsubdir)))

                 # verify we didn't require conflicting tags
                try:
                    commitstr = self.getCommit(gitdir)
                except:
                    gitdir = os.path.join(gitdir, projectsubdir)
                    commitstr = self.getCommit(gitdir)

                tags = self.getTags(gitdir, commitstr)
                if tag and (not tags or tag not in tags):
                    # TODO: just checkout to the new tag
                    raise NetworkException("Conflicting tag requirements - FIXME!")

                # lmz 2025.04.07 - disabling since these aren't useful in practice
                # self.checkVersion(version='modelVersion',parentdir=joinedTempDir, networkdir=networkdir,
                #                   gitdir=gitdir, projectsubdir=projectsubdir)
                # self.checkVersion(version='wranglerVersion',parentdir=joinedTempDir, networkdir=networkdir,
                #                   gitdir=gitdir, projectsubdir=projectsubdir)

                commitstr = self.getCommit(gitdir)
                return commitstr
            
            elif not projectsubdir and os.path.exists(os.path.join(joinedTempDir,networkdir)):
                WranglerLogger.debug("Skipping checkout of %s, %s already exists" % 
                                     (networkdir, os.path.join(joinedTempDir,networkdir)))

                # lmz 2025.04.07 - disabling since these aren't useful in practice
                # self.checkVersion(version='modelVersion',parentdir=joinedTempDir, networkdir=networkdir,
                #                   gitdir=gitdir, projectsubdir=projectsubdir)
                # self.checkVersion(version='wranglerVersion',parentdir=joinedTempDir, networkdir=networkdir,
                #                   gitdir=gitdir, projectsubdir=projectsubdir)

                # TODO: we should verify we didn't require conflicting tags?
                commitstr = self.getCommit(gitdir)
                return commitstr

        else:
            # need if for projtype... and joinedTempDir
            tempdir = tempfile.mkdtemp(prefix="Wrangler_tmp_", dir=".")
            joinedTempDir = tempdir
            WranglerLogger.debug("Using tempdir %s" % tempdir)
            gitdir = os.path.join(tempdir, networkdir)

        WranglerLogger.debug("Checking out networkdir %s into tempdir %s %s" %
                             (networkdir, joinedTempDir,"for "+projectsubdir if projectsubdir else ""))

        # if on windows and joinedBaseDir is on a mapped network drive, it needs to be prefaced with "file://"
        # https://stackoverflow.com/questions/37422428/git-internal-error-refs-remotes-origin-master-is-not-a-valid-packed-reference
        if os.name=='nt':
            import win32file
            (drive,tail) = os.path.splitdrive(joinedBaseDir)
            WranglerLogger.debug("Checking if windows drive [%s] is remote" % drive)
            if win32file.GetDriveType(drive)==win32file.DRIVE_REMOTE:
                joinedBaseDir = "file://" + joinedBaseDir
            WranglerLogger.debug("Using base dir [%s]" % joinedBaseDir)

        if os.path.exists(os.path.join(joinedBaseDir,networkdir,'.git')):
            cmd = r'git clone -b "%s" --quiet "%s" "%s"' % (branch, os.path.join(joinedBaseDir, networkdir), networkdir)
        else:
            cmd = r'git clone -b "%s" --quiet "%s"' % (branch,os.path.join(joinedBaseDir, networkdir))
        
        (retcode, retstdout, retstderr) = self._runAndLog(cmd, joinedTempDir)

        # try to resolve issue related to git cloning from Box
        # see NetworkWrangler: try to fix git issues if git clone fails https://app.asana.com/0/13098083395690/1206943005010445/f
        if (retcode == 128) and ("Box" in joinedBaseDir):
            git_fix_cmd = r'git fsck --full'
            (retcode, retstdout, retstderr) = self._runAndLog(git_fix_cmd, os.path.join(joinedBaseDir, networkdir))

            git_fix_cmd = r'git gc'
            (retcode, retstdout, retstderr) = self._runAndLog(git_fix_cmd, os.path.join(joinedBaseDir, networkdir))

            # and now try again...
            attempt = 2
            while (retcode == 128) and (attempt < 8):
                WranglerLogger.debug(f"attempt {attempt} to git clone")
                (retcode, retstdout, retstderr) = self._runAndLog(cmd, joinedTempDir)
                retcode += 1

        if retcode != 0:
            if not projectsubdir:
                raise NetworkException("Git clone failed; see log file")

            # if there was a subdir involved, try checking if the subdir is the git dir
            gitdir = os.path.join(gitdir, projectsubdir)
            newtempdir = os.path.join(joinedTempDir,networkdir)

            if not os.path.exists(newtempdir):
                os.makedirs(newtempdir)
            cmd = r'git clone -b "%s" --quiet "%s"' % (branch, os.path.join(joinedBaseDir, networkdir, projectsubdir))
            (retcode, retstdout, retstderr) = self._runAndLog(cmd, newtempdir)

        if tag != None:
            cmd = r'git checkout "%s"' % tag
            (retcode, retstdout, retstderr) = self._runAndLog(cmd, gitdir)
            if retcode != 0:
                raise NetworkException("Git checkout failed; see log file")

        # lmz 2025.04.07 - disabling since these aren't useful in practice
        # self.checkVersion(version='modelVersion',parentdir=joinedTempDir, networkdir=networkdir,
        #                   gitdir=gitdir, projectsubdir=projectsubdir)
        # self.checkVersion(version='wranglerVersion',parentdir=joinedTempDir, networkdir=networkdir,
        #                   gitdir=gitdir, projectsubdir=projectsubdir)

        commitstr = self.getCommit(gitdir)
        return commitstr

    def cloneAndApplyProject(self, networkdir, projectsubdir=None, tag=None, projtype=None, tempdir=None, **kwargs):
        """
        * *networkdir* corresponds to the dir relative to ``Y:\\networks``
        * *projectsubdir* is a subdir within that, or None if there's no subdir
        * *tag* is "1.0" or "1-latest", or None for just the latest version
        * *tempdir* is the parent dir to put the git clone dir; pass None for python to just choose
        * *kwargs* are additional args for the apply
        
        Returns the SHA1 hash ID of the git commit of the project applied
        """
        self.cloneProject(networkdir, projectsubdir, tag, projtype, tempdir, **kwargs)
        (joinedTempDir, networkdir, gitdir, projectsubdir) = self.getClonedProjectArgs(networkdir, projectsubdir, projtype, tempdir)
        return self.applyProject(parentdir=joinedTempDir, networkdir=networkdir,
                                 gitdir=gitdir, projectsubdir=projectsubdir, **kwargs)

    def getCommit(self, gitdir):
        """
        Figures out the SHA1 hash commit string for the given gitdir (so gitdir is a git dir).
        (e.g. a 40-character hex string)
        """
        # WranglerLogger.debug("getCommit({}) called".format(gitdir))
        # SET_CAPCLASS is special and setup by NetworkWrangler
        if gitdir.endswith("set_capclass"):
            return "set_capclass_N/A"

        cmd = r"git log -1"
        (retcode, retstdout, retstderr) = self._runAndLog(cmd, gitdir)
        if len(retstdout)<3:
            raise NetworkException("Git log failed; see log file")
        
        m = re.match(git_commit_pattern, retstdout[0])
        if not m:
            raise NetworkException("Didn't understand git log output: [" + retstdout[0] + "]")

        return m.group(1)

    def getTags(self, gitdir, commitstr):
        """
        Returns a list of all tags for this commit
        """
        cmd = r"git tag --contains " + commitstr
        (retcode, retstdout, retstderr) = self._runAndLog(cmd, gitdir)
        if len(retstdout)==0:
            return None
        return retstdout

    def logProject(self, gitdir, projectname, year=None, projectdesc=None, county=None):
        """
        Figures out the commit string and the tag.  Subclass should figure out the rest.
        Returns the SHA1 hash ID of the git commit of the project applied
        """
        commitstr = self.getCommit(gitdir)
        tag       = self.getTags(gitdir, commitstr)

        if year:
            yearstr = "%4d" % year
        else:
            yearstr = "    "

        WranglerLogger.info("%-4s | %-5s | %-40s | %-40s | %-10s | %s" %
                            (yearstr,
                             tag if tag else "notag",
                             commitstr if commitstr else "",
                             projectname.lstrip() if projectname else "",
                             county.lstrip() if county else "",
                             projectdesc.lstrip() if projectdesc else ""
                             )
                            )
        self.appliedProjects[projectname] = tag if tag else commitstr
        
        return commitstr
                
    def write(self, path='.', name='network', writeEmptyFiles=True, suppressQuery=False, suppressValidation=False):
        """
        Implemented by subclass
        """
        pass

    def reportDiff(self, netmode:str, other_network, directory:pathlib.Path, network_year:int, report_description:str, project_gitdir:str):
        """
        Implemented by subclass for the most part.
        Returns True if diffs were reported, false otherwise.

        other_network=WindowsPath('E:/temp/tmp8z_tyxhz') 
        directory=WindowsPath('E:/GitHub/NetworkWrangler/scripts/BlueprintNetworks/ProjectDiffs_Blueprint/net_2023_hwy_01_MAJ_Bay_Area_Forward_all')
        report_description='MAJ_Bay_Area_Forward_all'
        project_gitdir='Wrangler_tmp_2025Apr20.184622\\MAJ_Bay_Area_Forward_all'
        tempdir='Wrangler_tmp_2025Apr20.184622'
        """
        WranglerLogger.debug(f"Network.reportDiff() passed with {other_network=}\n  {directory=}\n  {network_year=}\n  {report_description=}\n  {project_gitdir=}")
        
        # create the report directory
        directory.mkdir(parents=True, exist_ok=True)

        # copy the tableau file into place
        # check for project+mode+year-specific version first
        TABLEAU_TEMPLATE = pathlib.Path(project_gitdir) / f"ProjectMapping_{netmode}_{network_year}.twb"
        if TABLEAU_TEMPLATE.exists():
            shutil.copyfile(TABLEAU_TEMPLATE, pathlib.Path(directory) / f"ProjectMapping_{report_description}.twb")
            WranglerLogger.debug(f"Copying project specific tableau from {TABLEAU_TEMPLATE}")
            return True

        # check for project+mode specific next
        TABLEAU_TEMPLATE = pathlib.Path(project_gitdir) / f"ProjectMapping_{netmode}.twb"
        WranglerLogger.debug(f"Looking for TABLEAU_TEMPLATE={TABLEAU_TEMPLATE}")

        if TABLEAU_TEMPLATE.exists():
            shutil.copyfile(TABLEAU_TEMPLATE, pathlib.Path(directory) / f"ProjectMapping_{report_description}.twb")
            WranglerLogger.debug(f"Copying project specific tableau from {TABLEAU_TEMPLATE}")
            return True
        
        # finally, use generic wrangler
        TABLEAU_TEMPLATE = pathlib.Path(__file__).parent.parent / "ProjectMapping" / f"ProjectMapping_{netmode}.twb"
        shutil.copyfile(TABLEAU_TEMPLATE, pathlib.Path(directory) / f"ProjectMapping_{report_description}.twb")

        return True