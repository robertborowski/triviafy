const drillDownOne = document.getElementsByClassName('drill-down')[0];
const drillDownTwo = document.getElementsByClassName('drill-down')[1];
const drillDownThree = document.getElementsByClassName('drill-down')[2];

const subListItemsOne = document.getElementsByClassName('sub-list-items')[0];
const subListItemsTwo = document.getElementsByClassName('sub-list-items')[1];
const subListItemsThree = document.getElementsByClassName('sub-list-items')[2];



drillDownOne.addEventListener('click', () => {
  subListItemsOne.classList.toggle('active');
  subListItemsTwo.classList.remove('active');
  subListItemsThree.classList.remove('active');
})
drillDownTwo.addEventListener('click', () => {
  subListItemsOne.classList.remove('active');
  subListItemsTwo.classList.toggle('active');
  subListItemsThree.classList.remove('active');
})
drillDownThree.addEventListener('click', () => {
  subListItemsOne.classList.remove('active');
  subListItemsTwo.classList.remove('active');
  subListItemsThree.classList.toggle('active');
})