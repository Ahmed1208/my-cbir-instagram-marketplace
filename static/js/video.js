// Dropzone.options.formId = {
//     // autoProcessQueue: false,
//     addRemoveLinks: true,
//     maxFiles: 1,
//     // paramName: "file",
    
//     init: function (e) {
        
//         var myDropzone = this;
//         console.log(myDropzone)
//         console.log("k")
//         // document.querySelector("#sub").addEventListener("click", function() {
//         //     myDropzone.processQueue(); 
//         //     alert("processing")
//         // });
//         // this.on("sending", function() {
//         //     $("#formId").submit()
//         // });

//     },
//     // accept: function(file, done) {
//     //     if (file.name == "justinbieber.jpg") {
//     //       done("Naha, you don't.");
//     //     }
//     //     else { done(); }
//     //   }
// };









Dropzone.options.formId = {
    autoProcessQueue: false,
        addRemoveLinks: true,
        maxFiles: 1,

    init: function()
    {
      let myDropzone = this;
      document.getElementById('sub').addEventListener("click", function (e) {
          e.preventDefault();
          myDropzone.processQueue();
      });

      this.on('sending', function(file, xhr, formData) 
      {
          new FormData(document.getElementById('formId')).append("file", document.getElementById('sub').value);
      });
    }
  };