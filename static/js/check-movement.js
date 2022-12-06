
let count = -1;
let media_hash  = {
	"no_mice":["https://media.giphy.com/media/21I7j6xSyuTHUNiRdp/giphy.gif", "https://media.giphy.com/media/DeobURBiyoMRFO4GqD/giphy.gif", "https://media.giphy.com/media/29JM2v753GbY8SG9QG/giphy.gif" ],
	"1_mice": ["https://media.giphy.com/media/WpaVhEcp3Qo2TjwyI1/giphy.gif", "https://media.giphy.com/media/9Fticsj7froxbpd5Sg/giphy.gif", "https://media.giphy.com/media/jivGITd768psP80B2i/giphy.gif"],
	'too_many':["https://media.giphy.com/media/4TmLKfeYOuO2c/giphy.gif", "https://media.giphy.com/media/jTfQtwVaqQaVh4ePJn/giphy.gif", "https://media.giphy.com/media/xT1XGEmKXhLMx8ZT4Q/giphy.gif"]}
let media 

const sleep = (ms) => {
	return new Promise(resolve => setTimeout(resolve, ms));
	}

const setMedia = async (num) => {
		
	if (num == 0) {
		console.log(media)
		return media = media_hash['no_mice']
	}else if (num == 1){
		console.log(media)
		return media = media_hash['1_mice']
		
	}else{
		console.log(media)
		return media = media_hash['too_many']
	}
	await sleep (1000);
}

const changeMedia= () => {
  count++;
  if (count == media.length) count = 0;
  document.getElementById("media").src = media[count];
  setTimeout("changeMedia()", 3000);
 }
