$(document).ready(function(){

	// Topmenu Dropdown
	var dropdownButton = $('.dd-button');
	dropdownButton.on('click',function(){
		$(this).parent().toggleClass('active');
	});

	var editFormButton = $('#editform-activer');
	editFormButton.click(function(){
		$('.originalprofile').hide();
		$('.inline-edit').show();
	});

})