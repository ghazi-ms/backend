$('#buttonEdit').click(function(){

    let total = 0;

    $('#feedList li').each(function(){

        total += parseInt($(this).text());
        $(this).replaceWith('<div><input size = "50" value = "'+ $(this).text() +'"</div>');
        

    })

    $('.button-container').append('<button id = "editBack" onclick = "saveNewInfo()">Save</button>');
    $('#buttonEdit').css("display", "none");
});

function saveNewInfo(){
    
    let total = 0;

    $('input').each(function() {

        total += parseInt($(this).val());
        $(this).replaceWith('<li>' + $(this).val() + '</li>');
        
      });

    $('#editBack').remove();
    $('#buttonEdit').css("display","block");
}