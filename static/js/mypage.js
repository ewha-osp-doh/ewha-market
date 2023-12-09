function withdrawlCheck(){
    
    var answer = confirm('정말 회원 탈퇴를 진행하시겠습니까?');
    
    if (answer){
        window.location.href = "/withdrawal";
    }
    else{
        alert("탈퇴 진행이 취소되었습니다.");
    }
    
}
