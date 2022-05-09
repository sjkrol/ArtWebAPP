function openImg(id){
  var image = document.getElementById(id);
  var source = image.src;
  const image_name = source.substring(source.lastIndexOf('/') + 1);

  console.log("image_name");

  const request = new XMLHttpRequest();
  request.open('GET', `/gallery/painting/${JSON.stringify(image_name)}`);

  request.onreadystatechange = function() {
      if(request.readyState == XMLHttpRequest.DONE && request.status == 200) {
        window.location.href = "/gallery/painting";
      }
  }

  request.send();
}

function returnToGallery(){
  window.location.href = "/gallery";
}

function beginExperiment(){
  window.location.href = "/experiment/consent";
}

function goToDemographic(){

  c1 = document.getElementById("C1").checked;
  c2 = document.getElementById("C2").checked;
  c3 = document.getElementById("C3").checked;
  c4 = document.getElementById("C4").checked;
  c5 = document.getElementById("C5").checked;
  c6 = document.getElementById("C6").checked;

  if(c1 && c2 && c3 && c4 && c5 && c6){
    window.location.href = "/experiment/demographic";
  } else{
    $('#myModal').modal('show');
    console.log("stop right there criminal scum");
  }

}

function returnToExplanatory(){
  window.location.href = "/experiment";
}

function returnToConsent(){
  window.location.href = "/experiment/consent";
}

function sendDemographicInfo(){
  gender = document.getElementById("gender").value;
  other = document.getElementById("other_gender").value;
  age = document.getElementById("age").value;
  lowvision = document.getElementById("lowvision").value;

  if(gender != "Other" || (gender == "Other" && other != '')){

      console.log("Move along, no issues here")
      const request = new XMLHttpRequest();
      // sender = JSON.stringify([gender, other, age, lowvision]);
      sender = JSON.stringify({"gender" : gender, "other" : other, "age" : age, "lowvision" : lowvision});
      request.open('POST', '/experiment/demographic');

      request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE && request.status == 200) {
          window.location.href = "/experiment/questions";
        }
    }

    request.send(sender);

  } else {
    $('#demographic_modal').modal('show');
    console.log("Must specify other gender");
  }

}

function save_responses(){

  // retrieve data
  pleasant = document.querySelector('input[name="pleasant"]:checked');
  representative = document.querySelector('input[name="representative"]:checked');

  if(pleasant === null || representative === null){
    $('#questionsModal').modal('show');
  } else {
    const request = new XMLHttpRequest();
    sender = JSON.stringify({"pleasant" : pleasant.value, "representative" : representative.value});
    request.open('POST', '/experiment/questions');
    
    request.onreadystatechange = function() {
      if(request.readyState == XMLHttpRequest.DONE && request.status == 200) {
        window.location.href = "/experiment/questions";
      }
    }
    request.send(sender);
  }
}

function returnToIndex(){
  window.location.href = "/";
}

function leaveExperimentModal(){
  $('#leaveExperimentModal').modal('show');
}

function leaveExperiment(){
  window.location.href = "/gallery";
}