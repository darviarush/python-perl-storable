import sys
import unittest
from data_printer import np, p

sys.path.append(".")

from python_perl_storable.thaw import thaw
from python_perl_storable.freeze import freeze
import subprocess

def freeze_perl(value, init=''):
    p = subprocess.Popen(["perl", "-e", "%suse Storable; print Storable::freeze(%s)" 
        % (init, value)], stdout=subprocess.PIPE)
        
    output, err = p.communicate()

    if p.returncode != 0:
        raise IOError("returncode=%s" % p.returncode)
    return output 

def thaw_perl(value, init='', noout=0):

    value = '"%s"' % (('%s' % value)[2:-1])

    x = subprocess.call(["perl", "-e", "%suse Storable; use Data::Dumper; %s(Storable::thaw(%s))" 
        % (init, ("" if noout else "print STDERR Dumper"), value)])

    if x != 0:
        raise IOError("returncode=%s" % x)


class FreezeTestCase(unittest.TestCase):

    def test_freeze_1(self):
        """ Натуральное """
        value = 123
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Натуральное')
        self.assertEqual(data, freeze_perl("\\%s" % value), 'Натуральное в storable')


    def test_freeze_2(self):
        """ Среднее натуральное """
        value = 128
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Среднее натуральное')
        self.assertEqual(data, freeze_perl("\\%s" % value), 'Среднее натуральное в storable')


    def test_freeze_3(self):
        """ Среднее натуральное побольше """
        value = 1000000
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Среднее натуральное побольше')
        self.assertEqual(data, freeze_perl("\\%s" % value), 'Среднее натуральное побольше в storable')


    def test_freeze_4(self):
        """ Большое натуральное """
        value = 5000000000
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Большое натуральное')
        self.assertEqual(data, freeze_perl("\\%s" % value), 'Среднее натуральное побольше в storable')


    def test_freeze_5(self):
        """ Целое """
        value = -123
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Целое')
        self.assertEqual(data, freeze_perl("\\%s" % value), 'Целое в storable')


    def test_freeze_6(self):
        """ Среднее целое """
        value = -128
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Среднее целое')
        self.assertEqual(data, freeze_perl("\\%s" % value), 'Среднее Целое в storable')


    def test_freeze_7(self):
        """ Среднее целое поменьше """
        value = -1000000
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Среднее целое поменьше')
        self.assertEqual(data, freeze_perl("\\%s" % value), 'Среднее Целое поменьше в storable')


    def test_freeze_8(self):
        """ Большое целое """
        value = -5000000000
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Большое целое')
        self.assertEqual(data, freeze_perl("\\%s" % value), 'Большое Целое в storable')


    def test_freeze_9(self):
        """ Плавающее """
        value = 1.23
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Плавающее')
        self.assertEqual(data, freeze_perl("\\%s" % value), 'Плавающее в storable')


    def test_freeze_10(self):
        """ Плавающее отрицательное """
        value = -1.23e+100
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Плавающее отрицательное')
        # perl игнорирует первый байт. Поэтому - без проверки
        #self.assertEqual(data, freeze_perl("\\%s" % value), 'Плавающее отрицательное в storable')


    def test_freeze_11(self):
        """ Строка """
        value = "123"
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Строка')
        self.assertEqual(data, freeze_perl("\\'%s'" % value, "use utf8;"), 'Строка в storable')


    def test_freeze_12(self):
        """ Пустая строка """
        value = ""
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Пустая строка')
        self.assertEqual(data, freeze_perl("\\'%s'" % value, "use utf8;"), 'Пустая строка в storable')


    def test_freeze_13(self):
        """ Длинная строка """
        value = '1' * 1000
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Длинная строка')
        self.assertEqual(data, freeze_perl("\\'%s'" % value, "use utf8;"), 'Длинная строка в storable')


    def test_freeze_14(self):
        """ Строка no utf8 """
        value = b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82\x21'
        v = "".join(["\\x%02x" % ch for ch in value])

        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Строка no utf8')
        self.assertEqual(data, freeze_perl("\\\"%s\"" % v), 'Строка no utf8')


    def test_freeze_15(self):
        """ Строка в utf8 """
        value = "Привет!"
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Строка в utf8')
        self.assertEqual(data, freeze_perl("\\'%s'" % value, "use utf8;"), 'Строка в utf8 в storable')

    def test_freeze_16(self):
        """ Скаляр """
        value = "-1.23"
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Скаляр')
        self.assertEqual(data, freeze_perl("\\'%s'" % value), 'Скаляр в storable')

    def test_freeze_17(self):
        """ Массив """
        value = [123,-1.23,"123","Привет!"]
        data = freeze(value)
        self.assertEqual(np(thaw(data)), np(value), 'Массив')
        self.assertEqual(data, freeze_perl(str(value), 'use utf8;'), 'Массив в storable')

    def test_freeze_18(self):
        """ Хеш """
        value = {"-15600000000":-1.23,"1":23,"tip":{"x":None},"u":"123","Привет!":[1,2,3]}
        data = freeze(value)

        self.assertEqual(np(thaw(data, iconv=lambda s: s.decode('utf-8'))), np(value), 'Хеш')
        thaw_perl(data, '', 1)

    def test_freeze_19(self):
        """ Неопределённое значение """
        value = None
        data = freeze(value)
        self.assertEqual(thaw(data), value, 'Неопределённое значение')
        self.assertEqual(data, freeze_perl("\\$x"), 'Неопределённое значение в storable')

    def test_freeze_20(self):
        """ Вложенный Массив """
        value = [123,-1.23,"123",[1,2,3],"Привет!"]
        data = freeze(value)
        self.assertEqual(np(thaw(data)), np(value), 'Вложенный Массив')
        self.assertEqual(data, freeze_perl(str(value), 'use utf8;'), 
            'Вложенный Массив в storable')


    def test_freeze_21(self):
        """ Рекурсивный Массив """
        value = [3, None, {"u": [7]}, [5, None], "Привет!"]
        value[3].append(value[2]["u"])
    
        #self.maxDiff = None

        data = freeze(value)

        p(value)
        p(thaw(data))

        x = freeze_perl('$x', 'use utf8; $x=[3, $none, {u=>[7]}, [5, $none], "Привет!"]; push @{$x->[3]}, $x->[2]{u};')

        print("python")
        p(data)
        print("perl")
        p(x)

        self.assertEqual(np(thaw(data)), np(value), 'Рекурсивный Массив')
        self.assertEqual(data, x, 'Рекурсивный Массив в storable')


    def test_freeze_22(self):
        """ Объект """
        class A__A:
            def __init__(self, x):
                self.x = x
            def getX(self):
                return self.x
        value = A__A(x=6)
        data = freeze(value)
        
        a = thaw(data, classes={'A::A': A__A})

        self.assertEqual(a.getX(), 6)
        self.assertIsInstance(a, A__A)

        x = freeze_perl('bless {x=>6}, "A::A"')

        self.assertEqual(data, x, 'Объект в storable')


    def test_freeze_23(self):
        """ Объект-массив """
        class A(list):
            pass

        value = A([5, "abc"])
        data = freeze(value)
        
        a = thaw(data, classes={'A': A})
        self.assertEqual(len(a), 2)
        self.assertIsInstance(a, A)
    


if __name__ == '__main__':
    unittest.main()

