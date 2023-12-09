function statusSetting(){
    var status = documnet.getElementById("statusSet");
    var statusView = documnet.getElementById("statusView");
    console.log(status.innerText);
    
    if (status === '상') {
         // 아이콘을 활성화 상태로 변경
            statusView.src = "../static/assets/great_active.svg";
            
      } else if (status === '중'){
       // 아이콘을 비활성화 상태로 변경
           statusView.src = "../static/assets/good_active.svg";
      } else if (status === '하'){
      // 아이콘을 비활성화 상태로 변경
            statusView.src = "../static/assets/soso_active.svg";
      }
}

statusSetting();