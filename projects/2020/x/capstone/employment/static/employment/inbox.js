document.addEventListener('DOMContentLoaded', function() {
    const urls = ['http://127.0.0.1:8000/register/employer',
     'http://127.0.0.1:8000/register', 'http://127.0.0.1:8000/login', 'http://127.0.0.1:8000/create',
     'http://127.0.0.1:8000/edit']
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
        search_btn = document.getElementById("search_btn")
        search_btn.addEventListener("click", function(){
            search()
    })
    }catch{}
})

const engineer = ["---","chemical engineering", "computer engineering", "civil engineering", "mechanical engineering"]
const medicine = ["---", "nursing", "psychology", "medical lab", "biochemistry"]
const business = ["---", "marketing", "agribusiness", "accounting", "management"]


function change_cat(value){
    s_cat = document.getElementById("s_cat")
    s_cat.textContent = ''
    if(value == "engineer"){
        for (major in engineer){
            major_e = document.createElement("option")
            major_e.value = engineer[major]
            major_e.textContent = engineer[major]
            s_cat.append(major_e)
            console.log(s_cat)
        }
    } else if(value == "medicine"){
        for (major in medicine){
            major_e = document.createElement("option")
            major_e.value = medicine[major]
            major_e.textContent = medicine[major]
            s_cat.append(major_e)
            console.log(s_cat)
        }
    } else if(value == "business"){
        for (major in business){
            major_e = document.createElement("option")
            major_e.value = business[major]
            major_e.textContent = business[major]
            s_cat.append(major_e)
            console.log(s_cat)
        }
    } else if(value == ""){
        major_e = document.createElement("option")
        major_e.value = ""
        major_e.textContent = "---"
        s_cat.append(major_e)
    }
}

function search(){
    search_bar = document.getElementById("search_bar")
    search_bar = search_bar.value
    cat = document.getElementById("cat")
    cat = cat.value
    s_cat = document.getElementById("s_cat")
    s_cat = s_cat.value
    search_bar = [search_bar, cat, s_cat]
    ah = document.getElementById("ah")
    ah.textContent = ''
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
            person = document.createElement("h1")
            person.setAttribute('id','person')
            person.textContent = result.name[i]
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
