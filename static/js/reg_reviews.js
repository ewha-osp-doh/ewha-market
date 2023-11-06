// 리뷰 이미지 업로드
function uploadImage() {
  document.getElementById("productImage").click();
}

function checkFile() {
  var fileInput = document.getElementById("productImage");
  var file = fileInput.files[0];

  if (file) {
    var fileType = file.type;
    var fileSize = file.size;

    if (fileType !== "image/jpeg" && fileType !== "image/png") {
      alert("이미지 파일은 jpg 또는 png 형식이어야 합니다.");
      fileInput.value = "";
    } else if (fileSize > 5000000) {
      // 5MB
      alert("이미지 파일의 크기는 5MB 이하여야 합니다.");
      fileInput.value = "";
    } else {
      var imgPreview = document.getElementById("imagePreview");
      var defaultIcon = document.getElementById("defaultIcon");
      imgPreview.src = URL.createObjectURL(file);
      defaultIcon.style = "display: none";
      imgPreview.style = "display:block";
    }
  }
}

// 별점
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
