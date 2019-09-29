import contextlib
import csv
import multiprocessing as mp
import os
import shutil

import config as cfg

from tools import timeit

from workers import archiver, reader


@timeit
def write_archives(pool, arch_names):
    pool.map(archiver, arch_names)


@timeit
def read_archives(pool, arch_names, queue):
    pool.map(reader, [(x, queue) for x in arch_names])


@timeit
def write_csv(queue):
    with open(cfg.CSV1, 'w') as f1, open(cfg.CSV2, 'w') as f2:
        writer1 = csv.DictWriter(f1, fieldnames=['id', 'level'])
        writer1.writeheader()
        writer2 = csv.DictWriter(f2, fieldnames=['id', 'object_name'])
        writer2.writeheader()
        while not queue.empty():
            lst = queue.get()
            for data in lst:
                writer1.writerow({'id': data.id, 'level': data.level})
                for name in data.obj_names:
                    writer2.writerow({'id': data.id, 'object_name': name})


if __name__ == '__main__':
    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(os.path.join(cfg.MY_DIR, 'data'))

    os.makedirs(cfg.ARCH_DIR)
    os.makedirs(cfg.CSV_DIR, exist_ok=True)

    arch_names = [
        '.'.join(['arc'+str(i), 'zip']) for i in range(cfg.ARCHS_NUM)
    ]

    with mp.Pool() as pool:
        write_archives(pool, arch_names)
        q = mp.Manager().Queue()
        read_archives(pool, arch_names, q)
        write_csv(queue=q)
