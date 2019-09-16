	$(document).ready( function() {
		
		$('body').on("click", ".larg div h3", function(){
			if ($(this).children('span').hasClass('close')) {
				$(this).children('span').removeClass('close');
			}
			else {
				$(this).children('span').addClass('close');
			}
			$(this).parent().children('p').slideToggle(250);
		});
		
		$('body').on("click", "nav ul li a", function(){
			var title = $(this).data('title');
			$('.title').children('h2').html(title);
		});
	});
	$("#info").hide();
	$("#attendance").hide();
	$("#subjects").hide();
	$("#Security").hide();

//srs
$(function() {
  // Bind Click event to the drop down navigation button
  $(".nav-button").click(function() {
    /*  Toggle the CSS closed class which reduces the height of the UL thus 
    hiding all LI apart from the first */
    $(this).parent().parent().toggleClass("closed");
});

});
