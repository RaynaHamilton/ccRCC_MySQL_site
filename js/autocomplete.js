
function autosearch() {
	//searches the database using search_term input, then autocompletes results
    
	if ($("#search_term").val() != ""){
    var frmStr = $('#gene_search').serialize();
    
    $.ajax({
        url: './search_product.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            var results=autoJSON(data);
			if (results.length>=5){$( "#search_term" ).autocomplete({source:results.slice(0,5)});}
			$( "#search_term" ).autocomplete({source:results.slice(0,5)});
			
			
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform gene search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
				  
        }
    });
	
	};
}

function autoJSON( data ) {
    // returns an array containing unique search results
	var results_2=[]
    
    $.each( data.matches, function(i, item) {
		results_2.push(item.product);
        

    });
	
    return [...new Set(results_2)];
    
}

