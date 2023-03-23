$(document).ready(function () {
    //nav bar
    $('.sidenav').sidenav();
    $('#desktop-links').children('li').clone().each(function () {
        // if(!$(this).hasClass('dropdown-trigger'))
            $('#mobile-links').append(this);
    });
    //collapsible
    $('.collapsible').collapsible();
    //Modals
    $('.modal').modal();
});