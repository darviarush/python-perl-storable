#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use open qw/:std :utf8/;

use Storable qw/freeze thaw/;
use JSON::XS;

my $json = JSON::XS->new->canonical->allow_nonref;
sub to_json {
    local $_ = $json->encode($_[0]);
    s/\bnull\b/None/;
    s/\bfalse\b/False/;
    s/\btrue\b/True/;
        $_
}

open my $f, ">", "tests/thaw.py" or die $!;

sub ascii {
    use bytes;
    my ($x) = @_;
    utf8::is_utf8($x) && utf8::encode($x);
    return join "", map { sprintf "\\x%02x", ord($_) } split m!!x, $x;
}

my $x;
my $i=0;
my $its = join "\n\n", map {
    my $name = $_->[0];
    my $data = $_->[1];
    my $freeze = freeze ref $data? $data: \$data;
    my $array = ascii($freeze);
    my $expect = $_->[3] // "self.assertEqual(thaw(data), ".($_->[2] // to_json($data)).", '$name')";

    $i++;

    #print "$name\t$freeze\n\n";

<< "END_IT"
    def test_throw_$i(self):
        """ $name """
        data = b'$array';
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
    ["Строка no utf8", do { $x="Привет!"; utf8::encode($x); $x}, "b'".ascii($x)."'"],
    ["Строка в utf8", "Привет!"],
    ["Скаляр", $x = do { my $x = -1.23; my $y=int $x; "$x" }],
    ["Массив", [123, -1.23, "123", "Привет!"]],
    ["Хеш", {1 => 23, -1.56e10 => -1.23, u => "123",  "Привет!" => [1, 2, 3], tip => {x => undef} }],
    ["Неопределённое значение", undef],
    ["Вложенный Массив", [123, -1.23, "123", [1, 2, 3], "Привет!"]],
    ["Рекурсивный Массив", do {
        my $x = [123, -1.23, undef, "123", "1" x 1000, [5], {x=>6}, "Привет!"];
        push @$x, $x;
        $x
    }, undef, "
        a = thaw(data)
        self.assertEqual(len(a), len(RECURSION_ARRAY))
        self.assertTrue(a[-1] == a)
    "],
    ["Объект", bless({x=>6}, "A::A"), undef, "
        class A__A:
            def getX(self):
                return self.x
        a = thaw(data, classes={'A::A': A__A})
        self.assertEqual(a.getX(), 6)
        self.assertIsInstance(a, A__A)
    "],
    ["Объект-массив", bless([5, "abc"], "A"), undef, "
        class A(list):
            pass
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

x=[123, -1.23, None, '123', '1' * 1000, [5], {'x': 6}, 'Привет!']
x.append(x)
RECURSION_ARRAY = x

class ThawTestCase(unittest.TestCase):

$its

if __name__ == '__main__':
    unittest.main()

END

close $f;
