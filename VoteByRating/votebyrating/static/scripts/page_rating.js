$(function()
{
	var ratings_table = {
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
	
	function change_selcted_rating(value) {
		var name = $( ".selected_candidate" ).html()
		$( "#selected_rating" ).html( name + ": " );
		ratings_table[name] = value;
			
		if (value > 0)
		{
			for (var i = 0; i < value; ++i)
			{
				$( "#selected_rating" ).append( ":) " );
			}
		}
		else if (value == 0)
		{
			$( "#selected_rating" ).append( ":| " );
		}
		else
		{
			for (var i = 0; i < value * -1; ++i)
			{
				$( "#selected_rating" ).append( ":( " );
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
	
	var name;
	
	for (name in ratings_table)
	{
		$( "#candidates" ).append( "<div class='candidate' data-candidate='" + name + "'>" + name + "</div>" );
	}
	
	$( ".candidate:first" ).addClass( "selected_candidate" );
	change_selcted_rating( 0 );
	
	$( ".candidate" ).click(function()
	{
		$( ".candidate" ).removeClass( "selected_candidate" );
		$( this ).addClass( "selected_candidate" );
		var rating = ratings_table[$( this ).html()];
		$( "#slider_box" ).slider( "value", rating );
		change_selcted_rating( rating );
	});
	
	$( "#plus_box" ).click(function()
	{
		var rating = ratings_table[$( ".selected_candidate" ).html()];
		if (rating != 5)
		{
			$( "#slider_box" ).slider( "value", rating + 1 );
			change_selcted_rating(rating + 1);
		}
	});
	
	$( "#minus_box" ).click(function()
	{
		var rating = ratings_table[$( ".selected_candidate" ).html()];
		if (rating != -5)
		{
			$( "#slider_box" ).slider( "value", rating - 1 );
			change_selcted_rating(rating - 1);
		}
	});
		
});