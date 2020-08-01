# -*- coding:utf-8 -*-

import csv
import sys
import time
from sudachipy import dictionary
from sudachipy.dictionarylib.dictionaryheader import DictionaryHeader
from sudachipy.dictionarylib import USER_DICT_VERSION_2
from sudachipy.dictionarylib import BinaryDictionary
from sudachipy.dictionarylib.userdictionarybuilder import UserDictionaryBuilder

USER_DEF_FILE = './user_def.txt'
USER_CSV_FILE = './user_dic.csv'
USER_DIC_FILE = './user.dic'
TOKENIZER_OBJ = dictionary.Dictionary().create()
SYSTEM_DIC_PATH = dictionary.config.settings.system_dict_path()

def convert_def_to_csv(def_filename, csv_filename):
    """defファイルからCSVユーザ辞書ファイルに変換

    SudachiPyでは、CSVユーザ辞書ファイルを使用してユーザ辞書を作成する手順を示しているが、
    機能が多くメンテナンスが大変なので、以下の特徴を持つdefファイルフォーマットを定義する。

    - 品詞は「普通名詞」と「固有名詞」のみ
    - 品詞、見出し、読み以外は固定

    defファイルのフォーマットは以下の通り。

    <品詞>,<見出し>,<読み>

    CSVユーザ辞書ファイルはSudachiPyで決められたものを使用。

    :param def_filename: defファイルのファイルパス
    :param csv_filename: CSVユーザ辞書ファイルパス
    """
    lines = []
    with open(def_filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            pos = row[0]
            sfc = row[1]
            red = row[2]
            lines.append('%s,4786,4786,5000,%s,名詞,%s,一般,*,*,*,%s,%s,*,*,*,*,*'
                         % (sfc, sfc, pos, sfc, red))

    with open(csv_filename, 'w') as f:
        for line in lines:
            f.write(line+'\n')


def convert_csv_to_dic(user_csv_file, user_dic_file):
    """CSVユーザ辞書ファイルからユーザ辞書ファイルに変換

    :param user_csv_file: CSVユーザ辞書ファイルパス
    :param user_dic_file: ユーザ辞書ファイルパス
    """
    header = DictionaryHeader(USER_DICT_VERSION_2, int(time.time()),
                              'Build User Dictionary')
    dict_ = BinaryDictionary.from_system_dictionary(SYSTEM_DIC_PATH)
    with open(user_dic_file, 'wb') as wf:
        wf.write(header.to_bytes())
        builder = UserDictionaryBuilder(dict_.grammar, dict_.lexicon)
        builder.build([user_csv_file], None, wf)


if __name__ == '__main__':
    user_def_file = USER_DEF_FILE
    if len(sys.argv) == 2:
        user_def_file = sys.argv[1]

    user_csv_file = USER_CSV_FILE
    user_dic_file = USER_DIC_FILE

    convert_def_to_csv(user_def_file, user_csv_file)
    convert_csv_to_dic(user_csv_file, user_dic_file)
    print('done')
