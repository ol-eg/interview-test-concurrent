# -*- coding: utf-8 -*-
import contextlib
import os
import unittest
from xml.etree import cElementTree as et
from zipfile import ZipFile

import tools


class TestTools(unittest.TestCase):
    zip_file = os.path.join(os.getcwd(), 'test.zip')

    def setUp(self):
        with contextlib.suppress(FileNotFoundError):
            os.remove(TestTools.zip_file)

    def test_make_xml(self, xml_string=tools.make_xml()):
        root = et.fromstring(xml_string)
        self.assertTrue(root.tag == 'root')

        # <var name=’id’ value=’<случайное уникальное строковое значение>’/>
        # <var name=’level’ value=’<случайное число от 1 до 100>’/>
        var_elements = root.findall('var')
        self.assertEqual(len(var_elements), 2)
        for var in var_elements:
            self.assertEqual(set(var.attrib.keys()), set(['name', 'value']))
            self.assertTrue(var.attrib['name'] in ['id', 'level'])
            if var.attrib['name'] == 'level':
                num = int(var.attrib['value'])
                self.assertTrue(num > 0 and num < 101)
            else:
                self.assertTrue(len(var.attrib['value']) > 0)

        # <root><objects>...</objects></root>
        objects = root.findall('objects')
        self.assertEqual(len(objects), 1)

        # <objects><object name=’<случайное строковое значение>’/>...</objects>
        # from 1 to 10 objects
        objects = root.findall('*/object')
        num_of_objects = len(objects)
        self.assertTrue(num_of_objects > 0 and num_of_objects < 11)
        for obj in objects:
            self.assertTrue(len(obj.attrib['name']) > 0)

    def test_parse_xml(self):
        data = tools.parse_xml(xml_str=tools.make_xml())

        self.assertTrue(len(data.id) > 0)
        self.assertTrue(data.level > 0 and data.level < 101)
        for obj_name in data.obj_names:
            self.assertTrue(len(obj_name) > 0)

    def test_make_arch(self):
        xmls = (tools.make_xml() for _ in range(10))

        tools.make_arch(data_gen=xmls)
        self.assertTrue(os.path.isfile(TestTools.zip_file))

        with ZipFile(TestTools.zip_file) as z:
            for finfo in z.infolist():
                with z.open(finfo) as f:
                    xml = f.read()
                    self.test_make_xml(xml_string=xml)

    def test_read_arch(self):
        xmls = (tools.make_xml() for _ in range(10))

        tools.make_arch(data_gen=xmls)
        lst = tools.read_arch()

        for item in lst:
            self.assertTrue(len(item.id) > 0)
            self.assertTrue(item.level > 0 and item.level < 101)

        for obj_name in item.obj_names:
            self.assertTrue(len(obj_name) > 0)


if __name__ == '__main__':
    unittest.main()
