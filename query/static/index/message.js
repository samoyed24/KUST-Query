$(document).ready(function () { 
    $('#message_form').submit(function (e) { 
        e.preventDefault();
        submit();
   });

   function submit() {
    if(username.value.length >32 | message.value.length > 500) {
        alert('昵称或留言长度超出限制');
        return;
    }
    formdata = new FormData(message_form);
    fetch('/leave_message', {
        method:'POST',
        body:formdata,
    })
    .then(resp => {
        if(resp.ok) alert('成功!');
        window.location.href="";
    })
   }
 })

 function frame_control() {
    $(".messages_content").slideToggle();
 }