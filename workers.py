import traceback

import config as cfg

import tools


def archiver(name):
    xmls = (tools.make_xml() for _ in range(cfg.XML_PER_ARCH))
    try:
        tools.make_arch(
            arch_dir=cfg.ARCH_DIR, arch_name=name, data_gen=xmls)
    except Exception as e:
        print(f'ERR: failed to make {name}')
        print(traceback.format_exc())
        print(e.message)


def reader(args):
    name = args[0]
    queue = args[1]
    try:
        queue.put(tools.read_arch(
            arch_dir=cfg.ARCH_DIR, arch_name=name))
    except Exception as e:
        print(f'ERR: failed to read {name}')
        print(traceback.format_exc())
        print(e.message)
