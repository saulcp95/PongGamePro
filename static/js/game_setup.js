$(function(){
	('button').click(function(){
		var modalidad = $('#j1 :selected').text();
		
		$.ajax({	
			if (modalidad = "Jugador vs PC")
			{
				url: 'localhost:8000/jugar/';
				data: $('form').serialize();
				type: 'GET';
				dataType: "html";
			}
			else
			{
				url: 'localhost:8000/login/';
				data: $('form').serialize();
				type: 'GET';
				dataType: "html";
			}
		
		}
     });
    return false;
	});
});