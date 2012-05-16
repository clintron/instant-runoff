$(function()
{
	var candidate_rating_table = {
			"Lorem Ipsum":0,
			"Dolor Sit":0,
			"Amet Consectetur":0,
			"Adipiscing Elit":0,
			"Cras A. Posuere":0,
			"Nunc Donec":0,
			"Imperdiet Bibendum":0,
			"Orci Vitae":0,
			"Tincidunt Vestibulum":0,
			"Commodo Elementum":0
	};
	
	var rating_candidate_table = new Array();
	
	for ( var i = 0; i < 11; ++i )
	{
		rating_candidate_table.push( new Array() );
	}
	
	for ( var name in candidate_rating_table )
	{
		rating_candidate_table[candidate_rating_table[name] + 5].push( name );
	}
	
	function remove_candidate_from_rating_table( name )
	{
		for ( var value in rating_candidate_table )
		{
			var index = rating_candidate_table[value].indexOf( name );
			if ( index != -1 )
			{
				rating_candidate_table[value].splice( index, 1 );
				break;
			}
		}
	}
	
	var rating_background_colors =
	[
		"minus_5",
		"minus_4",
		"minus_3",
		"minus_2",
		"minus_1",
		"dont_care",
		"plus_1",
		"plus_2",
		"plus_3",
		"plus_4",
		"plus_5"
	];
	
	function populate_slider_labels()
	{
		$( "#slider_labels" ).html( "" );
		for ( var value = rating_candidate_table.length - 1; value >= 0; --value )
		{
			var candidates = rating_candidate_table[value];
			$( "#slider_labels" ).append( "<div class='candidate_label' id='" + rating_background_colors[value] + "'></div>" );
			for (var index in candidates)
			{
				var name = candidates[index];
				var html = "";
				if ( $( "div.selected_candidate" ).html() == name )
				{
					html = "<span class='selected_candidate'>" + name + "</span> ";
				}
				else if ( index != candidates.length - 1 )
				{
					html = name + ", ";
				}
				else
				{
					html = name + " ";
				}
				$( ".candidate_label:last" ).append( html );
			}
		}
	}
	
	function change_selcted_rating( value )
	{
		var name = $( ".selected_candidate" ).html()
		$( "#selected_rating" ).html( "<span>" + name + "</span><div class='clear'></div>" );
		candidate_rating_table[name] = value;
		remove_candidate_from_rating_table( name );
		rating_candidate_table[value + 5].push( name );
		populate_slider_labels();
			
		if ( value > 0 )
		{
			for ( var i = 0; i < value; ++i )
			{
				$( "#selected_rating .clear" ).before( "<div class='ratingGood'></div>" );
			}
		}
		else if ( value == 0 )
		{
			$( "#selected_rating .clear" ).before( "<div class='ratingNeutral'></div>" );
		}
		else
		{
			for ( var i = 0; i < value * -1; ++i )
			{
				$( "#selected_rating .clear" ).before( "<div class='ratingBad'></div>" );
			}
		}
	};
	
	$( "#slider_box" ).slider({
		min: -5,
		max: 5,
		orientation: "vertical",
		slide: function( event, ui )
		{
			change_selcted_rating( ui.value );
		}
		
	});
	
	for ( var name in candidate_rating_table )
	{
		$( "#candidates" ).append( "<div class='candidate'>" + name + "</div>" );
	}
	
	$( ".candidate:first" ).addClass( "selected_candidate" );
	change_selcted_rating( 0 );
	
	$( ".candidate" ).click(function()
	{
		$( ".candidate" ).removeClass( "selected_candidate" );
		$( this ).addClass( "selected_candidate" );
		var rating = candidate_rating_table[$( this ).html()];
		$( "#slider_box" ).slider( "value", rating );
		change_selcted_rating( rating );
	});
	
	$( "#plus_box" ).click(function()
	{
		var rating = candidate_rating_table[$( ".selected_candidate" ).html()];
		if (rating != 5)
		{
			$( "#slider_box" ).slider( "value", rating + 1 );
			change_selcted_rating( rating + 1 );
		}
	});
	
	$( "#minus_box" ).click(function()
	{
		var rating = candidate_rating_table[$( ".selected_candidate" ).html()];
		if (rating != -5)
		{
			$( "#slider_box" ).slider( "value", rating - 1 );
			change_selcted_rating( rating - 1 );
		}
	});
	
	$(document).on( "click", ".candidate_label", function()
	{
		var value = 5 - $( ".candidate_label" ).index( $( this ) );
		$( "#slider_box" ).slider( "value", value );
		change_selcted_rating(value);
	});
	
	for ( var i = 0; i < 11; ++i )
	{
		$( "#tick_marks" ).append( "-<br/>" );
	}
		
});