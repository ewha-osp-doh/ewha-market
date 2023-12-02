function uploadImage() {
  document.getElementById("productImage").click();
}

function checkFile() {
  console.log("파일 체크는 돼요");
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

function formatPrice() {
  var priceInput = document.getElementById("productPrice");
  var price = priceInput.value.replace(/,/g, "");
  if (!isNaN(price)) {
    priceInput.value = parseFloat(price).toLocaleString();
  }
}

function changeStatus(status) {
  var greatImg = document.getElementById("greatImg");
  var goodImg = document.getElementById("goodImg");
  var sosoImg = document.getElementById("sosoImg");

  if (status === "great") {
    greatImg.src = "../static/assets/great_active.svg";
    goodImg.src = "../static/assets/good_inactive.svg";
    sosoImg.src = "../static/assets/soso_inactive.svg";
  } else if (status === "good") {
    greatImg.src = "../static/assets/great_inactive.svg";
    goodImg.src = "../static/assets/good_active.svg";
    sosoImg.src = "../static/assets/soso_inactive.svg";
  } else if (status === "soso") {
    greatImg.src = "../static/assets/great_inactive.svg";
    goodImg.src = "../static/assets/good_inactive.svg";
    sosoImg.src = "../static/assets/soso_active.svg";
  }
}

function validateForm() {
  var sellerId = document.getElementById("sellerId").value;
  var productName = document.getElementById("productName").value;
  var productImage = document.getElementById("productImage").value;
  var productPrice = document.getElementById("productPrice").value;
  var sellerLocation = document.getElementById("currentLocation").value;
  var productDescription = document.getElementById("productDescription").value;

  var condition = document.querySelector(
    'input[name="condition"]:checked'
  ).value;

  var submitBtn = document.getElementById("submitBtn");

  if (
    sellerId == "" ||
    productName == "" ||
    productImage == "" ||
    productPrice == "" ||
    sellerLocation == "" ||
    productDescription == "" ||
    condition == null
  ) {
    // alert(
    //   `${sellerId} ${productName} ${productImage} ${productPrice} ${sellerLocation} ${productDescription} ${condition}`
    // );
    submitBtn.setAttribute("disabled", true);
  } else {
    submitBtn.removeAttribute("disabled");
  }

  return true;
}

var inputs = document.querySelectorAll(
  "input[type='text'], input[type='file'], input[type='radio']"
);
inputs.forEach(function (input) {
  input.addEventListener("input", validateForm);
});
