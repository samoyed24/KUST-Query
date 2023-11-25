document.getElementById("loginform").addEventListener("submit", function(e) {
    e.preventDefault();
    checkLogin().then(result => {
        if (result) {
            document.getElementById("myForm").dispatchEvent(new Event('submit'));
        } else {
            console.log("登录失败，不允许提交表单");
            e.preventDefault();
        }
    });
});

function checkLogin() {
    const URL = '/checkLogin';
    let formdata = new FormData(document.getElementById('loginform'));
    return fetch(URL, {
        method:'POST',
        body:formdata
    })
    .then(response => {
        if (!response.ok) return false;
        else return true;
    });
}