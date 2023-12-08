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
const ratingText = document.getElementById("ratingTxt");

stars.forEach((star, index) => {
  star.addEventListener("change", () => updateRating(index));
});

function updateRating(checkedIndex) {
  stars.forEach((star, index) => {
    const starLabel = star.nextElementSibling;
    if (index <= checkedIndex) {
      starLabel.classList.add("active");
    } else {
      starLabel.classList.remove("active");
    }
  });

  ratingText.innerHTML = `별점: ${checkedIndex + 1}`;
}

// 제출 버튼 활성화
function validateForm() {
  var productImage = document.getElementById("productImage").value;
  var reviewTitle = document.getElementById("reviewTitle").value;
  var productName = document.getElementById("productName").value;
  var condition = document.querySelector('input[name="rating"]:checked');

  var submitBtn = document.getElementById("submitBtn");

  if (
    productImage !== "" &&
    reviewTitle !== "" &&
    productName !== "" &&
    condition !== null
  ) {
    submitBtn.removeAttribute("disabled");
  } else {
    submitBtn.setAttribute("disabled", true);
  }

  return true;
}

var inputs = document.querySelectorAll(
  "input[type='text'], input[type='file'], input[type='radio']"
);
inputs.forEach(function (input) {
  input.addEventListener("input", validateForm);
});
