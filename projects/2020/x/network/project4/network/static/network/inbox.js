document.addEventListener('DOMContentLoaded', function() {
    btns = document.getElementsByClassName('edit_btn')
    Array.prototype.forEach.call(btns, function(btn) {
        btn.addEventListener('click',  function() {
            edit(btn)
        })
    });
    texts = document.getElementsByClassName('text')
    Array.prototype.forEach.call(texts, function(text) {
        text.style.display = "none"
    })
    save_btns = document.getElementsByClassName('save_btn')
    Array.prototype.forEach.call(save_btns, function(save_btn) {
        save_btn.style.display = "none"
    })
    /*likes_btn = document.getElementsByClassName('likes_num')
    Array.prototype.forEach.call(likes_btn, function(like_btn) {
        like_btn.addEventListener('click', function(){
            like(like_btn)
        })
    })*/
    images = document.getElementsByClassName('image')
    Array.prototype.forEach.call(images, function(image) {
        image.addEventListener('click', function(){
            like(image)
        })
    })
})

function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

/*function like(post_id){
    fetch(`like/${post_id.dataset.id}`)
    .then(response =>response.json())
    .then(result =>{
        like_btn = document.getElementById(`likes${post_id.dataset.id}`)
        image = document.getElementById(`image${post_id.dataset.id}`)
        if (result.message == "liked"){
            image.src = "{% static 'like.png' %}"
        } else{
            image.src = "{% static 'unlike.png' %}"
        }
        like_btn.textContent = `${result.like_num}`
    })
}*/

function save(post_id){
    const content = document.getElementById(`text${post_id.dataset.id}`).value
    fetch(`edit/${post_id.dataset.id}`, {
        method: "POST",
            headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
            body: JSON.stringify({
                content: content
            })
        })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        text_area = document.getElementById(`text${post_id.dataset.id}`)
        text_area.style.display = "none"
        post = document.getElementById(`post${post_id.dataset.id}`)
        post.style.display = "block"
        post.textContent = result.data
        save_btn = document.getElementById(`save_btn${post_id.dataset.id}`)
        save_btn.style.display = "none"
        btn = document.getElementById(`edit_btn${post_id.dataset.id}`)
        btn.style.display = "block"
    })
    //console.log(post_id.dataset.id)
}

function edit(btn) {
    post = document.getElementById(`post${btn.dataset.id}`)
    post.style.display = "none"
    let text_area = document.getElementById(`text${btn.dataset.id}`)
    text_area.textContent = post.textContent
    text_area.style.display = 'block'
    btn.style.display = "none"
    let save_btn = document.getElementById(`save_btn${btn.dataset.id}`)
    save_btn.style.display = 'block'
    save_btn.addEventListener('click',() =>save(save_btn))
    console.log(btn)
}
