#!/usr/bin/perl


# author: Nils Jahn
# usage: perl trans2praat.pl input-file > output-file

sub initVariables {
	@store = () ;
	$time = 0 ;
	$anz = 1 ;
	$tiers = 0 ;
	$start = 1000 ;
	$end = 0 ;
	@t1 = () ;
	@t2 = () ;
}

sub writeFile {
	$item = $#t1 + 1 ;  # print data into file
	$tstamps = $#store + 1 ;
	print "File type = \"ooTextFile\"\n" ;
	print "Object class = \"TextGrid\"\n\n" ;
	print "xmin = $start\n" ;
	print "xmax = $end\n" ;
	print "tiers? <exists>\n" ;
	print "size = $tiers\n" ;
	print "item[]:\n" ;
	for ($i=0; $i < $tiers; $i++) {
		$ctier = $i + 1 ;
		$size = $#t1 + 1 ;
		print "\titem\[$ctier\]:\n" ;
		print "\t\tclass = \"IntervalTier\"\n" ;
		print "\t\tname = \"tier $ctier\"\n" ;
		print "\t\txmin = $start\n" ;
		print "\t\txmax = $end\n" ;
		print "\t\tintervals: size = $size\n" ;
		if ($ctier == 1) {	# for 1st tier
			$ctext = 1 ;
			$ctime = 0 ;
			foreach $data (@t1) {
				print "\t\tintervals\[$ctext]\n" ;
				print "\t\t\txmin = $store[$ctime]\n" ;
				print "\t\t\txmax = $store[$ctime+1]\n" ;
				print "\t\t\ttext = \"$data\" \n" ;
				$ctext++ ;
				$ctime = $ctime+2 ;
			}
		}	
		if ($ctier == 2) {
			$ctext = 1 ;
			$ctime = 0 ;
			foreach $data (@t2) {	# for 2nd tier
				print "\t\tintervals\[$ctext]\n" ;
				print "\t\t\txmin = $store[$ctime]\n" ;
				print "\t\t\txmax = $store[$ctime+1]\n" ;
				print "\t\t\ttext = \"$data\" \n" ;
				$ctext++ ;
				$ctime = $ctime+2 ;
			}
		}
	}
}

sub main {
	while(<>) {
		chomp ;
		if (/<Section.+?startTime=\"(.+?)\".+?endTime=\"(.+?)\"/) {
			$start = $1 if ($1 < $start) ; #extract start and end time
			$end = $2 if ($2 > $end) ;
		} 
		if ((/<Sync time=\"(.+?)\"/) && ($time==0)) { # for start time only
			$time = 1 ;			      # time is stored twice
			if ($anz < 3) {
				push(@store, $1) ;
			}
			else { 
				push(@store, $store[$#store]) ;
				push(@store, $1) ;
			}
			$anz++ ;
		}
		elsif ((/<Sync time=\"(.+?)\"/) && ($time==1)) { # if start and end time is given
			push(@store, $1) ;
		}
		if (($_ =~ m/^\w+/) && ($time==1)) { # get annotated text of 1st tier
			$mot =  $_ ;
			$mot =~ s/\s{2,}/ / ;
			$tiers = 1 if $tiers  == 0 ;
			push(@t1, $mot) ;
			$time = 0 ;
		}
		elsif (($_ =~ m/^\w+/) && ($time==0)) { # get annotated text of 2nd tier
			$mot = $_ ;
			$mot =~ s/\s{2,}/ / ;
			$tiers = 2 ;
			push(@t2, $mot) ;
		}	
		if ((/<\/Episode/) && ($time == 0)) { # if Episode tag is closed and no end time given
			push(@store, $store[$#store]) ; # copy last time stamp and push it onto array
			push(@store, $end) ;
			$time = 1 ;
		}
	}
}

initVariables ;
main ;
writeFile ;
