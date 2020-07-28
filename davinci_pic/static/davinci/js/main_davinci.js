$(document).ready(function(){

  window.addEventListener("resize", displayWindowSize);

 $('#username-signin').click(function(){

   $('#password-signin').removeClass('signin-clicked');
   $(this).addClass('signin-clicked');

 });

 $('#password-signin').click(function(){


   $('#username-signin').removeClass('signin-clicked');
   $(this).addClass('signin-clicked');

 });

 $('#username-signin').on('keydown',function(event){

       if(event.which == 13){
         event.preventDefault();
         $( "#password-signin" ).trigger( "click" );
         $( "#password-signin" ).focus();
       }


 });
 $('#password-signin').on('keydown',function(event){

       if(event.which == 13){
         event.preventDefault();
         $( "#submit" ).trigger( "click" );
         $( "#submit" ).focus();
       }



 });

  $('.signin-form').closest('form').find("input[type=text], input[type=password]").val("");

//  $('.submit-signinstopped').click(function(){
//    var user = $('#username-signin').val();
//    var pass = $('#password-signin').val();
//    var csrftoken = Cookies.get('csrftoken');


//    $.ajax({
//       url: '/davinci/sign_in/',
//       type: 'POST',
//       data: {
//         'username': user,
//         'password': pass,
//       },
//       headers: { "X-CSRFToken": csrftoken },
//       dataType: 'json',
//       success: function(data) {
//                 if(data.status== 'true'){

//                   window.location.href = window.location.origin+"/davinci/gallery/"+data.id;
//                 }
//                 else{
//                   alert('failed');

//                 }
//       }


//    });




// });

 $('.register-link').click(function(){
   $('.div-reg').addClass("div-display");
   $('body').addClass("body-dark");


 });

 $('#username-register').removeAttr('required');
 $('#password-register').removeAttr('required');
 $('#email-register').removeAttr('required');

$('#close-register').click(function(){

  $('.div-reg').removeClass("div-display");
  $('body').removeClass("body-dark");
  $('.register-form').removeClass('div-hidden');
  $('.thankyou').addClass('div-hidden');
  $('.register-form').closest('form').find("input[type=text], input[type=password],input[type=email]").val("");
  location.reload();

});



$('#submit-register').click(function(){

  var csrftoken = Cookies.get('csrftoken');


  $.ajax({
     url: '/davinci/',
     type: 'POST',
     data: $('.register-form').serialize(),
     headers: { "X-CSRFToken": csrftoken },
     dataType: 'json',
     success: function(data) {
               if(data.register == true){
                 $('.register-form').addClass('div-hidden');
                 $('.thankyou').removeClass('div-hidden');
               }
               else{
                
                
                 document.getElementById('form-error').innerHTML = data.error
               }
     }


  });





});


//waypoints

$('.section-features').waypoint(function(direction){
   if(direction == "down"){
     $('.js--features').addClass('animated fadeIn');
     $('#features-line').addClass('section-line-animate');
     $('.features-icon').addClass('animated flip');
   }
   else{
     $('.js--features').removeClass('animated fadeIn');
     $('#features-line').removeClass('section-line-animate');
     $('.features-icon').removeClass('animated flip');
   }

},{
  offset: '500px;'
});

$('.head-link').click(function(){

  $('html,body').animate({scrollTop: $('.section-head').offset().top},1000);


});
$('.features-link').click(function(){

  $('html,body').animate({scrollTop: $('.section-features').offset().top},1000);


});
$('.signin-link').click(function(){

  $('html,body').animate({scrollTop: $('.section-signin').offset().top},1000);


});

function displayWindowSize(){

if($(window).width() > 767)
{
   $('.nav-toggle').removeClass('div-display');
}

}

$('#toggle-button').click(function(){
  console.log($(this).val());
   var set =  $(this).val();
  if(set == 0){
    $('.nav-toggle').addClass('div-display');
    $(this).val(1);
  }
  else{
    $('.nav-toggle').removeClass('div-display');
     $(this).val(0);
  }

});

});
