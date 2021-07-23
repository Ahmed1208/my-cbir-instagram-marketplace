// for(let i=1;i<3;i++){
//     let dropContainer = document.getElementById(`dropContainer${i}`)
//     let fileInput = document.getElementById(`fileInput${i}`)
//     dropContainer.ondragover = dropContainer.ondragenter = e => {
//         dropContainer.style.border = "2px dashed #47f"
//         e.preventDefault();
//     }
//         // console.log(Array(...e.dataTransfer.files).length > 1)
//         // if(Array(...e.dataTransfer.files).length > 1)
//         // dropContainer.style.border = "2px dashed #f74"
//         // else
//         // dropContainer.style.border = "2px dashed #4f7"
//     dropContainer.ondragleave = e => {
//         dropContainer.style.border = "2px dashed #aaa"
//         e.preventDefault();
//     }
//     dropContainer.onclick = () => fileInput.click();
//     let fileSys = []
//     dropContainer.ondrop = function(evt) {
//         fileInput.files = evt.dataTransfer.files;
//         const dT = new DataTransfer();
//         let newFileSys = Array(...evt.dataTransfer.files)
//         fileSys = fileSys.concat(newFileSys.filter(e => {
//             return fileSys.find(el => el.name == e.name) == undefined;
//         }));
//         if(fileSys.length > 1){
//             dropContainer.style.border = "2px dashed #f74"
//             console.log(dropContainer.childNodes[0])
//             console.log(dropContainer.chil)
//             dropContainer.style.color = "#f74"
//             document.querySelector(".fa-image").style.color = "#f74"
//             dropContainer.appendChild(document.createElement("p")).appendChild(document.createTextNode("multiple files are not allowed"))
//         }
//         else
//         dropContainer.style.border = "2px dashed #4f7"
//         console.log(fileSys)
//         fileSys.forEach(e => {
//                 dT.items.add(e);
//         })
//         fileInput.files = dT.files;
//         evt.preventDefault();
//         let parent = document.querySelector("#fileSystem");
//         while (parent.firstChild) 
//             parent.firstChild.remove();
//             fileSys.map(e => {
//                 let li = document.createElement("li");
//                 Object.assign(
//                     Object.assign(document.querySelector("#fileSystem").appendChild(li),
//                     {"className":"list-group-item"}).appendChild(document.createElement("input")),
//                     {"className":"form-check-input me-1","type":"checkbox","name":"filesPicked","value":e.name }
//                     )
//                     li.appendChild(document.createTextNode(e.name))
//                     if(e.type.split("/")[0] == "image")
//                         Object.assign(li.appendChild(document.createElement("i")),
//                         {"className":"fas fa-images mx-4"})
//             })
//         console.log(fileInput.files)
//     }
// }


if(document.querySelector(".splideAll"))
    new Splide( '.splideAll' ,{
        perPage: 12,
        autoWidth: true,
    }).mount();
if(document.querySelector(".splideQuery"))
    new Splide( '.splideQuery' ,{
        perPage: 12,
        autoWidth: true,
    }).mount();

if(document.querySelector(".container"))
    var mixer = mixitup(document.querySelector(".container"), {
        animation: {
            effects: 'fade scale stagger(50ms)',
            duration: 300
        }
    });


document.querySelector(".selectedClusterType").onchange = e => {
    // console.log(document.querySelector('.selectedClusterType').value)

    // 
    // 
    // at least on of 2 checked (not completed yet)
    // 
    // 
}

document.querySelector("#selectedClusterType1").onchange = e => {
    (e.currentTarget.checked)?
    document.querySelector("[name=kmeanClusterCount]").removeAttribute("disabled")
    :document.querySelector("[name=kmeanClusterCount]").setAttribute("disabled","true")
}