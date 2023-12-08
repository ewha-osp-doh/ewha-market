// function setStatusIcon(iconPath) {
//     $("#status-icon").attr("src", iconPath);
// }

// $(document).ready(function() {
//     function show_status() {
//         $.ajax({
//             type: 'GET',
//             url: '/get_product_status', // 백엔드에서 상태를 가져오는 API 엔드포인트
//             data: {
//                 product_id: productId // 가져올 상품의 아이디
//             },
//             success: function(response) {
//                 var status = response['product-status']; // 응답에서 상태 정보 추출
                
//                 if (status === 'great') {
//                     // 아이콘을 활성화 상태로 변경
//                     setStatusIcon('/static/assets/great_active.svg'); 
//                 } else if (status === 'good'){
//                     // 아이콘을 비활성화 상태로 변경
//                     setStatusIcon('/static/assets/good_active.svg'); 
//                 } else if (status === 'soso'){
//                     // 아이콘을 비활성화 상태로 변경
//                     setStatusIcon('/static/assets/soso_active.svg'); 
//                 }
//             }
//         });
//     }

//     show_status(); // 페이지가 로드될 때 상태를 가져와서 아이콘을 설정
// });


function statusSetting(){
    var status = documnet.getElementByID("statusSet")
    var statusView = documnet.getElementByID("statusView")
    
    if (status === '상') {
         // 아이콘을 활성화 상태로 변경
        statusView.src = "/static/assets/great_active.svg"
      } else if (status === '중'){
       // 아이콘을 비활성화 상태로 변경
       setStatusIcon('/static/assets/good_active.svg'); 
      } else if (status === '하'){
                    // 아이콘을 비활성화 상태로 변경
                    setStatusIcon('/static/assets/soso_active.svg'); 
                }
}