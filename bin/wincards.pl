use strict;
use warnings;
use LWP::Simple;
use URI::Escape;

sub get_card_image {
  my ($name, $i) = @_;

  my $card_cache = '/home/kevin/workspace/warlord/bin/images/warlords';

  my $encoded_name = '';
  my $url = '';
  if ( $name =~/\(Treasure\)/ ) {
    print "Treasure\n";
    $encoded_name = uri_escape($name);
    my $img_url = "http://www.temple-of-lore.com/spoiler/images/Promo/$encoded_name.jpg";
    getstore($img_url, "$card_cache/$i.jpg");
    return
  }
  $encoded_name = uri_escape($name);
  $url = "http://www.temple-of-lore.com/spoiler/popup.php?name=$encoded_name";

  print $url . "\n";
  my $html = get($url);
  if ( $html !~ /IMG src="(.*?)"/ ) {
    get_card_image($name, $i);
  } else {
    $html =~ /IMG src="(.*?)"/;
    print STDERR $1 . "\n";
    my $img_url = "http://www.temple-of-lore.com/spoiler/$1";
    getstore($img_url, "$card_cache/$i.jpg");
  }
}

unless (defined $ARGV[0]) {
  print "need to give us a name.";
  exit;
}

my $type = $ARGV[0];

`rm images/warlords/*`;
my $filename = 'next.dat';
open(my $fh, '<:encoding(UTF-8)', $filename)
  or die "Could not open file '$filename' $!";

my $i = 0;
my $card_cache = '/home/kevin/workspace/warlord/bin/images/warlords';
while (my $row = <$fh>) {
  $i++;
  my $index = sprintf('%03d', $i);
  chomp $row;
  print "processing $index $row\n";

  get_card_image($row, $index);
}

`cd $card_cache; montage -tile 10x7 -geometry 395x546 *.jpg $type.jpg`
