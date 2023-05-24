#!/usr/bin/perl
# 
# Tyler Kendall, 07/25/06,
#  bug fix 1: 08/11/06
#  bug fix 2: 09/11/07
# Modified from trans2praat.pl originally writting by Nils Jahn
#  cf. http://www.spectrum.uni-bielefeld.de/LangDoc/EGA/Tools/
#
# usage: perl trs_to_tg.pl input-file > output-file

sub init {
    %speakers = () ;
    %tiers = () ;
    %utterances = () ;
    $start = 100000 ;
    $end = 0 ;
}

sub writeTG {
    $tcount = keys(%speakers);
    print "File type = \"ooTextFile\"\n";
    print "Object class = \"TextGrid\"\n\n";
    print "xmin = $start\n";
    print "xmax = $end\n";
    print "tiers? <exists>\n";
    print "size = $tcount\n";
    print "item []:\n";
    
    @sorted_spkrs = sort { $a cmp $b } keys (%speakers);
    for ($i = 0; $i <= $#sorted_spkrs; $i++) {
	$s_id = $sorted_spkrs[$i];
	print "    item [".($i+1)."]:\n";
	print "        class = \"IntervalTier\"\n";
	print "        name = \"".$speakers{$s_id}."\"\n";
	print "        xmin = $start\n";
	print "        xmax = $end\n";
	print "        intervals: size = ".($#{$tiers{$s_id}}+1)."\n";
	$j = 1;
	foreach (@{$tiers{$s_id}}) {
	    print "        intervals [$j]:\n";
	    print "            xmin = ".$_->{'start'}."\n";
	    print "            xmax = ".$_->{'end'}."\n";
	    print "            text = \"".$_->{'text'}."\"\n";
	    $j++;
	}
    }
}

sub main {
    @turn_spkrs = () ;
    $cur_spkr = "" ;
    while(<>) {
	chomp ;
	# generate hash for speakers
	if (/<Speaker.+?id=\"(.+?)\".+?name=\"(.+?)\"/) {
	    $speakers{$1} = $2 ;
	    $tiers{$1} = ();
	} elsif (/<Section.+?startTime=\"(.+?)\".+?endTime=\"(.+?)\"/) {
	    $start = $1 if ($1 < $start) ; #extract start and end time
	    $end = $2 if ($2 > $end) ;
	    
	} else { # put the rest of the file back in an array
	    push(@file_lines, $_);
	}
    }
    $in_turn = 0;
    $active_spkrs = '';
    $turn_start = 0;
    $turn_end = 0;
    $utt_needs_end = 0;
    foreach (@file_lines) {
	if (/<Turn speaker=\"(.+?)\".+?startTime=\"(.+?)\".+?endTime=\"(.+?)\"/) {
	    $in_turn = 1;
	    $active_spkrs = $1;
	    $turn_start = $2;
	    $turn_end = $3;
	    @turn_spkrs = split(/\s/, $1) ;
	    # default speaker is first (often only) speaker
	    $cur_spkr = $turn_spkrs[0]; 
	} elsif (/<\/Turn>/) {
	    if ($utt_needs_end) {
		$utt_needs_end = 0;
		foreach $s (@turn_spkrs) {
		    $utterances{$s}->[$#{$utterances{$s}}]->{'end'} = $turn_end;
		}
	    }
	    $in_turn = 0;
	    $active_spkrs = '';
	    $turn_start = $turn_end;
	    $turn_end = 0;
	    
	} elsif (!$in_turn) {
	    next;
	} elsif (/<Sync time=\"(.+?)\"/) {
	    if ($utt_needs_end) {
		$utt_needs_end = 0;
		foreach $s (@turn_spkrs) {
		    $utterances{$s}->[$#{$utterances{$s}}]->{'end'} = $1;
		}
	    }
	    foreach $s (@turn_spkrs) {
		push(@{$utterances{$s}}, 
		     {'start' => $1, 'text' => '', 'end' => ''});
	    }
	    $utt_needs_end = 1;
	    
	} elsif (/<Who nb=\"(\d+?)\"/) {
	    
	    $cur_spkr = $turn_spkrs[$1-1];
	} elsif ($_ !~ /^<.+/) { # this is a line of text
            # this cleans out ^M characters that seem to hide in the .trs file
	    s/\cM//sg; 
	    # this makes all " into '
	    s/\"/\'/g;
	    $cur_spkr = $active_spkrs if !$cur_spkr;
	    $utterances{$cur_spkr}->[$#{$utterances{$cur_spkr}}]->{'text'} = $_;
	}
    }

    # Now, need to buffer each tier with blank lines to account
    #  for unaccounted time in .trs (TextGrids have entries for blank lines)
    while (($s_id, $s_init) = each (%speakers)) {
	$last_time = $start;
	$last_end;
	foreach (@{$utterances{$s_id}}) {
	    if ($last_time < $_->{'start'}) {
		$pause = 
		{'start' => $last_time, 'text' => "", 'end' => $_->{'start'} };
		push(@{$tiers{$s_id}}, $pause, $_);
	    } else {
		push(@{$tiers{$s_id}}, $_);
	    }
	    $last_time = $_->{'end'};
	}
	if ($last_time < $end) {
	    $pause = {'start' => $last_time, 'text' => "", 'end' => $end };
	    push(@{$tiers{$s_id}}, $pause);
	}
    }
}

init;
main;
writeTG;
