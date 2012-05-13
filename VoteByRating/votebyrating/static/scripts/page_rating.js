$(document).ready(function()
{
	$( "#slider_box" ).slider({
		min: -5,
		max: 5,
		orientation: "vertical",
		slide: function(event, ui)
		{
			$( "#selected_rating" ).html("Lorem Ipsum: ");
			if (ui.value > 0)
			{
				for (var i = 0; i < ui.value; ++i)
				{
					$( "#selected_rating" ).append(":) ");
				}
			}
			else if (ui.value == 0)
			{
				$( "#selected_rating" ).append(":| ");
			}
			else
			{
				for (var i = 0; i < ui.value * -1; ++i)
				{
					$( "#selected_rating" ).append(":( ");
				}
			}
		}
	});
		
	$( "#selected_rating" ).html("Lorem Ipsum: :| ");
		
	var ratings_table = {
		
			"Lorem Ipsum": 0,
			"Dolor Sit": 0,
			"Amet Consectetur": 0,
			"Adipiscing Elit": 0,
			"Cras A. Posuere": 0,
			"Nunc Donec": 0,
			"Imperdiet Bibendum": 0,
			"Orci Vitae": 0,
			"Tincidunt Vestibulum": 0,
			"Commodo Elementum": 0
	};
	
	for (var name in ratings_table)
	{
		$( "#candidates" ).append("<div class='candidate' data-candidate='" + name + "'>" + name + "</div>");
	}
	
	$( ".candiate" ).on("click", function(event){
		alert("Joy");
		$( ".candidate" ).removeClass("selected_candidate");
		$( this ).addClass("selected_candidate");
	});
		
});

