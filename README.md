This is the site I refer to as Jank Yanker for creating PDFs for proxy warlord decks.  This scraps the 
temple of lore website with permission from his owner.

The program was running on a ubuntu 12 server.  It uses perl and image magick. The site was served using
apache and perl cgi.  Below is the section of apache config I used in /etc/apache2/site-available/default

# Older apache

<VirtualHost *>
  ServerName warlord.e-kevin.com

	DocumentRoot /home/sites/warlord
	<Directory /home/sites/warlord>
    AllowOverride None
    AddHandler cgi-script .cgi
    Options ExecCGI -MultiViews FollowSymLinks
    Order allow,deny
    Allow from all 
    DirectoryIndex index.cgi
	</Directory>
</VirtualHost>


# Apache 2.4

<VirtualHost *>                                                                               
  #ServerName warlord.e-kevin.com    
    
  DocumentRoot /home/sites/warlord    
  <Directory /home/sites/warlord>    
    AllowOverride None    
    AddHandler cgi-script .cgi .pl    
    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch    
    Require all granted    
    DirectoryIndex index.cgi    
  </Directory>    
</VirtualHost>

For the perl side you will need to make sure these perl modules are installed.
 
use CGI;
use Template;
use FindBin qw($Bin);
use LWP::Simple;
use URI::Escape;
use JSON;
use File::Slurp;
use LWP::Simple;                                                                                                              
use URI::Escape;

Instead of using the perl image magick libs I just make command line calls to imagemagick's montage command line utility
which will need to be installed.  You can find where this happens in bin/wincards/Warlord.pm.

I do not have time to address any issues with changes or setting up the code.  Anyone may feel free to use it,
change it or use ideas from it as a base for a new more modern version.  As of 2017, I wrote this about 7 years ago and used
techniques from the last 90's before all these fancy frameworks existed. So look at this as fixing up an old model T car 
in some ways. :)  It might be best to use the scrapping techniques and rewrite this project using a more modern framework 
like Ruby on Rails.  But right now, it is what it is.  Good luck and have fun yanking your jank.
