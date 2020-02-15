function f1(e) {
    e.parentNode.parentNode.removeChild(e.parentNode)
    $( "#removedfood").append('<li class="food_list output"><input value="'+ e.parentNode.innerText + '" name="removed_foods" style="display:none;">' + e.parentNode.innerText + '</input><a href="#" onclick="parentNode.parentNode.removeChild(parentNode)"> <i class="fa fa-minus-circle" aria-hidden="true"></i></a></li>');

}

function remove_all(){
	$('#removedfood').empty();
}

function remove_all_selected(){
	$('#selectedfood').empty();
}

function add_mfp(e){
	
}