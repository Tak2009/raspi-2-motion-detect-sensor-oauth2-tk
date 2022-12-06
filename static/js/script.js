console.log("test")

const media = ["https://media.giphy.com/media/H5POhvdgk9kcYyTToA/giphy.gif", "https://media.giphy.com/media/QXh9XnIJetPi0/giphy.gif", "https://media.giphy.com/media/oae3Nv1fd0CYM/giphy.gif"];

let count = -1;

function mediaChange() {
  count++;
  if (count == media.length) count = 0;
  document.getElementById("media").src = media[count];
  setTimeout("mediaChange()", 3000);
  //~ console.log(count)
}

mediaChange();


