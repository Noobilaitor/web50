document.addEventListener('DOMContentLoaded', function() {
    const urls = ['http://127.0.0.1:8000/register/employer',
     'http://127.0.0.1:8000/register', 'http://127.0.0.1:8000/login', 'http://127.0.0.1:8000/create',
     'http://127.0.0.1:8000/edit','http://127.0.0.1:8000/create_job']
    const search_urls = ['http://127.0.0.1:8000/filter/jobs', 'http://127.0.0.1:8000/filter/search_job']
    html = document.getElementById('html')
    if (urls.includes(window.location.href)) {
        document.body.style.backgroundColor = '#166db1';
        html.style.backgroundColor = '#166db1'
    } else{
        document.body.style.backgroundColor = '#5cb6fd';
        html.style.backgroundColor = '#5cb6fd'
    }
    try{
        cat = document.getElementById("cat")
        cat.addEventListener("change", function(){
            change_cat(cat.value)
    })
    cat.onchange = change_cat(cat.value)
    }catch{}
    try{
        if (search_urls.includes(window.location.href)) {
            search_btn = document.getElementById("search_btn")
            search_btn.addEventListener("click", function(){
            search(true)
            })
        } else {
            search_btn = document.getElementById("search_btn")
            search_btn.addEventListener("click", function(){
            search(false)
            })
        }
    }catch{}
    try{
        recruit_btn = document.getElementById("recruit")
        recruit_btn.addEventListener("click", function(){
            recruit(recruit_btn.dataset.id, true)
    })
    }catch{}
    try{
        acc_btn = document.getElementById("accept")
        acc_btn.addEventListener("click", function(){
            work(acc_btn.dataset.id)
    })
    }catch{}
})

const engineer = ["---","chemical engineering", "computer engineering", "civil engineering", "mechanical engineering"]
const medicine = ["---", "nursing", "psychology", "medical lab", "biochemistry"]
const business = ["---", "marketing", "agribusiness", "accounting", "management"]


function change_cat(value){
    cat = document.getElementById("cat")
    s_cat = document.getElementById("s_cat")
    s_cat.textContent = ''
    //console.log(cat.value)
    if(value == "engineer"){
        for (major in engineer){
            major_e = document.createElement("option")
            major_e.value = engineer[major]
            major_e.textContent = engineer[major]
            s_cat.append(major_e)
        }
    } else if(value == "medicine"){
        for (major in medicine){
            major_e = document.createElement("option")
            major_e.value = medicine[major]
            major_e.textContent = medicine[major]
            s_cat.append(major_e)
        }
    } else if(value == "business"){
        for (major in business){
            major_e = document.createElement("option")
            major_e.value = business[major]
            major_e.textContent = business[major]
            s_cat.append(major_e)
        }
    } else if(value == ""){
        major_e = document.createElement("option")
        major_e.value = ""
        major_e.textContent = "---"
        s_cat.append(major_e)
    }
}

function search(bool){
    search_bar = document.getElementById("search_bar")
    search_bar = search_bar.value
    cat = document.getElementById("cat")
    cat = cat.value
    s_cat = document.getElementById("s_cat")
    s_cat = s_cat.value
    search_bar = [search_bar, cat, s_cat]
    ah = document.getElementById("ah")
    ah.textContent = ''
    if (bool){
        fetch(`search_job/${search_bar}`)
        .then(response =>response.json())
        .then(result =>{
            let i = 0
            for(value in result.name){
                cvs = document.createElement("div")
                cvs.setAttribute('id','singleCV')
                ah.append(cvs)
                per_ski = document.createElement("div")
                per_ski.setAttribute('class','per_ski')
                cvs.append(per_ski)
                person = document.createElement("a")
                person.setAttribute('id','person')
                person.textContent = result.name[i]
                const domain = window.location.origin
                const new_domain = domain + `/user/${result.name[i]}`
                person.setAttribute('href',new_domain)
                per_ski.append(person)
                skill_div = document.createElement("div")
                skill_div.setAttribute('id','skill')
                per_ski.append(skill_div)
                job = document.createElement("h3")
                job.setAttribute('class','skill')
                job.textContent = result.job[i]
                skill_div.append(job)
                skills = result.skill[i].split(",")
                for (skill in skills){
                    skilll = document.createElement("h3")
                    skilll.setAttribute('class','skill')
                    skilll.textContent = skills[skill]
                    skill_div.append(skilll)
                }
                desc = document.createElement("h4")
                desc.setAttribute('id','desc')
                desc.textContent = result.desc[i]
                cvs.append(desc)
                i = i + 1
            }
        })
    } else{
        fetch(`search/${search_bar}`)
        .then(response =>response.json())
        .then(result =>{
            let i = 0
            for(value in result.name){
                cvs = document.createElement("div")
                cvs.setAttribute('id','singleCV')
                ah.append(cvs)
                per_ski = document.createElement("div")
                per_ski.setAttribute('class','per_ski')
                cvs.append(per_ski)
                person = document.createElement("a")
                person.setAttribute('id','person')
                person.textContent = result.name[i]
                const domain = window.location.origin
                const new_domain = domain + `/user/${result.name[i]}`
                person.setAttribute('href',new_domain)
                per_ski.append(person)
                skill_div = document.createElement("div")
                skill_div.setAttribute('id','skill')
                per_ski.append(skill_div)
                job = document.createElement("h3")
                job.setAttribute('class','skill')
                job.textContent = result.job[i]
                skill_div.append(job)
                skills = result.skill[i].split(",")
                for (skill in skills){
                    skilll = document.createElement("h3")
                    skilll.setAttribute('class','skill')
                    skilll.textContent = skills[skill]
                    skill_div.append(skilll)
                }
                desc = document.createElement("h4")
                desc.setAttribute('id','desc')
                desc.textContent = result.desc[i]
                cvs.append(desc)
                i = i + 1
            }
        })
    }
}

function recruit(user, bool){
    fetch(`${user}/recruit`)
    .then(response =>response.json())
    .then(result =>{
        if (result.message === "success"){
            recruit_btn = document.getElementById("recruit")
            recruit_btn.textContent = `Already recruited ${user}`
            console.log(result)
        } else if( result.message === "fail"){
            recruit_btn = document.getElementById("recruit")
            recruit_btn.textContent = `Recruit ${user}`
            console.log(result)
        } else if( result.result === "success"){
            recruit_btn = document.getElementById("recruit")
            recruit_btn.textContent = `Already applied for ${user}'s job`
            console.log(result)
        } else if( result.result === "fail"){
            recruit_btn = document.getElementById("recruit")
            recruit_btn.textContent = `Apply for ${user}'s job`
            console.log(result)
        }
    })
}

function work(user){
    fetch(`notification/${user}`)
    .then(response =>response.json())
    .then(result =>{
        if (result.message === "accepted"){
            div = document.getElementById(user)
            div.remove()
            console.log(result)
        } else if(result.message === "j_accepted"){
            div = document.getElementById(user)
            div.remove()
            console.log(result)
        }
    })
}
