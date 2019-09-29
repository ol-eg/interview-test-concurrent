import multiprocessing
import os

MY_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(MY_DIR, 'data')
ARCH_DIR = os.path.join(DATA_DIR, 'archives')
CSV_DIR = os.path.join(DATA_DIR, 'csv')
CSV1 = os.path.join(CSV_DIR, 'file1.csv')
CSV2 = os.path.join(CSV_DIR, 'file2.csv')
ARCHS_NUM = 50
XML_PER_ARCH = 100
