window.onload = function(){

new Chart(document.getElementById('rainChart'),{
type:'bar',
data:{
labels:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
datasets:[{
data:rainfallData,
backgroundColor:'blue'
}]
}
});

}