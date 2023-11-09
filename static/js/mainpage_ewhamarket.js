document.addEventListener('DOMContentLoaded', function() {
    const userIdInput = document.getElementById('user-id');
    const userIdDisplay = document.getElementById('user-display');
    const userIdSubmit = document.getElementById('user-id-submit');

    userIdSubmit.addEventListener('click', function() {
        const userId = userIdInput.value.trim(); // 앞뒤 공백 제거
        if (userId) { // 입력된 값이 있을 경우에만 출력
            userIdDisplay.textContent = userId + '님!';
        } else {
            userIdDisplay.textContent = '(User ID)'; // 입력값이 없으면 기본 텍스트로
        }
    });
});
