# python_perl_storable

## NAME

python_perl_storable - распаковывает структуру из формата perl-storable

## VERSION

0.0.1

## DESCRIPTION

```
from python_perl_storable import thaw

thaw(data)
```

## SYNOPSIS

В языке perl есть свой формат бинарных данных для упаковки любых структур: хешей, списков, объектов, регулярок, скаляров, файловых дескрипторов, ссылок, глобов и т.п. Он реализуется модулем https://metacpan.org/pod/Storable.

Данный формат довольно популярен и запакованные в бинарную строку данные различных проектов на perl хранятся во внешних хранилищах: mysql, memcached, tarantool и т.д.

Данный змеиный модуль предназначен для дешифровки данных, полученных из таких хранилищ в структуры python. 

## METHODS

### thaw

#### Arguments

- events - события. Бинарная строка  

#### Returns

Any

# INSTALL

```sh
$ pip install 
```

# REQUIREMENTS

# LICENSE

Copyright (C) Yaroslav O. Kosmina.

This library is free software; you can redistribute it and/or modify
it under the same terms as Python itself.

# AUTHOR

Yaroslav O. Kosmina <darviarush@mail.ru>
