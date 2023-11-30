document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email').style.display = 'none';

  // Clear out composition fields
}

function archive(is_archived, email_id) {
  if (is_archived){
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    .then(() => {
      load_mailbox('inbox');
    })
  } else{
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
        
      })
    })
    .then(() => {
      load_mailbox('inbox');
    })
  }
  
  
}

function reply(sender, subject, body, timestamp){
  recipientss = document.querySelector("#compose-recipients")
  recipientss.value = sender
  check = subject.slice(0,3)
  if (check == 'Re:'){
    document.querySelector("#compose-subject").defaultValue = `${subject}`
  } else {
    document.querySelector("#compose-subject").defaultValue = `Re: ${subject}`
  }
  document.querySelector("#compose-body").innerHTML =`On ${timestamp} ${sender} wrote:" ${body}"`
  compose_email()
}

function load_email(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#email_sender').innerHTML = `from: ${email.sender}`
    document.querySelector('#email_recipient').innerHTML = `to: ${email.recipients}`
    document.querySelector('#email_timestamp').innerHTML = `${email.timestamp}`
    document.querySelector('#email_subject').innerHTML = `${email.subject}`
    document.querySelector('#email_body').innerHTML = `${email.body}`
    archive_btn = document.querySelector('#archive_btn')
    reply_btn = document.querySelector('#reply_btn')
    user_emaill = document.querySelector("#user_email").innerHTML
    
    if (email.archived){
      archive_btn.removeAttribute("hidden")
      archive_btn.innerHTML = 'Unarchive'
      archive_btn.addEventListener('click', () => archive(true, email_id));

    } else if(email.sender == user_emaill){
      archive_btn.setAttribute("hidden","hidden")
    } else {
      archive_btn.removeAttribute("hidden")
      archive_btn.innerHTML = 'Archive'
      archive_btn.addEventListener('click', () => archive(false, email_id))
    }

    if (email.sender == user_emaill){
      reply_btn.setAttribute("hidden","hidden")
    } else {
      reply_btn.removeAttribute("hidden")
      reply_btn.addEventListener('click', () => reply(email.sender, email.subject, email.body, email.timestamp))
    }
    //document.querySelector('#single-email').append(element) 
    })
    
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email').style.display = 'block';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email').style.display = 'none';
  parent_div = document.querySelector("#parent_div")
  email_list = []
  

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails)
    emails.forEach(email => {
      console.log(email)
      
      let element = document.createElement('div')
      element.setAttribute('id', 'element')
      element.innerHTML = `
      <h5>${email.sender}</h5>
      <h6>${email.subject}</h6>
      <h6>${email.timestamp}</h6>`
      element.style.marginBottom = '5px'
      element.style.border = 'solid'
      element.style.borderRadius = "20px"
      element.style.borderColor = 'grey'
      element.style.paddingLeft = '7px'
      if (email.read == true) {
        element.style.backgroundColor = "#bdbbbb"
        console.log(email.read)
      if (email_list.includes(email.id)){
        console.log('email already there')
      } else{
        document.querySelector("#emails-view").append(element)
        //parent_div.append(element)
        element.addEventListener('click',() => load_email(email.id))
        email_list.push(email.id)
        console.log(email_list)
      }
      }
    }); 
  })

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function send_email(event) {
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value
  const subject = document.querySelector('#compose-subject').value
  const body = document.querySelector('#compose-body').value
  user_emaill = document.querySelector("#user_email").innerHTML
  if (recipients == user_emaill) {
    alert("You can't send yourself an email!")
  } else {
      document.querySelector('#compose-recipients').value = '';
      document.querySelector('#compose-subject').value = '';
      document.querySelector('#compose-body').value = '';
      fetch("/emails", {
        method: 'POST',
        body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
        })
      })
      .then(response => response.json())
      .then(result => {
        result = result["error"]
        reall = `User with email ${recipients} does not exist.`
        if (result == reall){
          alert(result)
        } else {
          load_mailbox('sent')
        }
      })
  }
}
