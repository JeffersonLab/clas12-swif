#!/bin/csh -f

# 2017/02/7 Vardan Gyurjyan

# SET INPUTS
setenv INPUTFILE $1
setenv OUTPUTFILE $2
setenv TORUS -1.0
setenv SOLENOID -1.0


setenv MALLOC_ARENA_MAX 2
setenv MALLOC_MMAP_THRESHOLD_ 131072
setenv MALLOC_TRIM_THRESHOLD_ 131072
setenv MALLOC_TOP_PAD_ 131072
setenv MALLOC_MMAP_MAX_ 65536
setenv MALLOC_MMAP_MAX_ 65536

setenv CLARA_HOME "/group/da/vhg/testbed/clara/myClara"
setenv CLAS12DIR "/group/da/vhg/testbed/clara/myClara/plugins/clas12"

# PRINT INPUTS
echo "CLARA_HOME        = $CLARA_HOME"
echo "CLAS12DIR         = $CLAS12DIR"
echo "TORUS             = $TORUS"
echo "SOLENOID          = $SOLENOID"
echo "INPUTFILE         = $INPUTFILE"
echo "OUTPUTFILE        = $OUTPUTFILE"


# COPY INPUT FILE TO WORKING DIRECTORY
# This step is necessary since the cache files will be created as soft links in the current directory, and we want to avoid large I/O processes.
# We first copy the input file to the current directory, then remove the link.
ls -l
cp $INPUTFILE ./tmp_file
rm -f $INPUTFILE
mv tmp_file $INPUTFILE
ls -l

# RUN DECODER
$CLARA_HOME/plugins/clas12/bin/decoder -t $TORUS -s $SOLENOID -i $INPUTFILE -o $OUTPUTFILE -c

