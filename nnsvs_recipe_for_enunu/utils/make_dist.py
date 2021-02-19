#! /usr/bin/env python3
# coding: utf-8
# This file is derived from make_it_for_release_enunu.py.
# Original Copyright (c) 2020-2021 oatsu

import argparse
import sys
from glob import glob
import os
from os.path import basename, dirname, join
from shutil import copy2, copytree, make_archive
from jinja2 import Environment, FileSystemLoader
import yaml
from tqdm import tqdm
import zipfile

# monkey patch for making zipfile which filenames are encoded with CP932
# https://scrapbox.io/shimizukawa/Python3%E3%81%A7cp932%E3%81%AAzip%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E4%BD%9C%E3%82%8A%E3%81%9F%E3%81%84
import unittest.mock
def _patch_encodeFilenameFlags(self):
    try:
        return self.filename.encode('ascii'), self.flag_bits
    except UnicodeEncodeError:
        return self.filename.encode('cp932'), self.flag_bits
   
zipcp932patch = unittest.mock.patch(
    'zipfile.ZipInfo._encodeFilenameFlags',
    _patch_encodeFilenameFlags)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Make ENUNU model for distribution",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("nnsvs_config", type=str, help="NNSVS config file")
    parser.add_argument("dist_config", type=str, help="Disbribution config file")
    parser.add_argument("dest_dir", type=str, help="Destination directory")    
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
    copytree(dictionary_dir, f'{release_dir}/dic')


def copy_question(question_path, release_dir):
    """
    Copy hed file
    """
    os.makedirs(f'{release_dir}/hed', exist_ok=True)
    print('copying question')
    copy2(question_path, f'{release_dir}/{question_path}')


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
    list_path_model = glob(f'exp/{name_exp}/*/latest.pth', recursive=True)
    list_path_model += glob(f'exp/{name_exp}/*/best_loss.pth', recursive=True)
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
        name = basename(resource_path)
        if name != "enuconfig.yaml":
            copy2(resource_path, f'{release_dir}/{name}')

        
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

def make_enuconfig(template_dir, release_dir, nnsvs_config):
    env = Environment(loader=FileSystemLoader(template_dir, encoding='utf8'))
    tpl = env.get_template('enuconfig.tmpl.yaml')
    yaml = tpl.render({
        'question_path': basename(nnsvs_config['question_path']),
        'spk': nnsvs_config['spk'],
        'tag': nnsvs_config['tag'],
        'acoustic_eval_checkpoint': nnsvs_config['acoustic_eval_checkpoint'],
        'duration_eval_checkpoint': nnsvs_config['duration_eval_checkpoint'],
        'timelag_eval_checkpoint': nnsvs_config['timelag_eval_checkpoint'],
        'timelag_allowed_range': nnsvs_config['timelag_allowed_range'],
        'timelag_allowed_range_rest': nnsvs_config['timelag_allowed_range_rest']
    })

    enuconfig_yaml_path=join(release_dir, "enuconfig.yaml")

    print('Making enuconfig.yaml')    
    with open(enuconfig_yaml_path, 'w') as f:
        f.write(yaml)
        
def copy_extra_files(extra_files_list, release_dir):
    """
    Copy extra files
    """
    print('Copying extra files')
    for extra_files_path in tqdm(extra_files_list):
        copytree(extra_files_path, f'{release_dir}/{basename(extra_files_path)}')
        
def main():
    """
    Copy model files for destribution.
    """

    args = get_parser().parse_args(sys.argv[1:])
    nnsvs_config_path=args.nnsvs_config
    dist_config_path=args.dist_config
    dest_dir=args.dest_dir
    
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

    question_path = nnsvs_config['question_path']
    name_exp = nnsvs_config['tag']
    extra_files_list = dist_config['extra_files_list']
    
    config_dir = 'conf'
    template_dir = join(dirname(__file__), '../_common/template/')
    resource_dir = 'resources'

    
    copy_train_config(config_dir, release_dir)
    copy_dictionary(dictionary_dir, release_dir)
    copy_question(question_path, release_dir)
    copy_scaler(singer, release_dir)
    copy_model(singer, name_exp, release_dir)

    copy_resources(resource_dir, release_dir)

    make_install_txt(template_dir, release_dir, description)
    make_character_txt(template_dir, release_dir, release_name.replace('_', ' '), image, author, web)

    make_enuconfig(template_dir, release_dir, nnsvs_config)
    
    copy_extra_files(extra_files_list, release_dir)
    
#    archive_file_name = release_name ; ".zip"
#    make_archive(join(dest_dir, archive_file_name), 'zip', root_dir=join(release_dir, ".."))
    
if __name__ == '__main__':
    main()
