#! /usr/bin/env python3
# coding: utf-8
# This file is derived from make_it_for_release_enunu.py.
# Original Copyright (c) 2020-2021 oatsu

import argparse
import sys
from glob import glob
import os
from os.path import basename, dirname, join
from shutil import copy2, copytree
from jinja2 import Environment, FileSystemLoader
import yaml
from tqdm import tqdm


def get_parser():
    parser = argparse.ArgumentParser(
        description="Make ENUNU model for distribution",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("nnsvs_config", type=str, help="NNSVS config file")
    parser.add_argument("dist_config", type=str, help="Disbribution config file")
    return parser

def copy_train_config(config_dir, release_dir):
    """
    Copy acoustic_*.yaml, duration_*.yaml, timelag_*.yaml
    """
    print('copying config')
    copytree(config_dir, f'{release_dir}/{config_dir}')


def copy_dictionary(dictionary_dir, release_dir):
    """
    Copy *.table, *.conf
    """
    print('copying dictionary')
    copytree(dictionary_dir, f'{release_dir}/{dictionary_dir}')


def copy_question(path_question, release_dir):
    """
    Copy hed file
    """
    os.makedirs(f'{release_dir}/hed', exist_ok=True)
    print('copying question')
    copy2(path_question, f'{release_dir}/{path_question}')


def copy_scaler(singer, release_dir):
    """
    Copy *.joblib_scaler
    """
    os.makedirs(f'{release_dir}/dump/{singer}/norm', exist_ok=True)
    list_path_scaler = glob(f'dump/{singer}/norm/*_scaler.joblib')

    print('copying scaler')
    for path_scaler in tqdm(list_path_scaler):
        copy2(path_scaler, f'{release_dir}/{path_scaler}')


def copy_model(singer, name_exp, release_dir):
    """
    Copy NNSVS model
        name_exp: ID of experiments
    """
    name_exp = singer + '_' + name_exp
    os.makedirs(f'{release_dir}/exp/{name_exp}/acoustic', exist_ok=True)
    os.makedirs(f'{release_dir}/exp/{name_exp}/duration', exist_ok=True)
    os.makedirs(f'{release_dir}/exp/{name_exp}/timelag', exist_ok=True)
    list_path_model = glob(f'exp/{name_exp}/*/*.pth')
    list_path_model += glob(f'exp/{name_exp}/**/*.yaml', recursive=True)

    print('copying model')
    for path_model in tqdm(list_path_model):
        copy2(path_model, f'{release_dir}/{path_model}')


def copy_resources(resource_dir, release_dir):
    """
    Copy resource files.
    """
    os.makedirs(f'{release_dir}', exist_ok=True)
    
    resource_path_list = glob(join(resource_dir, '*'))

    print('Copying resources')
    for resource_path in tqdm(resource_path_list):
        copy2(resource_path, f'{release_dir}/{basename(resource_path)}')

        
def make_install_txt(template_dir, release_dir, description, encoding='CP932', newline="\r\n"):
    env = Environment(loader=FileSystemLoader(template_dir, encoding='utf8'))
    tpl = env.get_template('install.tmpl.txt')
    txt = tpl.render({'release_dir': basename(release_dir), 'description': description})
    
    install_txt_path=join(release_dir, "..", "install.txt")

    print('Making install.txt')
    with open(install_txt_path, 'w', encoding=encoding, newline=newline) as f:
        f.write(txt)

def make_character_txt(template_dir, release_dir, release_name, image, author, web, encoding='CP932', newline="\r\n"):
    env = Environment(loader=FileSystemLoader(template_dir, encoding='utf8'))
    tpl = env.get_template('character.tmpl.txt')
    txt = tpl.render({'release_name': release_name, 'image': image, 'author': author, 'web': web})
    
    install_txt_path=join(release_dir, "character.txt")

    print('Making character.txt')    
    with open(install_txt_path, 'w', encoding=encoding, newline=newline) as f:
        f.write(txt)
        
def main():
    """
    Copy model files for destribution.
    """

    args = get_parser().parse_args(sys.argv[1:])
    nnsvs_config_path=args.nnsvs_config
    dist_config_path=args.dist_config

    nnsvs_config = None
    with open(nnsvs_config_path, 'r', encoding="UTF-8") as f:
        nnsvs_config = yaml.load(f, Loader=yaml.FullLoader)
    if nnsvs_config is None:
        print(f"Cannot read NNSVS config file: {nnsvs_config_path}.")
        sys.exit(-1)

    dist_config = None
    with open(dist_config_path, 'r', encoding="UTF-8") as f:
        dist_config = yaml.load(f, Loader=yaml.FullLoader)
    if dist_config is None:
        print(f"Cannot read distribution config file: {dist_config_path}.")
        sys.exit(-1)
    
    singer = nnsvs_config['spk']
    dictionary_dir = nnsvs_config['sinsy_dic']
    model_name = dist_config['model_name']
    version = dist_config['version']
    description = dist_config['description']
    image = dist_config['image']
    author= dist_config['author']
    web=dist_config['web']
    
    release_name= f"{model_name}_v{version}"
    release_dir = f"release/{release_name}"

    path_question = nnsvs_config['question_path']
    name_exp = nnsvs_config['tag']
    config_dir = 'conf'
    template_dir = join(dirname(__file__), '../_common/template/')
    
    resource_dir = 'resources'
    
    print(template_dir)
#    copy_train_config(config_dir, release_dir)
#    copy_dictionary(dictionary_dir, release_dir)
#    copy_question(path_question, release_dir)
#    copy_scaler(singer, release_dir)
#    copy_model(singer, name_exp, release_dir)

    copy_resources(resource_dir, release_dir)

    make_install_txt(template_dir, release_dir, description)
    make_character_txt(template_dir, release_dir, release_name, image, author, web)

if __name__ == '__main__':
    main()
