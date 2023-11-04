const stars = document.querySelectorAll('.rate input[type="radio"]');
const ratingText = document.getElementById("ratingText");

stars.forEach((star) => {
  star.addEventListener("change", updateRating);
});

function updateRating() {
  const checkedStars = document.querySelectorAll(
    '.rate input[type="radio"]:checked'
  );
  const rating = Array.from(checkedStars).reduce(
    (total, star) => total + parseFloat(star.value),
    0
  );
  ratingText.textContent = `별점: ${rating}`;
}
