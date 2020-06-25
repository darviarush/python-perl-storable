use strict;
use warnings;
use utf8;

use JSON::XS;
use DDP;

my $json = JSON::XS->new->canonical->allow_nonref;
sub to_json {
    local $_ = $json->encode($_[0]);
    s/\bnull\b/None/;
    s/\bfalse\b/False/;
    s/\btrue\b/True/;
        $_
}

sub ascii {
    use bytes;
    my ($x) = @_;
    utf8::is_utf8($x) && utf8::encode($x);
    return join "", map { sprintf "\\x%02x", ord($_) } split m!!x, $x;
}

1;