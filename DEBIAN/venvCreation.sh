#!/bin/bash
set -x
set -e
# ./venvCreation.sh -b BUILD_DIR -i INSTALL_DIR -o OUTPUT_PACKAGE 

while getopts "b:i:o:" o; do
    case "${o}" in
        b)
            bDir=${OPTARG}
            ;;
        i)
            iDir=${OPTARG}
            ;;
        o)
            outPacket=${OPTARG}
            ;;
        *)
            echo "Error in input"
						exit 1
            ;;
    esac
done
shift $((OPTIND-1))

oldPwd=$(pwd)

cd ${bDir}
python3.5 -m venv ${bDir}/venv/ 
. ${bDir}/venv/bin/activate 
pip3 install --no-cache-dir -r src/requirements.txt
find ${bDir}/venv/bin/ -type f -exec sed -i "s/$(echo ${bDir} | sed -e 's|/|\\/|g')/$(echo ${iDir}  | sed -e 's|/|\\/|g')/g" {} \;

cd $oldPwd
tar -cf ${outPacket} -C ${bDir} venv/
