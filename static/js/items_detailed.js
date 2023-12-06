$(document).ready(
    function show_status() {
      $.ajax({
        type: 'GET',
        url: '/get_product_status', // 백엔드에서 상태를 가져오는 API 엔드포인트
        data: {
            product_id: '상품 아이디' // 가져올 상품의 아이디
        },
        success: function(response) {
            // 가져온 상태 정보를 확인하고 아이콘을 변경하는 로직
            var status = response.status; // 가져온 상태 정보
            if (status === 'active') {
                // 아이콘을 활성화 상태로 변경
                $('#icon').addClass('active');
            } else {
                // 아이콘을 비활성화 상태로 변경
                $('#icon').removeClass('active');
            }
        }
    });
    
});