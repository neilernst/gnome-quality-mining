#!/usr/bin/perl -w

my $word = $ARGV[0];
if (!defined($word)) {
    print "define a word\n";
    exit;
}
use Lingua::TypoGenerator 'typos';
my @typos = typos($word);
# returns qw(ibformation, ifnormation, iformation, iiformation, ...)
#print qw(@typos)
foreach $typo (@typos) {
print $typo . " ";
}
# use accents
#@typos = typos("año", accents => 1);
# returns qw(aao, aaño, ano, ao, aoñ, añ, añi, añp...)
#print @typos