#!/usr/bin/perl

use CGI;
use Template;
use FindBin qw($Bin);
use LWP::Simple;
use URI::Escape;
use JSON;
use File::Slurp;

use lib "$Bin/bin/wincards";
use WarLord;

use warnings;
use strict;

my $config = {
  INCLUDE_PATH => "$Bin/templates",     # or list ref
  INTERPOLATE  => 1,               # expand "$var" in plain text
  POST_CHOMP   => 1,               # cleanup whitespace
  EVAL_PERL    => 1,               # evaluate Perl code blocks
};

my $info = CGI::Vars();

if ($$info{a} && $$info{a} eq 'search') {
    search($$info{name});
} elsif ($$info{a} && $$info{a} eq 'pdf') {
    createPDF();
} else {
    main();
}

sub createPDF {
    my $data = decode_json($$info{mydata});
    my $name = $$data[0]{name};
    my $ts = time;
    WarLord::createPDF($data, $ts);
    print "Content-Type:application/pdf\n";
    print "Content-Disposition: attachment; filename=\"$name.pdf\"\n";
    print "\n";
    my $pdf = read_file("$ts.pdf");
    print $pdf;
    unlink "$ts.pdf";
}

sub search {
    my ($name) = @_;
     
    my $encoded_name = uri_escape($name);
    my $html = get("http://www.temple-of-lore.com/spoiler/search_results.php?name=$encoded_name");
    my @lines = split /\n/, $html;
    my @results = ();
    foreach my $line (@lines) {
        if ($line =~ /switchPic/) {
            $line =~ /\"(.*\.jpg)\"?/;
            my $img_url = $1;
            $line =~ /;>(.*?)<\/A>/;
            my $found = $1;
            push @results, { name => $found, url => $img_url };
        }
    }

    my $template = Template->new($config);
    print CGI::header("text/html");
    my $input = 'search_results.html';
    my $vars = { results => \@results };
    $template->process($input, $vars)
}

sub main {
    my $template = Template->new($config);

    print CGI::header("text/html");
    my $input = 'index.html';
    my $vars = {};
    $template->process($input, $vars) || die "Template process failed: ", $template->error(), "\n"
}
