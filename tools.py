import os
import time
from xml.etree import cElementTree as et
from zipfile import ZipFile

from random_wrapper import Random


class XmlData:
    pass


def timeit(f):
    def timed_f(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        end = time.time()
        print(f'Function: {f.__name__}, exec time={end-start}')
    return timed_f


def make_xml():
    rand = Random()
    root = et.Element('root')
    et.SubElement(root, 'var', name='id', value=rand.string)
    et.SubElement(root, 'var', name='level', value=str(rand.one_to_hundred))
    objects = et.SubElement(root, 'objects')
    for i in range(rand.one_to_ten):
        et.SubElement(objects, 'object', name=rand.string)
    return et.tostring(root)


def parse_xml(xml_str) -> XmlData:
    data = XmlData()
    data.obj_names = list()
    root = et.fromstring(xml_str)
    for child in root:
        if child.tag == 'var':
            if child.attrib['name'] == 'id':
                data.id = child.attrib['value']
            elif child.attrib['name'] == 'level':
                data.level = int(child.attrib['value'])
            else:
                raise Exception(
                    f'Unexpected xml var tag, attribs: {child.attrib.keys()}')
        elif child.tag == 'objects':
            for obj in child:
                data.obj_names.append(obj.attrib['name'])
        else:
            raise Exception(f'Unexpected xml tag: {child.tag}')

    return data


def make_arch(arch_dir=os.getcwd(), arch_name='test.zip', data_gen=range(0)):
    arch_name = os.path.join(arch_dir, arch_name)
    with ZipFile(arch_name, "a") as zip_file:
        file_base_name = 'file'
        count = 1
        for data in data_gen:
            file_name = '.'.join([file_base_name+str(count), 'xml'])
            zip_file.writestr(file_name, data)
            count += 1


def read_arch(arch_dir=os.getcwd(), arch_name='test.zip') -> []:
    zip_name = os.path.join(arch_dir, arch_name)
    lst = list()

    with ZipFile(zip_name) as zip_file:
        for finfo in zip_file.infolist():
            with zip_file.open(finfo) as f:
                lst.append(parse_xml(xml_str=f.read()))

    return lst
