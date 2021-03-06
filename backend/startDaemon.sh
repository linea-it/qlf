#!/bin/bash
echo "Initializing QLF Daemon..."

export QLF_PROJECT=$(pwd)/framework/qlf
export QLF_ROOT=$(pwd)

for package in desispec desiutil desimodel specter; do
	echo "Setting $package..."
	export PATH=$QLF_ROOT/$package/bin:$PATH
	export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

export PYTHONPATH=$QLF_ROOT/framework/bin:$PYTHONPATH
export DESIMODEL=$QLF_ROOT/desimodel

python -Wi framework/bin/servers.py