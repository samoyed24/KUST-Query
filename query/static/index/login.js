document.getElementById("loginform").addEventListener("submit", function(e) {
    e.preventDefault();
    doLogin();
});

let result = document.getElementsByClassName('result');
let hint = document.getElementById('hint');
let button = document.getElementById('submit');

function doLogin() {
    init();
    hint.textContent = '请求中...';
    hint.hidden = false;
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
        const type = response.headers.get('Content-Type');
        if(type=='application/json') return response.json();
        else if(type=='application/octet-stream') return response.blob();
        else {
             alert('500 内部服务器错误, 这可能是一个BUG, 请及时反馈!');
             end_func();
             throw new Error('500');
        }
    })
    .then(resp => {
        end_func();
        if(resp instanceof Blob) {
            const href = URL.createObjectURL(resp);
            download.download = `${USERNAME}_${QUERYTYPE}.xlsx`;
            download.href = href;
            download.text = '点击下载';
            download.hidden = false;
            // link.click();
        }
        else {
            if(resp.errorStatus) alert(resp.errorMsg);
            else {
                switch(resp.type) {
                    case(0):
                    frame_show.hidden = false;
                    let table = document.getElementById('result_table');
                    tr = document.createElement('tr');
                    for (i = 0; i<resp.table_head.length; i++) {
                        td = document.createElement('td');
                        td.innerHTML = resp.table_head[i];
                        tr.appendChild(td);
                    }
                    table.appendChild(tr);
                    for (i = 0; i<resp.table_body.length; i++) {
                        tr = document.createElement('tr');
                        for (j = 0; j<resp.table_body[i].length; j++) {
                            td = document.createElement('td')
                            td.innerHTML = resp.table_body[i][j];
                            tr.appendChild(td);
                        }
                        table.appendChild(tr);
                    }
                    break;
                    case(1):
                    frame_show.hidden = false;
                    
                }
            }
        }
    });
}

function frame_change() {
    // frame = document.getElementById('info_frame');
    // frame.hidden = !frame.hidden;
    $("#info_frame").slideToggle();
}

function init() {
    download.hidden = true;
    frame_show.hidden = true;
    button.disabled = true;
    info_frame.hidden = true;
    result_table.innerHTML = '';
}

function end_func() {
    hint.hidden = true;
    button.disabled = false;
}