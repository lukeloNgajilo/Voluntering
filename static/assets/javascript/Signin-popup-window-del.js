// show signup popup window
$('#show').on('click', function () {
    $('.center').show();
    $(this).show();
});

$('#close').on('click', function () {
    $('.center').hide();
    $('#show').show();
});


// show signin popup window
$('#show1').on('click', function () {
    $('.center1').show();
    $(this).show();
});

$('#close1').on('click', function () {
    $('.center1').hide();
    $('#show1').show();
});