#!/usr/bin/perl -w

use Lingua::TypoGenerator 'typos';
my @typos = typos("information");
# returns qw(ibformation, ifnormation, iformation, iiformation, ...)
#print qw(@typos)
foreach $typo (@typos) {
print $typo . "\n";
}
# use accents
#@typos = typos("año", accents => 1);
# returns qw(aao, aaño, ano, ao, aoñ, añ, añi, añp...)
#print @typos