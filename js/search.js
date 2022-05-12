// this function executes our search via an AJAX call
function runSearch( term ) {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    
    // transforms all the form parameters into a string we can send to the server
    var frmStr = $('#gene_search').serialize();
    
    $.ajax({
        url: './search_database.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
			$('.to_gene').click(function(e)
                {
					var symbol=this.value;
					var name=this.id;
					window.location.href="./search_genes.cgi?symbol="+symbol+"&name="+name;
					    
                });
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform gene search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
        }
    });
}


// this processes a passed JSON structure representing gene matches and draws it
//  to the result table

function processJSON( data ) {
    // set the span that lists the match count
    $('#match_count').text( data.match_count );
    
    // this will be used to keep track of row identifiers
    var next_row_num = 1;
	
   
    // iterate over each match and add a row to the result table for each
    $.each( data.matches, function(i, item) {
		 var tr = $("<tr />");
                $.each(item, function (k, v) {
                    tr.append($("<td />", { html: v }));
                    
                })
				tr.append('<button class="to_gene" value='+item.locus_id+' id='+item.product.split(' ').join('_')+'>'+item.locus_id+'</button>');
  
					$("#mytable").append(tr);
    });
    
    // now show the result section that was previously hidden
    $('#results').show();
}


// run our javascript once the page is ready
$(document).ready( function() {
(new URL(window.location.href)).searchParams.forEach((x, y) =>
    document.getElementById(y).value = x.replaceAll("_"," "));
    // define what should happen when a user clicks submit on our search form
    $('#submit').click( function() {
        runSearch();
        return false;  // prevents 'normal' form submission
    });
	
});
