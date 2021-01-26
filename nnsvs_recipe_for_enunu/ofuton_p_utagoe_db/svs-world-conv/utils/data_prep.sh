#! /bin/bash

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)

if [ $# -ne 1 ];then
    echo "USAGE: data_prep.sh config_path"
    exit 1
fi

config_path=$1

# Step 1:
# Generate full-context lables from music xml using pysinsy
# pysinsy: https://github.com/r9y9/pysinsy

python $NO2_ROOT/utils/gen_lab.py $config_path

# Step 2:
# Align sinsy's labels and singing voice database's alignment file by DTW
# The reason we need this is because there are some mismatches between
# sinsy output and singing voice database's provided alignment.
# e.g., number of pau/sil
# One solution for this is to correct alignment manually, but it would be laborious to work.
# To mitigate the problem, I decided to follow the following strategy:
#  1. Take an rough alignment using DTW
#  2. Manually check if the alignment is correct, Otherwise correct it manually.
# which should save my time for manual annotations.

python $NO2_ROOT/utils/align_lab.py $config_path

# Step 2A:
# ------------------------------
# THIS STEP IS ADDED FOR ENUNU.
# ------------------------------
# Modify sinsy's labels for ENUNU.
# Following contexts are modified.
# - Contexts around rest notes. (d, f)
# - Contexts of picth of notes. (e2, e3)
# - Contexts for Phrases. (g, h, i)

#python $ENUNU_ROOT/py/modify_full_label_for_enunu.py $config_path

# Step 3:
# Perform segmentation.
python $NO2_ROOT/utils/perf_segmentation.py $config_path

# Step 4:
# Make labels for training
# 1. time-lag model
# 2. duration model
# 3. acoustic model
python $NO2_ROOT/utils/finalize_lab.py $config_path
