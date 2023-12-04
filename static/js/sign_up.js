function checkDuplicate() {
  // [TODO] 아이디 중복 확인 로직 구현
  // 중복 확인 버튼 클릭 시 호출됩니다.
  // 중복이 아닌 경우 아이디 사용 가능 메시지를 표시하고,
  // 중복일 경우 아이디가 이미 사용 중이라고 알려줍니다.
  var duplicateCheck = document.getElementById("duplicateCheck");
  duplicateCheck.setAttribute("value", "confirmed");
  document.getElementById("check-id").style.visibility = "hidden";
}

function validateForm() {
  var id = document.getElementById("id").value;
  var password = document.getElementById("password").value;
  var confirmPassword = document.getElementById("confirmPassword").value;
  var email = document.getElementById("email").value;

  if (id === "") {
    document.getElementById("check-id").style.visibility = "visible";
    return false;
  }
  if (password === "" || password.length < 10) {
    document.getElementById("check-pw").style.visibility = "visible";
    return false;
  }
  if (confirmPassword === "") {
    document.getElementById("check-pw-re").innerHTML = "*10자 이상 입력";
    document.getElementById("check-pw-re").style.visibility = "visible";
    return false;
  }
  if (email === "") {
    document.getElementById("check-pw-re").style.visibility = "visible";
    return false;
  }

  if (password !== confirmPassword) {
    var passwordCheck = document.getElementById("check-pw-re");
    passwordCheck.innerHTML = "*비밀번호가 일치하지 않습니다";
    passwordCheck.style.visibility = "visible";
    return false;
  }

  // 이메일 형식 검증
  var emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailPattern.test(email)) {
    document.getElementById("check-email").style.visibility = "visible";
    return false;
  }

  // 중복 확인 여부를 검증
  var duplicateCheck = document.getElementById("duplicateCheck").value;
  if (duplicateCheck !== "confirmed") {
    document.getElementById("check-id").style.visibility = "visible";
    return false;
  }

  return true;
}

function checkInputs() {
  var id = document.getElementById("id").value;
  var password = document.getElementById("password").value;
  var confirmPassword = document.getElementById("confirmPassword").value;
  var email = document.getElementById("email").value;

  var submitBtn = document.getElementById("submitBtn");

  if (
    id !== "" &&
    password.length !== "" &&
    confirmPassword !== "" &&
    email !== ""
  ) {
    submitBtn.removeAttribute("disabled");
  } else {
    submitBtn.setAttribute("disabled", true);
  }
}

var inputs = document.querySelectorAll(
  "input[type='text'], input[type='password'], input[type='email']"
);
inputs.forEach(function (input) {
  input.addEventListener("input", checkInputs);
});
