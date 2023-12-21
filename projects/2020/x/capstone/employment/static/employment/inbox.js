document.addEventListener('DOMContentLoaded', function() {
    const urls = ['http://127.0.0.1:8000/register/employer',
     'http://127.0.0.1:8000/register', 'http://127.0.0.1:8000/login', 'http://127.0.0.1:8000/create']
    html = document.getElementById('html')
    if (urls.includes(window.location.href)) {
        document.body.style.backgroundColor = '#166db1';
        html.style.backgroundColor = '#166db1'
    } else{
        document.body.style.backgroundColor = '#5cb6fd';
        html.style.backgroundColor = '#5cb6fd'
    }
})
