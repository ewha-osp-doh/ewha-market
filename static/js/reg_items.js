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
      imgPreview.src = URL.createObjectURL(file);
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

function getCurrentLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;
      // [TODO] 현재 위치를 동 단위로 표시하는 로직 작성
      document.getElementById("currentLocation").innerHTML =
        latitude + "," + longitude;
    });
  }
}

function validateForm() {
  var sellerId = document.getElementById("sellerId").value;
  var productName = document.getElementById("productName").value;
  var productImage = document.getElementById("productImage").value;
  var productPrice = document.getElementById("productPrice").value;
  var condition = document.querySelector('input[name="condition"]:checked');
  var productDescription = document.getElementById("productDescription").value;

  if (
    !sellerId ||
    !productName ||
    !productImage ||
    !productPrice ||
    !condition ||
    !productDescription
  ) {
    alert("모든 정보를 입력해주세요.");
    return false;
  }

  return true;
}
