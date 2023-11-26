document.getElementById("loginform").addEventListener("submit", function(e) {
    e.preventDefault();
    doLogin();
});

function doLogin() {
    button = document.getElementById("submit");
    button.disabled = true;
    form = document.getElementById("loginform");
    const url = form.getAttribute('action');
    let formdata = new FormData(form);
    const USERNAME = formdata.get('username')
    const QUERYTYPE = formdata.get('queryType')
    fetch(url, {
        method:'POST',
        body:formdata
    })
    .then(response => {
        if(!response.ok) {
            alert('认证失败, 用户名或密码错误!');
            button.disabled = false;
            throw new Error('Failed');
        }
        return response.blob();
    })
    .then(blob => {
        const href = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.download = `${USERNAME}_${QUERYTYPE}.xlsx`;
        link.href = href;
        link.click();
        button.disabled = false;
        document.body.removeChild(link);

    });
}