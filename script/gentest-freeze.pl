#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use open qw/:std :utf8/;

require './script/gentest-util.pl';


open my $f, ">", "tests/test_freeze.py" or die $!;


my $x;
my $i=0;
my $its = join "\n\n", map {
    my $name = $_->[0];
    my $data = $_->[1];
    my $expect = $_->[3] // "self.assertEqual(thaw(data), value, '$name')";
    my $freeze = $_->[2] // do { use DDP {colored=>1}; 
    	my $x=to_json($data); p($name); $x };

    $i++;

    #print "$name\t$freeze\n\n";

<< "END_IT"
    def test_freeze_$i(self):
        """ $name """
        value = $freeze
        data = freeze(value)
        $expect
END_IT
}
    ["Натуральное", 123],
    ["Среднее натуральное", 128],
    ["Среднее натуральное побольше", 1_000_000],
    ["Большое натуральное", 5_000_000_000],
    ["Целое", -123],
    ["Среднее целое", -128],
    ["Среднее целое поменьше", -1_000_000],
    ["Большое целое", -5_000_000_000],
    ["Плавающее", 1.23],
    ["Плавающее отрицательное", -1.23e100, "-1.2300000000000003e+100"],
    ["Строка", "123"],
    ["Пустая строка", ""],
    ["Длинная строка", "1" x 1000, "'1' * 1000"],
    ["Строка no utf8", do { $x="Привет!"; utf8::encode($x); $x}, 
    	"b'".ascii($x)."'"],
    ["Строка в utf8", "Привет!"],
    ["Скаляр", $x = do { my $x = -1.23; my $y=int $x; "$x" }],
    ["Массив", [123, -1.23, "123", "Привет!"]],
    ["Хеш", {1 => 23, -1.56e10 => -1.23, u => "123",  "Привет!" => 
    	[1, 2, 3], tip => {x => undef} }],
    ["Неопределённое значение", undef],
    ["Вложенный Массив", [123, -1.23, "123", [1, 2, 3], "Привет!"]],
    ["Рекурсивный Массив", undef, '
        x = [123, -1.23, None, "123", "1" * 1000, [5], {"x":6}, 
        	"Привет!"];
        x.append(x)
        x
    ', undef, "
        a = thaw(data)
        self.assertEqual(len(a), len(RECURSION_ARRAY))
        self.assertTrue(a[-1] == a)
    "],
    ["Объект", undef, 'class A__A:
		def __init__(self, x):
			self.x = x
        def getX(self):
            return self.x
        A__A(x=6)', "
        
        a = thaw(data, classes={'A::A': A__A})
        self.assertEqual(a.getX(), 6)
        self.assertIsInstance(a, A__A)
    "],
    ["Объект-массив", undef, 'class A(list):
        pass
    	A([5, "abc"])', "
        
        a = thaw(data, classes={'A': A})
        self.assertEqual(len(a), 2)
        self.assertIsInstance(a, A)
    "],
    ;


print $f +<< "END";
"""
 * ВНИМАНИЕ!!!
 *   Тест сгенерирован утилитой $0.
 *   Ничего не менять: перетрётся.
"""

import sys
import unittest

sys.path.append(".")

from python_perl_storable.thaw import thaw
from python_perl_storable.freeze import freeze

x=[123, -1.23, None, '123', '1' * 1000, [5], {'x': 6}, 'Привет!']
x.append(x)
RECURSION_ARRAY = x

class FreezeTestCase(unittest.TestCase):

$its

if __name__ == '__main__':
    unittest.main()

END

close $f;
