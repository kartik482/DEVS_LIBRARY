
let projectsurl='http://127.0.0.1:8000/api/projects/'

let getprojects=() =>{
    fetch(projectsurl)
        .then(response=>response.json())
        .then(data=>{
            console.log(data)
            buildprojects(data)
        })

}


let buildprojects=(projects)=>{
    projectswrapper=document.querySelector('#projects--wrapper')
    projectswrapper.innerHTML=''
    for (let i = 0; i < projects.length; i++) {
        const project = projects[i];
        // console.log(project)
        let projectcard=`<div class='project--card'>
        <img src='http://127.0.0.1:8000${project.featured_image}'>
        <div>
        <div class='card--header'>
        <h3>${project.title}</h3>
        <strong class='vote--option' data-vote='up' data-project='${project.id}'>&#43;</strong>
        <strong class='vote--option' data-vote='down' data-project='${project.id}'>&#8722;</strong>
        </div>
        <p>${project.vote_ratio} % positive feedbacks</p>
        <p>${project.description.substring(0,150)}</p>
        
        </div> 
    </div>`

    projectswrapper.innerHTML+=projectcard
        
    }
    addvoteevents()
}

let addvoteevents= () => {
    let votebtns=document.querySelectorAll('.vote--option')
    
    for(let i=0;votebtns.length>i;i++){
        votebtns[i].addEventListener('click',(e)=>{
            let token=localStorage.getItem('token')
            let vote=e.target.dataset.vote
            let project=e.target.dataset.project
            // console.log('project:',project,'vote:',vote)
            fetch(`http://127.0.0.1:8000/api/projects/${project}/vote`,{
            method:'POST',
            headers:{
                'content-type':'application/json',
                Authorization:`Bearer ${token}`
            },
            body:JSON.stringify({
                'value':vote
            })
            })
            .then(response=>response.json())
            .then(data=>{
                console.log('success:',data)
                getprojects()
            })

        })
    }

}

getprojects()