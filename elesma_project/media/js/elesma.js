$(document).ready(function() {
	$(".defaultText").focus(function(srcc) {
		if ($(this).val() == $(this)[0].title) {
		    $(this).removeClass("defaultTextActive");
		    $(this).val("");
		}});
	$(".defaultText").blur(function() {
		if ($(this).val() == "") {
		    $(this).addClass("defaultTextActive");
		    $(this).val($(this)[0].title);
		}});
	$(".defaultText").blur();        
	$(".uniForm #id_name").keyup(function() {
		$.ajax({ url: "/ajax/suggestions?q="+escape($("#id_name").val()),context: document.body, dataType: 'json', success: function(data){
			    $(".uniForm #id_name_suggestions").remove();
			    var results = data[0].results,
				suggestions = "",
				i = 0,
				l = results.length;
			    if (l > 0) {
				for (i=0; i<l; i++) {
				    var result = results[i];
				    if (i == 0) {
					suggestions += "<a href=\""+result[0] + "\">"+result[1] + "</a>";
				    } else if (i < l - 1) {
					suggestions += ", <a href=\""+result[0] + "\">"+result[1] + "</a>";
				    } else {
					suggestions += " or <a href=\""+result[0] + "\">"+result[1] + "</a>";
				    }}
				$(".uniForm #id_name").after($("<p id=\"id_name_suggestions\">Are you looking for "+suggestions+"?</p>"));
			    }}})});
    });