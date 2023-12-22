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
    cat = document.getElementById("cat")
    cat.addEventListener("change", function(){
        change_cat(cat.value)
    })
    cat.onchange = change_cat(cat.value)
})

const engineer = ["chemical engineering", "computer engineering", "civil engineering", "mechanical engineering"]
const medicine = ["nursing", "psychology", "medical lab", "biochemistry"]
const business = ["marketing", "agribusiness", "accounting", "management"]
//cat.onchange = change_cat(cat.value)


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
    }
}
