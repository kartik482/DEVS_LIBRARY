let tags = document.getElementsByClassName('project-tag')
for (let i = 0; i < tags.length; i++) {
    tags[i].addEventListener('click', (e) => {
        tagId = e.target.dataset.tag
        projectId = e.target.dataset.project
        // console.log(tagId)
        fetch('http://127.0.0.1:8000/api/remove-tag/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'project':projectId, 'tag': tagId })
        })
        .then(response=>response.json())
        .then(data=>{
            e.target.remove()
        })

        

    })
}